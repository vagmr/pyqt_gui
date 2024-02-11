"""
@文件        :list_crud.py
@说明        :一个简单的关于列表的增删改查的实例 
@时间        :2024/02/11 23:07:03
@作者        :vagmr
@版本        :1.1
"""


from PyQt6.QtWidgets import (QApplication, QWidget, QLCDNumber, QCompleter,
                             QHBoxLayout, QVBoxLayout, QListWidgetItem, QLabel)
import sys
from PyQt6.QtCore import QTime, QTimer, Qt, QSize
from PyQt6.QtGui import QIcon

from qfluentwidgets import (ListWidget, PushButton, CardWidget, InfoBar,
                            PrimaryPushButton, FluentIcon, BodyLabel, SearchLineEdit)
from qfluentwidgets.components.material import AcrylicLineEdit
from json import loads
from customComponets.cusMessageBox import CustomWarningMessageBox

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
        # 提示弹框
        self.info = None
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
        self.list.setFixedHeight(200)
        # 一些按钮
        init_btn = PrimaryPushButton(FluentIcon.PLAY, '初始化列表')
        init_btn.clicked.connect(self._init_list)
        delete_btn = PushButton(FluentIcon.DELETE, '删除选中')
        delete_btn.setStyleSheet(style)
        delete_btn.clicked.connect(self.delete_item)  # type: ignore
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
        close_btn.clicked.connect(lambda: put_widget.close())  # type: ignore
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
        confirm_btn.clicked.connect(
            lambda: self.add_item(edit.text(), put_widget))
        w_row3.addWidget(confirm_btn)
        w_layout.addLayout(w_row1)
        w_layout.addLayout(w_row2)
        w_layout.addLayout(w_row3)
        put_widget.setLayout(w_layout)
        add_btn.clicked.connect(lambda: put_widget.show())
        # 改
        P_edit = AcrylicLineEdit()
        P_edit.setClearButtonEnabled(True)
        put_btn = PushButton(FluentIcon.EDIT, '修改')
        put_btn.clicked.connect(lambda: self.put_item(P_edit.text()))
        # 查
        search_btn = SearchLineEdit()
        self.completer = QCompleter(item['item'], search_btn)
        self.completer.setMaxVisibleItems(4)
        search_btn.setCompleter(self.completer)
        search_btn.searchSignal.connect(
            lambda: self.search_item(search_btn.text()))
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
        row5 = QHBoxLayout()
        row5.addWidget(P_edit)
        row5.addWidget(put_btn)
        row6 = QHBoxLayout()
        row6.addWidget(search_btn)
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addLayout(row6)
        layout.addLayout(row4)
        layout.addLayout(row5)
        self.show()

    def refresh_time(self):
        self.current_time = QTime.currentTime()
        time_str = self.current_time.toString('hh:mm:ss')
        self.lcd.display(time_str)

    def _init_list(self):
        global item
        if not self.isInitList:
            for i in item['item']:
                qitem = QListWidgetItem(i)
                self.list.addItem(qitem)
            self.isInitList = True
        else:
            self.create_warning_info('请不要重复初始化列表')
            return

    def add_item(self, value, infoParent=None):
        if not value:
            self.create_warning_info('请输入条目名', infoParent)
            return
        if not self.isInitList:
            self.create_warning_info('请先初始化列表', infoParent)
            return
        item = QListWidgetItem(value)
        self.list.addItem(item)
        self.create_success_info('添加成功!', infoParent)

    def create_warning_info(self, content, parent=None):
        self.info = InfoBar.new(
            icon=QIcon('../img/al.svg'),
            title='警告',
            content=content,
            isClosable=True,
            duration=2000,
            parent=parent or self
        )
        self.info.setCustomBackgroundColor('#ff9100', "#f00")
        self.info.show()

    def create_success_info(self, content, parent=None):
        self.info = InfoBar.success(
            title='成功',
            content=content,
            parent=parent or self,
            duration=2000
        )
        self.info.show()

    def put_item(self, value):
        if not value:
            self.create_warning_info('请输入条目名')
            return
        elif self.list.currentRow() == -1:
            self.create_warning_info('请选择要修改的条目')
            return
        self.list.currentItem().setText(value)
        self.create_success_info('修改成功!')

    def delete_item(self):
        if self.list.currentRow() == -1:
            self.create_warning_info('请选择要删除的条目')
            return
        dialog = CustomWarningMessageBox(
            parent=self,
            title='警告',
            content='是否确认删除该条目?'
        )
        if dialog.exec():
            self.list.takeItem(self.list.currentRow())
            self.create_success_info('删除成功!')
        else:
            return

    def search_item(self, value):
        if not self.isInitList:
            self.create_warning_info('请先初始化列表')
            return
        elif not value:
            self.create_warning_info('请输入搜索条目')
            return
        if value in item['item']:
            self.list.setCurrentRow(item['item'].index(value))
            self.create_success_info('搜索成功!')
        else:
            self.create_warning_info('搜索失败!')


app = QApplication(sys.argv)
w = Window()

sys.exit(app.exec())
