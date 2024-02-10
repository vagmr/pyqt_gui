from PyQt6.QtWidgets import QApplication, QWidget, QCheckBox, QHBoxLayout, QVBoxLayout, QLabel, QSpinBox
from PyQt6.QtCore import QTimer
from qfluentwidgets import CheckBox, SpinBox
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        w_style = """
        QWidget {
            background-color: #7bed9f;
            color: #000000;
        }
        QCheckBox {
            font-size: 20px;
            font-weight: bold;
            color: #2ecc71
            
        }
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
        }

        """
        self.setStyleSheet(w_style)
        row1 = QHBoxLayout()
        cb1 = QCheckBox('复选框1')
        cb1.stateChanged.connect(lambda: self.label1.setText('复选框1被改变了'))
        cb2 = QCheckBox('复选框2')
        cb3 = QCheckBox('复选框3')
        row1.addWidget(cb1)
        row1.addWidget(cb2)
        row1.addWidget(cb3)
        row2 = QHBoxLayout()
        cb4 = CheckBox('复选框4')
        cb5 = CheckBox('复选框5')
        cb6 = CheckBox('复选框6')
        row2.addWidget(cb4)
        row2.addWidget(cb5)
        row2.addWidget(cb6)
        column = QVBoxLayout()
        row3 = QHBoxLayout()
        self.label1 = QLabel('标签1')
        spinbox = QSpinBox(self)
        self.spinbox2 = SpinBox(self)
        column.addLayout(row1)
        column.addLayout(row2)
        row3.addWidget(self.label1)
        row3.addWidget(spinbox)
        row3.addWidget(self.spinbox2)
        column.addLayout(row3)
        # 设置定时器
        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.setSingleShot(True)
        self.spinbox2.valueChanged.connect(self.handler_value_changed)
        self.timer.timeout.connect(self.handler_timeout)
        self.setLayout(column)
        # 防抖

    def handler_timeout(self):
        self.label1.setText(str(self.spinbox2.value()))

    def handler_value_changed(self):
        if self.timer.isActive():
            self.timer.stop()
        self.timer.start()


app = QApplication(sys.argv)
w = Window()
sys.exit(app.exec())
