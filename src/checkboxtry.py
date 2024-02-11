from PyQt6.QtWidgets import (QApplication, QWidget, QCheckBox,
                             QHBoxLayout, QVBoxLayout, QLabel,
                             QSpinBox, QLCDNumber, QSlider, QListWidget)
from PyQt6.QtCore import QTimer, Qt, QTime
from PyQt6.QtGui import QColor, QIcon
from qfluentwidgets import CheckBox, SpinBox, Slider, ListWidget
from qfluentwidgets.components.widgets.acrylic_label import AcrylicLabel
from qfluentwidgets.components.material import AcrylicLineEdit
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
        self.setWindowTitle('复选框学习')
        self.setWindowIcon(QIcon('../img/py.svg'))
        row0 = QHBoxLayout()
        self.lcd = QLCDNumber()
        self.lcd.setStyleSheet(
            'QLCDNumber {background-color: #666;color: #fff;padding: 5px;}')
        self.lcd.setDigitCount(8)
        self.current_time = QTime()
        self.refresh_time()  # 初始化时更新一次时间

        self.lcd_timer = QTimer(self)  # 创建定时器
        self.lcd_timer.timeout.connect(self.refresh_time)  # 每次定时器触发时刷新时间
        self.lcd_timer.start(1000)  # 每隔一秒触发定时器
        row0.addWidget(self.lcd)
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
        spinbox.setMinimum(1)
        spinbox.setMaximum(20)
        self.spinbox2 = SpinBox(self)
        column.addLayout(row0)
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
        row4 = QHBoxLayout()
        acryli_line = AcrylicLineEdit()
        acryli_line.setClearButtonEnabled(True)
        label2 = AcrylicLabel(
            blurRadius=10, tintColor=QColor(105, 114, 168, 102))
        label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label2.setText('write here')
        label2.setFixedSize(100, 30)
        row4.addWidget(label2)
        row4.addWidget(acryli_line)
        row5 = self.init_slider()
        row6 = QHBoxLayout()
        list_widget1 = QListWidget()
        list_widget1.insertItem(0, 'python')
        list_widget1.insertItem(1, 'java')
        list_widget1.insertItem(2, 'c++')
        list_widget1.insertItem(3, 'c#')
        list_widget1.insertItem(4, 'kotlin')
        list_widget2 = ListWidget()
        list_widget2.insertItem(0, 'python')
        list_widget2.insertItem(1, 'java')
        list_widget2.insertItem(2, 'c++')
        list_widget2.insertItem(3, 'c#')
        list_widget2.insertItem(4, 'kotlin')
        row6.addWidget(list_widget1)
        row6.addWidget(list_widget2)
        column.addLayout(row6)
        column.addLayout(row5)
        self.setLayout(column)

    def init_slider(self):
        row = QHBoxLayout()
        left_row = QHBoxLayout()
        right_row = QHBoxLayout()
        slider1 = QSlider()
        slider1.setOrientation(Qt.Orientation.Horizontal)
        slider1.setTickPosition(QSlider.TickPosition.TicksAbove)
        slider1.setTickInterval(2)
        slider1.setMaximum(10)
        l_label = QLabel('')
        slider1.valueChanged.connect(
            lambda: l_label.setText(str(slider1.value())))
        left_row.addWidget(l_label)
        left_row.addWidget(slider1)

        slider2 = Slider()
        slider2.setOrientation(Qt.Orientation.Horizontal)
        slider2.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider2.setMaximum(10)
        r_label = AcrylicLabel(
            blurRadius=5, tintColor=QColor(191, 15, 24, 102))
        r_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        r_label.setMinimumWidth(10)
        slider2.valueChanged.connect(
            lambda: r_label.setText(str(slider2.value()))
        )
        right_row.addWidget(r_label)
        right_row.addWidget(slider2)
        row.addLayout(left_row)
        row.addLayout(right_row)
        return row

    def refresh_time(self):
        self.current_time = QTime.currentTime()
        time_str = self.current_time.toString('hh:mm:ss')
        self.lcd.display(time_str)

    def handler_timeout(self):
        self.label1.setText(str(self.spinbox2.value()))

    def handler_value_changed(self):
        if self.timer.isActive():
            self.timer.stop()
        self.timer.start()


app = QApplication(sys.argv)
w = Window()
sys.exit(app.exec())
