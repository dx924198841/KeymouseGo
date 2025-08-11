# -*- coding: utf-8 -*-
import json
import os
import datetime
from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import QDateTime
from UITaskDialogView import Ui_UITaskDialogView
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('UITaskDialogFunc')

class UITaskDialogFunc(QDialog):
    """
    任务对话框功能类，用于创建和编辑定时任务
    """
    def __init__(self, parent=None, macro_files=None, macro_paths=None):
        """
        初始化任务对话框
        :param parent: 父窗口
        :param macro_files: 可用的宏文件列表
        :param macro_paths: 宏文件的完整路径列表
        """
        super(UITaskDialogFunc, self).__init__(parent)
        self.ui = Ui_UITaskDialogView()
        self.ui.setupUi(self)
        self.macro_files = macro_files or []
        self.macro_paths = macro_paths or {}  # 使用字典保存文件名到路径的映射
        self.init_ui()
        self.connect_signals()
        # 设置中文字体
        self.setFont(parent.font() if parent else self.font())
        # 任务数据
        self.task_data = {}
        # 任务保存目录
        self.tasks_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tasks')
        if not os.path.exists(self.tasks_dir):
            os.makedirs(self.tasks_dir)

    def init_ui(self):
        """初始化UI组件"""
        
        # 填充宏文件下拉列表
        for file_name in self.macro_files:
            self.ui.comboBox_macro.addItem(file_name)
        
        # 设置默认时间
        now = QDateTime.currentDateTime()
        self.ui.dateTimeEdit_start_time.setDateTime(now)
        # 默认结束时间为明天的同一时间
        tomorrow = now.addDays(1)
        self.ui.dateTimeEdit_end_time.setDateTime(tomorrow)
        
        # 设置时间格式
        self.ui.dateTimeEdit_start_time.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.ui.dateTimeEdit_end_time.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

    def connect_signals(self):
        """连接信号和槽函数"""
        
        self.ui.pushButton_ok.clicked.connect(self.on_ok_clicked)
        self.ui.pushButton_cancel.clicked.connect(self.reject)

    def on_ok_clicked(self):
        """确定按钮点击事件处理"""
        
        # 验证输入
        if not self.validate_input():
            return
        
        # 收集任务数据
        self.collect_task_data()
        
        # 保存任务
        self.save_task()
        
        # 关闭对话框
        self.accept()

    def validate_input(self):
        """
        验证用户输入
        :return: 输入有效返回True，否则False
        """
        # 验证任务名称
        task_name = self.ui.lineEdit_task_name.text().strip()
        if not task_name:
            QMessageBox.warning(self, "Warning", "Task name cannot be empty!")
            return False
        
        # 验证宏文件选择
        if self.ui.comboBox_macro.currentIndex() == -1:
            QMessageBox.warning(self, "Warning", "Please select a macro file!")
            return False
        
        # 验证时间范围
        start_time = self.ui.dateTimeEdit_start_time.dateTime()
        end_time = self.ui.dateTimeEdit_end_time.dateTime()
        if start_time >= end_time:
            QMessageBox.warning(self, "Warning", "End time must be later than start time!")
            return False
        
        return True

    def collect_task_data(self):
        """收集任务数据"""
        # 获取基本信息
        task_name = self.ui.lineEdit_task_name.text().strip()
        macro_name = self.ui.comboBox_macro.currentText()
        start_time = self.ui.dateTimeEdit_start_time.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        end_time = self.ui.dateTimeEdit_end_time.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        interval_value = self.ui.spinBox_interval_value.value()
        interval_unit = self.ui.comboBox_interval_unit.currentText()
        frequency = self.ui.spinBox_frequency.value()
        
        # 构建任务数据
        self.task_data = {
            "task_name": task_name,
            "macro_name": macro_name,
            "start_time": start_time,
            "end_time": end_time,
            "interval_value": interval_value,
            "interval_unit": interval_unit,
            "frequency": frequency,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 如果有宏文件路径映射，添加宏文件的完整路径
        if macro_name in self.macro_paths:
            self.task_data["macro_path"] = self.macro_paths[macro_name]

    def save_task(self):
        """保存任务到文件"""
        try:
            # 生成唯一的任务ID (使用时间戳)
            task_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            task_file = os.path.join(self.tasks_dir, f"task_{task_id}.json5")
            
            # 保存为JSON5格式
            with open(task_file, 'w', encoding='utf-8') as f:
                # 使用json.dump并设置indent使其易读
                json.dump(self.task_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Task saved successfully: {task_file}")
            QMessageBox.information(self, "Success", f"Task '{self.task_data['task_name']}' created successfully!")
        except Exception as e:
            logger.error(f"Failed to save task: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to save task: {str(e)}")

    def get_task_data(self):
        """
        获取任务数据
        :return: 任务数据字典
        """
        return self.task_data

# 示例用法
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # 模拟宏文件列表
    macro_files = ["macro1.json5", "macro2.json5", "macro3.json5"]
    dialog = UITaskDialogFunc(macro_files=macro_files)
    if dialog.exec() == QDialog.Accepted:
        task_data = dialog.get_task_data()
        print("Task data:", task_data)
    sys.exit(app.exec())