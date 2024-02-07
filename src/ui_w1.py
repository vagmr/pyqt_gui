# Form implementation generated from reading ui file 'w1.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_window(object):
    def setupUi(self, window):
        window.setObjectName("window")
        window.setWindowModality(QtCore.Qt.WindowModality.NonModal)
        window.resize(716, 523)
        self.TitleLabel = TitleLabel(parent=window)
        self.TitleLabel.setGeometry(QtCore.QRect(240, 0, 231, 38))
        self.TitleLabel.setObjectName("TitleLabel")
        self.CardWidget = CardWidget(parent=window)
        self.CardWidget.setGeometry(QtCore.QRect(0, 50, 711, 326))
        self.CardWidget.setBorderRadius(6)
        self.CardWidget.setObjectName("CardWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.CardWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, -1, 9, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.BodyLabel = BodyLabel(parent=self.CardWidget)
        self.BodyLabel.setProperty("pixelFontSize", 16)
        self.BodyLabel.setObjectName("BodyLabel")
        self.horizontalLayout_4.addWidget(self.BodyLabel)
        self.LineEdit = LineEdit(parent=self.CardWidget)
        self.LineEdit.setBaseSize(QtCore.QSize(40, 0))
        self.LineEdit.setObjectName("LineEdit")
        self.horizontalLayout_4.addWidget(self.LineEdit)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)
        self.CaptionLabel = CaptionLabel(parent=self.CardWidget)
        self.CaptionLabel.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.CaptionLabel.setScaledContents(False)
        self.CaptionLabel.setProperty("pixelFontSize", 15)
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.horizontalLayout_3.addWidget(self.CaptionLabel)
        self.CalendarPicker = CalendarPicker(parent=self.CardWidget)
        icon = QtGui.QIcon.fromTheme("application-exit")
        self.CalendarPicker.setIcon(icon)
        self.CalendarPicker.setIconSize(QtCore.QSize(32, 32))
        self.CalendarPicker.setAutoRepeatDelay(300)
        self.CalendarPicker.setFlat(True)
        self.CalendarPicker.setObjectName("CalendarPicker")
        self.horizontalLayout_3.addWidget(self.CalendarPicker)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.StrongBodyLabel = StrongBodyLabel(parent=self.CardWidget)
        self.StrongBodyLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.StrongBodyLabel.setObjectName("StrongBodyLabel")
        self.verticalLayout.addWidget(self.StrongBodyLabel)
        self.PlainTextEdit = PlainTextEdit(parent=self.CardWidget)
        self.PlainTextEdit.setObjectName("PlainTextEdit")
        self.verticalLayout.addWidget(self.PlainTextEdit)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.BodyLabel_2 = BodyLabel(parent=self.CardWidget)
        self.BodyLabel_2.setObjectName("BodyLabel_2")
        self.horizontalLayout_5.addWidget(self.BodyLabel_2)
        self.PrimaryDropDownPushButton = PrimaryDropDownPushButton(parent=self.CardWidget)
        self.PrimaryDropDownPushButton.setCheckable(True)
        self.PrimaryDropDownPushButton.setObjectName("PrimaryDropDownPushButton")
        self.horizontalLayout_5.addWidget(self.PrimaryDropDownPushButton)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.PrimaryPushButton = PrimaryPushButton(parent=self.CardWidget)
        self.PrimaryPushButton.setObjectName("PrimaryPushButton")
        self.horizontalLayout_6.addWidget(self.PrimaryPushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "打卡组件"))
        self.TitleLabel.setText(_translate("window", "vagmr的打卡软件"))
        self.BodyLabel.setText(_translate("window", "填写项目"))
        self.CaptionLabel.setText(_translate("window", "选择日期："))
        self.CalendarPicker.setText(_translate("window", "请选择打卡日期"))
        self.StrongBodyLabel.setText(_translate("window", "打卡留言"))
        self.BodyLabel_2.setText(_translate("window", "输入打卡时间(分)"))
        self.PrimaryDropDownPushButton.setText(_translate("window", "点击选择"))
        self.PrimaryPushButton.setText(_translate("window", "点击开始"))
from qfluentwidgets import BodyLabel, CalendarPicker, CaptionLabel, CardWidget, LineEdit, PlainTextEdit, PrimaryDropDownPushButton, PrimaryPushButton, StrongBodyLabel, TitleLabel
