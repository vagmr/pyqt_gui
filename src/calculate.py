from PyQt6.QtWidgets import QApplication, QPushButton, QHBoxLayout
from ui_calculate import Ui_Form
from PyQt6.QtGui import QIcon
from qfluentwidgets import CardWidget
import sys


class Window(CardWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(
            QIcon("../img/c.svg"))
        self.setFixedSize(300, 500)
        self.language.setIcon(QIcon("../img/l.svg"))
        self.language.addItem("简体中文")
        self.language.addItem("English")
        self.language.setFixedWidth(120)
        self.language.setCurrentIndex(0)
        self.language.currentIndexChanged.connect(self.change_language)
        self.PrimaryPushButton.clicked.connect(self.start_calculate)
        btn = QPushButton("clear", self)
        btn.setFixedSize(260, 25)
        btn_layout = QHBoxLayout(self)
        # 按钮样式
        btn_style = """
            QPushButton {
                background-color: #ee7959;
                color: #000000;
                font-weight: bold;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ff9999; /* 悬停时的颜色 */
            }
            QPushButton:pressed {
                background-color: #cc6043; /* 按下时的颜色 */
            }
        """
        btn.setStyleSheet(btn_style)
        btn_layout.addWidget(btn)
        btn_layout.setContentsMargins(0, 10, 0, 40)
        btn.clicked.connect(self.clear)
        self.output = None
        self.show()

    def is_cn(self):
        return self.language.currentIndex() == 0

    def start_calculate(self):
        str1 = self.LineEdit.text()
        str2 = self.LineEdit_2.text()
        if not str1 or not str2:
            self.TextEdit.setText("请输入内容" if self.is_cn()
                                  else "Please input content")
            return
        num1 = float(str1)
        num2 = float(str2)
        res = self.operation(num1, num2)
        self.TextEdit.setText(
            f"{res}")

    def clear(self):
        self.LineEdit.clear()
        self.LineEdit_2.clear()

    def operation(self, num1, num2):
        if self.RadioButton.isChecked():
            return f"{num1} + {num2} = {num1 + num2}"
        elif self.RadioButton_2.isChecked():
            return f"{num1} - {num2} = {num1 - num2}"
        elif self.RadioButton_3.isChecked():
            return f"{num1} * {num2} = {num1 * num2}"
        elif self.RadioButton_4.isChecked():
            if num2 == 0:
                return "除数不能为0" if self.is_cn() else "The divisor can not be 0"
            return f"{num1} / {num2} = {num1 / num2}"
        else:
            return "请选择运算方式" if self.is_cn() else "Please select the operation mode"


app = QApplication(sys.argv)
w = Window()

sys.exit(app.exec())
