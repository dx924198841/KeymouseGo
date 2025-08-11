#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UI文件预览工具
用于在修改UI文件后快速预览效果，无需先编译成Python文件
使用方法: python preview_ui.py <ui_file_path>
"""

import sys
import os
from PySide6.QtCore import QFile, QIODevice, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication

# 设置必要的属性以避免Qt WebEngine警告
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)
if hasattr(QGuiApplication, 'setGraphicsApi') and hasattr(QGuiApplication, 'OpenGLRhi'):
    QGuiApplication.setGraphicsApi(QGuiApplication.OpenGLRhi)


def preview_ui(ui_file_path):
    """预览UI文件

    Args:
        ui_file_path (str): UI文件路径
    """
    # 检查文件是否存在
    if not os.path.exists(ui_file_path):
        print(f"错误: 找不到UI文件 '{ui_file_path}'")
        return

    # 创建应用程序
    app = QApplication(sys.argv)

    # 加载UI文件
    ui_file = QFile(ui_file_path)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"错误: 无法打开UI文件 '{ui_file_path}'")
        return

    # 创建UI加载器
    loader = QUiLoader()
    # 加载UI文件并创建窗口
    window = loader.load(ui_file)
    ui_file.close()

    # 检查窗口是否成功创建
    if window is None:
        print(f"错误: 无法加载UI文件 '{ui_file_path}'")
        return

    # 显示窗口
    window.show()
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("使用方法: python preview_ui.py <ui_file_path>")
        print("示例: python preview_ui.py UIView.ui")
    else:
        preview_ui(sys.argv[1])