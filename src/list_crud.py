from PyQt6.QtWidgets import (QApplication, QWidget, QLCDNumber, QStyle,
                             QHBoxLayout, QVBoxLayout, QListWidgetItem, QLabel)
import sys
from PyQt6.QtCore import QTime, QTimer, Qt, QSize
from PyQt6.QtGui import QIcon

from qfluentwidgets import (ListWidget, PushButton, CardWidget,
                            PrimaryPushButton, FluentIcon, BodyLabel)
from qfluentwidgets.components.material import AcrylicLineEdit
from json import loads

item = {}
style = ''
try:
    with open('item.json', 'r', encoding='utf-8') as f:
        item = loads(f.read())
    with open('list_crud.qss', 'r', encoding='utf-8') as f:
        style = f.read()
except:
    raise FileNotFoundError('../item.json not found!')


class Window(QWidget):
    def __init__(self):
        super().__init__()
        # 窗口设置
        self.setWindowTitle("ListWidget")
        self.setWindowIcon(QIcon("../img/py.svg"))
        self.isInitList = False
        # lcd设置
        self.lcd = QLCDNumber(self)
        self.lcd.setDigitCount(8)
        self.current_time = QTime()
        self.refresh_time()
        # 定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_time)
        self.timer.start(1000)
        # 列表设置
        self.list = ListWidget(self)
        # 一些按钮
        init_btn = PrimaryPushButton(FluentIcon.PLAY, '初始化列表')
        init_btn.clicked.connect(self._init_list)
        delete_btn = PushButton(FluentIcon.DELETE, '删除选中')
        delete_btn.setStyleSheet(style)
        delete_btn.clicked.connect(
            lambda: self.list.takeItem(self.list.currentRow()))  # type: ignore
        add_btn = PushButton(FluentIcon.ADD, '添加')
        # 弹出窗口设置
        put_widget = CardWidget()
        put_widget.setGeometry(460, 210, 150, 200)
        put_widget.setFixedSize(250, 180)
        put_widget.setWindowFlags(put_widget.windowFlags(
        ) | Qt.WindowType.FramelessWindowHint)  # 设置无边框窗口
        put_widget.setStyleSheet('background-color: #ccc;')
        w_layout = QVBoxLayout()
        w_row1 = QHBoxLayout()
        title = QLabel('添加新的条目')
        title.setStyleSheet(
            'font-weight: bold;background-color: transparent;color: #36d;font-size: 16px;')
        close_btn = PushButton(FluentIcon.CLOSE, '')
        close_btn.clicked.connect(lambda: put_widget.close())
        close_btn.setFixedWidth(25)
        close_btn.setStyleSheet('background-color: transparent;padding: 5px;')
        close_btn.setIconSize(QSize(20, 30))
        w_row1.addWidget(title)
        w_row1.addWidget(close_btn)
        w_row2 = QHBoxLayout()
        bodylabel = BodyLabel('新的条目名')
        edit = AcrylicLineEdit()
        edit.setPlaceholderText('请输入条目名')
        w_row2.addWidget(bodylabel)
        w_row2.addWidget(edit)
        w_row3 = QHBoxLayout()
        confirm_btn = PushButton(FluentIcon.PLAY, '确认添加')
        confirm_btn.clicked.connect(lambda: self.add_item(edit.text()))
        w_row3.addWidget(confirm_btn)
        w_row4 = QHBoxLayout()
        self.resLabel = QLabel('')
        self.resLabel.setStyleSheet(
            'color: #f00;font-size: 16px;')
        self.resLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        w_row4.addWidget(self.resLabel)
        w_layout.addLayout(w_row1)
        w_layout.addLayout(w_row2)
        w_layout.addLayout(w_row3)
        w_layout.addLayout(w_row4)
        put_widget.setLayout(w_layout)
        add_btn.clicked.connect(lambda: put_widget.show())
        # 布局设置
        layout = QVBoxLayout(self)
        row1 = QHBoxLayout()
        row1.addWidget(self.lcd)
        row2 = QHBoxLayout()
        row2.addWidget(self.list)
        row3 = QHBoxLayout()
        row3.addWidget(init_btn)
        row3.addWidget(delete_btn)
        row4 = QHBoxLayout()
        row4.addWidget(add_btn)
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addLayout(row4)
        self.show()

    def refresh_time(self):
        self.current_time = QTime.currentTime()
        time_str = self.current_time.toString('hh:mm:ss')
        self.lcd.display(time_str)

    def _init_list(self):
        global item
        if not self.isInitList:
            for i in item['item']:
                item = QListWidgetItem(i)
                self.list.addItem(item)
            self.isInitList = True
        else:
            return

    def add_item(self, value):
        if not value:
            self.resLabel.setText('请输入条目名')
            return
        item = QListWidgetItem(value)
        self.list.addItem(item)
        self.resLabel.setText('添加成功!')


app = QApplication(sys.argv)
w = Window()

sys.exit(app.exec())
