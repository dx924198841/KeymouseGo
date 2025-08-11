#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务调度器模块
负责读取任务文件、解析时间单位并执行定时任务
"""
import os
import json
import json5
import time
import threading
import datetime
from Util.RunScriptClass import RunScriptCMDClass
from PySide6.QtCore import QThread, Signal
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('TaskScheduler')

class StopFlag:
    def __init__(self):
        self.value = False

class TaskScheduler(QThread):
    """任务调度器类"""
    # 定义信号
    task_started = Signal(str)
    task_finished = Signal(str)
    task_error = Signal(str, str)

    def __init__(self, tasks_dir):
        """
        初始化任务调度器
        :param tasks_dir: 任务文件目录
        """
        super().__init__()
        self.tasks_dir = tasks_dir
        self.running = False
        self.task_threads = {}
        self.stop_flags = {}
        self.last_check_time = {}

    def run(self):
        """运行任务调度器"""
        self.running = True
        logger.info(f"Task scheduler started, monitoring directory: {self.tasks_dir}")

        while self.running:
            try:
                # 检查新任务
                self._check_new_tasks()
                # 检查任务状态
                self._check_task_status()
                # 优化：增加检查间隔至5秒以减轻系统负担
                time.sleep(5)
            except Exception as e:
                logger.error(f"Error in task scheduler: {str(e)}")
                self.task_error.emit("scheduler", str(e))

        logger.info("Task scheduler stopped")

    def stop(self):
        """停止任务调度器"""
        self.running = False
        # 停止所有运行中的任务
        for task_id, flag in self.stop_flags.items():
            flag.value = True
        # 等待所有任务线程结束
        for task_id, thread in self.task_threads.items():
            if thread.is_alive():
                thread.join(timeout=5.0)  # 设置5秒超时，避免无限等待
        self.wait()

    def _check_new_tasks(self):
        """检查新任务"""
        # 确保任务目录存在
        if not os.path.exists(self.tasks_dir):
            try:
                os.makedirs(self.tasks_dir)
                logger.info(f"Created tasks directory: {self.tasks_dir}")
            except Exception as e:
                logger.error(f"Failed to create tasks directory: {str(e)}")
                self.task_error.emit("scheduler", f"Failed to create tasks directory: {str(e)}")
                return

        # 获取所有任务文件
        for file_name in os.listdir(self.tasks_dir):
            if not file_name.endswith('.json5'):
                continue

            task_id = file_name.split('.')[0]
            # 如果任务已经在运行，跳过
            if task_id in self.task_threads:
                continue

            task_file = os.path.join(self.tasks_dir, file_name)
            # 检查文件修改时间
            file_mtime = os.path.getmtime(task_file)
            # 如果文件没有修改，跳过
            if task_id in self.last_check_time and self.last_check_time[task_id] >= file_mtime:
                continue
            # 更新最后检查时间
            self.last_check_time[task_id] = file_mtime

            try:
                # 读取任务文件
                with open(task_file, 'r', encoding='utf-8') as f:
                    task_data = json5.load(f)

                # 检查任务时间
                now = datetime.datetime.now()
                start_time = datetime.datetime.strptime(task_data['start_time'], '%Y-%m-%d %H:%M:%S')
                end_time = datetime.datetime.strptime(task_data['end_time'], '%Y-%m-%d %H:%M:%S')

                # 如果任务未到开始时间或已过结束时间，跳过
                if now < start_time or now > end_time:
                    continue

                # 解析时间间隔
                interval_value = task_data['interval_value']
                interval_unit = task_data['interval_unit']
                interval_ms = self._convert_to_ms(interval_value, interval_unit)

                # 计算任务的时间间隔（分钟）
                interval_minutes = 0
                if interval_unit == 'second(s)':
                    interval_minutes = interval_value / 60
                elif interval_unit == 'minute(s)':
                    interval_minutes = interval_value
                elif interval_unit == 'hour(s)':
                    interval_minutes = interval_value * 60
                elif interval_unit == 'day(s)':
                    interval_minutes = interval_value * 24 * 60

                # 计算下次执行时间
                # 首先尝试从任务数据中获取上次执行时间
                last_run_time = start_time
                if 'last_run_time' in task_data:
                    try:
                        last_run_time = datetime.datetime.strptime(task_data['last_run_time'], '%Y-%m-%d %H:%M:%S')
                    except Exception as e:
                        # 如果解析失败，使用开始时间
                        logger.warning(f"Failed to parse last_run_time: {e}, using start_time instead")

                # 计算下次执行时间
                next_run_time = last_run_time
                while next_run_time < now:
                    next_run_time += datetime.timedelta(minutes=interval_minutes)

                # 如果下次执行时间已超过结束时间，则不执行
                if next_run_time > end_time:
                    continue

                # 如果当前时间未到下次执行时间，则等待
                if now < next_run_time:
                    wait_seconds = (next_run_time - now).total_seconds()
                    logger.info(f"Task {task_data['task_name']} will run at {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}, waiting {wait_seconds:.2f} seconds")

                    # 使用循环等待，每5秒检查一次系统时间，以响应系统时间变化
                    remaining_seconds = wait_seconds
                    while remaining_seconds > 0:
                        # 最多等待5秒
                        wait_chunk = min(5, remaining_seconds)
                        time.sleep(wait_chunk)
                        remaining_seconds -= wait_chunk
                        
                        # 检查系统时间是否已到达下次执行时间
                        now = datetime.datetime.now()
                        if now >= next_run_time:
                            break

                # 更新任务的上次执行时间
                task_data['last_run_time'] = now.strftime('%Y-%m-%d %H:%M:%S')
                # 保存更新后的任务文件
                with open(task_file, 'w', encoding='utf-8') as f:
                    json5.dump(task_data, f, ensure_ascii=False, indent=2)

                # 构建脚本路径
                if 'macro_path' in task_data and os.path.exists(task_data['macro_path']):
                    script_path = task_data['macro_path']
                    logger.info(f"Using custom macro path: {script_path}")
                else:
                    script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
                    script_path = os.path.join(script_dir, task_data['macro_name'])

                # 检查脚本文件是否存在
                if os.path.exists(script_path):
                    # 对于分钟级任务，确保间隔大于5分钟
                    if interval_unit == 'minute(s)' and interval_value < 5:
                        logger.warning(f"Task {task_data['task_name']} interval too short. Adjusting from {interval_value} minutes to 5 minutes.")
                        # 更新间隔时间
                        interval_value = 5
                        interval_ms = self._convert_to_ms(interval_value, interval_unit)

                    # 移除秒级任务的限制
                    # 计算宏的全时间周期（仅作记录，不再用于限制）
                    macro_duration = self._get_macro_duration(script_path)
                    logger.info(f"Macro {task_data['macro_name']} duration: {macro_duration}ms")

                # 启动任务线程
                logger.info(f"Starting task: {task_data['task_name']} (ID: {task_id}) with interval {interval_value} {interval_unit}")
                self.task_started.emit(task_data['task_name'])

                stop_flag = StopFlag()
                self.stop_flags[task_id] = stop_flag

                # 创建任务线程
                task_thread = threading.Thread(
                    target=self._run_task,
                    args=(task_data, interval_ms, stop_flag)
                )
                task_thread.daemon = True
                task_thread.start()
                self.task_threads[task_id] = task_thread
            except Exception as e:
                logger.error(f"Error processing task file {file_name}: {str(e)}")
                self.task_error.emit(file_name, str(e))

    def _check_task_status(self):
        """检查任务状态"""
        # 清理已完成的任务线程
        completed_tasks = []
        for task_id, thread in self.task_threads.items():
            if not thread.is_alive():
                completed_tasks.append(task_id)

        for task_id in completed_tasks:
            del self.task_threads[task_id]
            if task_id in self.stop_flags:
                del self.stop_flags[task_id]
            logger.info(f"Task {task_id} completed")
            self.task_finished.emit(task_id)

    def _run_task(self, task_data, interval_ms, stop_flag):
        """
        运行任务
        :param task_data: 任务数据
        :param interval_ms: 间隔时间（毫秒）
        :param stop_flag: 停止标志
        """
        task_name = task_data['task_name']
        macro_name = task_data['macro_name']
        frequency = task_data['frequency']

        # 构建脚本路径
        if 'macro_path' in task_data and os.path.exists(task_data['macro_path']):
            script_path = task_data['macro_path']
            logger.info(f"Using custom macro path: {script_path}")
        else:
            script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
            script_path = os.path.join(script_dir, macro_name)

        # 检查脚本文件是否存在
        if not os.path.exists(script_path):
            error_msg = f"Script file not found: {script_path}"
            logger.error(error_msg)
            self.task_error.emit(task_name, error_msg)
            return

        try:
            # 执行任务指定次数
            for i in range(frequency):
                if stop_flag.value:
                    break

                logger.info(f"Executing task {task_name} (run {i+1}/{frequency})")
                # 使用RunScriptCMDClass执行脚本
                flag = StopFlag()
                runner = RunScriptCMDClass([script_path], 1, flag)
                runner.run()

                # 如果不是最后一次执行，等待间隔时间
                if i < frequency - 1 and not stop_flag.value:
                    # 使用_convert_to_ms确保时间单位正确转换
                    wait_time = self._convert_to_ms(task_data['interval_value'], task_data['interval_unit'])
                    logger.info(f"Task {task_name} waiting for {task_data['interval_value']} {task_data['interval_unit']}")
                    time.sleep(wait_time / 1000)

            logger.info(f"Task {task_name} completed all {frequency} runs")
            self.task_finished.emit(task_name)

            # 任务完成后等待设定的间隔时间
            if not stop_flag.value:
                wait_time = self._convert_to_ms(task_data['interval_value'], task_data['interval_unit'])
                logger.info(f"Task {task_name} waiting for {task_data['interval_value']} {task_data['interval_unit']} before next run")
                time.sleep(wait_time / 1000)

        except Exception as e:
            error_msg = f"Error executing task {task_name}: {str(e)}"
            logger.error(error_msg)
            self.task_error.emit(task_name, error_msg)

    def _get_macro_duration(self, macro_path):
        """
        获取宏的全时间周期（毫秒）
        :param macro_path: 宏文件路径
        :return: 宏的全时间周期（毫秒）
        """
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json5.load(f)

            # 计算宏的总执行时间
            total_duration = 0
            for event in macro_data.get('scripts', []):
                total_duration += event.get('delay', 0)

            return total_duration
        except Exception as e:
            logger.error(f"Error calculating macro duration: {str(e)}")
            return 0

    def _convert_to_ms(self, value, unit):
        """
        将不同时间单位转换为毫秒
        :param value: 数值
        :param unit: 单位
        :return: 毫秒数
        """
        unit_map = {
            'second(s)': 1000,
            'minute(s)': 60 * 1000,
            'hour(s)': 60 * 60 * 1000,
            'day(s)': 24 * 60 * 60 * 1000,
            'week(s)': 7 * 24 * 60 * 60 * 1000,
            'month(s)': 30 * 24 * 60 * 60 * 1000  # 近似值
        }

        if unit not in unit_map:
            logger.warning(f"Unknown time unit: {unit}, defaulting to seconds")
            return value * 1000

        return value * unit_map[unit]

if __name__ == '__main__':
    # 测试任务调度器
    tasks_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tasks')
    scheduler = TaskScheduler(tasks_dir)
    scheduler.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping scheduler...")
        scheduler.stop()