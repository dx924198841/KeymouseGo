# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UITaskDialogView.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateTimeEdit, QDialog,
    QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpinBox, QSpacerItem,
    QWidget)

class Ui_UITaskDialogView(object):
    def setupUi(self, UITaskDialogView):
        if not UITaskDialogView.objectName():
            UITaskDialogView.setObjectName(u"UITaskDialogView")
        UITaskDialogView.resize(400, 400)
        self.layoutWidget = QWidget(UITaskDialogView)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 381, 351))
        self.formLayout = QFormLayout(self.layoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_task_name = QLabel(self.layoutWidget)
        self.label_task_name.setObjectName(u"label_task_name")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_task_name)

        self.lineEdit_task_name = QLineEdit(self.layoutWidget)
        self.lineEdit_task_name.setObjectName(u"lineEdit_task_name")
        self.lineEdit_task_name.setPlaceholderText(u"Enter task name")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_task_name)

        self.label_macro = QLabel(self.layoutWidget)
        self.label_macro.setObjectName(u"label_macro")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_macro)

        self.comboBox_macro = QComboBox(self.layoutWidget)
        self.comboBox_macro.setObjectName(u"comboBox_macro")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_macro.sizePolicy().hasHeightForWidth())
        self.comboBox_macro.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboBox_macro)

        self.label_start_time = QLabel(self.layoutWidget)
        self.label_start_time.setObjectName(u"label_start_time")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_start_time)

        self.dateTimeEdit_start_time = QDateTimeEdit(self.layoutWidget)
        self.dateTimeEdit_start_time.setObjectName(u"dateTimeEdit_start_time")
        self.dateTimeEdit_start_time.setCalendarPopup(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.dateTimeEdit_start_time)

        self.label_end_time = QLabel(self.layoutWidget)
        self.label_end_time.setObjectName(u"label_end_time")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_end_time)

        self.dateTimeEdit_end_time = QDateTimeEdit(self.layoutWidget)
        self.dateTimeEdit_end_time.setObjectName(u"dateTimeEdit_end_time")
        self.dateTimeEdit_end_time.setCalendarPopup(True)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.dateTimeEdit_end_time)

        self.label_interval = QLabel(self.layoutWidget)
        self.label_interval.setObjectName(u"label_interval")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_interval)

        self.horizontalLayout_interval = QHBoxLayout()
        self.horizontalLayout_interval.setObjectName(u"horizontalLayout_interval")
        self.spinBox_interval_value = QSpinBox(self.layoutWidget)
        self.spinBox_interval_value.setObjectName(u"spinBox_interval_value")
        self.spinBox_interval_value.setMinimum(1)
        self.spinBox_interval_value.setValue(1)

        self.horizontalLayout_interval.addWidget(self.spinBox_interval_value)

        self.comboBox_interval_unit = QComboBox(self.layoutWidget)
        self.comboBox_interval_unit.setObjectName(u"comboBox_interval_unit")
        sizePolicy.setHeightForWidth(self.comboBox_interval_unit.sizePolicy().hasHeightForWidth())
        self.comboBox_interval_unit.setSizePolicy(sizePolicy)
        self.comboBox_interval_unit.addItem(u"second(s)")
        self.comboBox_interval_unit.addItem(u"minute(s)")
        self.comboBox_interval_unit.addItem(u"hour(s)")
        self.comboBox_interval_unit.addItem(u"day(s)")
        self.comboBox_interval_unit.addItem(u"week(s)")
        self.comboBox_interval_unit.addItem(u"month(s)")

        self.horizontalLayout_interval.addWidget(self.comboBox_interval_unit)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_interval)

        self.label_frequency = QLabel(self.layoutWidget)
        self.label_frequency.setObjectName(u"label_frequency")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_frequency)

        self.spinBox_frequency = QSpinBox(self.layoutWidget)
        self.spinBox_frequency.setObjectName(u"spinBox_frequency")
        self.spinBox_frequency.setMinimum(1)
        self.spinBox_frequency.setValue(1)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.spinBox_frequency)

        self.horizontalLayout_buttons = QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName(u"horizontalLayout_buttons")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_buttons.addItem(self.horizontalSpacer)

        self.pushButton_ok = QPushButton(self.layoutWidget)
        self.pushButton_ok.setObjectName(u"pushButton_ok")

        self.horizontalLayout_buttons.addWidget(self.pushButton_ok)

        self.pushButton_cancel = QPushButton(self.layoutWidget)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout_buttons.addWidget(self.pushButton_cancel)


        self.formLayout.setLayout(6, QFormLayout.SpanningRole, self.horizontalLayout_buttons)


        self.retranslateUi(UITaskDialogView)
        self.pushButton_cancel.clicked.connect(UITaskDialogView.reject)

        QMetaObject.connectSlotsByName(UITaskDialogView)
    # setupUi

    def retranslateUi(self, UITaskDialogView):
        UITaskDialogView.setWindowTitle(QCoreApplication.translate("UITaskDialogView", u"Create Task", None))
        self.label_task_name.setText(QCoreApplication.translate("UITaskDialogView", u"Task Name:", None))
        self.label_macro.setText(QCoreApplication.translate("UITaskDialogView", u"Macro:", None))
        self.label_start_time.setText(QCoreApplication.translate("UITaskDialogView", u"Start Time:", None))
        self.label_end_time.setText(QCoreApplication.translate("UITaskDialogView", u"End Time:", None))
        self.label_interval.setText(QCoreApplication.translate("UITaskDialogView", u"Interval:", None))
        self.label_frequency.setText(QCoreApplication.translate("UITaskDialogView", u"Frequency:", None))
        self.pushButton_ok.setText(QCoreApplication.translate("UITaskDialogView", u"OK", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("UITaskDialogView", u"Cancel", None))
    # retranslateUi