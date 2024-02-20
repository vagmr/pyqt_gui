from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QTableWidgetItem
from PyQt6.QtGui import QIcon
from ui.ui_VPsw import Ui_password_manage
from PyQt6.QtCore import Qt, QTimer
from qfluentwidgets import (InfoBar, InfoBarIcon, Flyout, FlyoutView, PrimaryPushButton, TableWidget, CardWidget,
                            InfoBarPosition, MessageBox, FluentIcon, FlyoutAnimationType,
                            ComboBox, SmoothScrollArea)
from psw import generate_password
from enum import Enum
import sys
import os
import pyperclip
from json import loads, dumps

application_path = ''
config_save_path = ''
psw_list = []

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    application_path = sys._MEIPASS  # type: ignore
    config_save_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
    config_save_path = application_path

config_path = os.path.join(config_save_path, 'config')

if os.path.exists(config_path) and os.path.isfile(os.path.join(config_path, 'psw.json')):
    try:
        with open(os.path.join(config_path, 'psw.json'), 'r', encoding='utf-8') as f:
            psw_list = loads(f.read())
    except Exception as e:
        print(e)


class CopyType(Enum):
    USERNAME = 0
    PASSWORD = 1
    ALL = 2


class ShowItems(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layoutView = QVBoxLayout(self)
        self._init_layout()
        self._init_widget()
        self.init_table_item()

    def _init_widget(self):
        self.setWindowTitle("展示保存项")
        self.setGeometry(200, 100, 500, 300)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.close_btn.clicked.connect(self.close)  # type: ignore
        self.table.setRowCount(len(psw_list))
        self.table.setColumnCount(4)
        self.table.setFixedWidth(500)
        self.table.setBorderVisible(True)
        self.table.setBorderRadius(8)
        self.table.setHorizontalHeaderLabels(['标记', '用户名', '密码', '网址'])

    def _init_layout(self):
        self.table = TableWidget()
        self.close_btn = PrimaryPushButton('关闭')
        self.layoutView.addWidget(self.table)
        self.layoutView.addWidget(self.close_btn)
        self.setLayout(self.layoutView)

    def init_table_item(self):
        marks = [m for i in psw_list for m, _ in i.items()]
        for row, data_dict in enumerate(psw_list):
            for col, (mark, credentials) in enumerate(data_dict.items()):
                self.table.setItem(row, 0, QTableWidgetItem(mark))
                self.table.setItem(
                    row, 1, QTableWidgetItem(credentials['username']))
                self.table.setItem(
                    row, 2, QTableWidgetItem(credentials['password']))
                self.table.setItem(
                    row, 3, QTableWidgetItem(credentials['url']))

    def refresh_table(self):
        self.table.clearContents()
        self.table.setRowCount(len(psw_list))
        self.init_table_item()


class Window2(QWidget, Ui_password_manage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        os.chdir(application_path)
        self.copy_type = CopyType.ALL
        self._init_window()
        self.signalToSlot()
        self.show()

    def _init_window(self):
        self.setWindowIcon(QIcon('./assets/password.png'))
        self.setFixedSize(600, 400)
        # 小部件设置
        self.show_widget = ShowItems()
        self.ImageLabel.setImage('./assets/password.png')
        self.ImageLabel.setFixedSize(100, 100)
        self.ToolButton.setIcon(FluentIcon.SEARCH)
        self.ToolButton.setFixedWidth(80)
        self.LineEdit.setClearButtonEnabled(True)
        self.LineEdit_2.setClearButtonEnabled(True)
        self.LineEdit_3.setClearButtonEnabled(True)
        self.LineEdit_4.setClearButtonEnabled(True)
        self.PushButton.setIcon(QIcon('./assets/gen.svg'))
        self.save_btn.setIcon(FluentIcon.SAVE)
        self.show_btn.setIcon(FluentIcon.SHARE)

    def signalToSlot(self):
        # 信号和槽
        self.PushButton.clicked.connect(self.setPassword)
        self.save_btn.clicked.connect(self.save_password)
        self.ToolButton.clicked.connect(self.showSearchResult)
        self.show_btn.clicked.connect(self.show_save_items)

    def show_save_items(self):
        self.show_widget.refresh_table()
        self.show_widget.show()

    def show_info(self, content='', title='', parent=None, success=True, duration=2000):
        """
        显示信息栏，包含指定的内容、标题、父级和成功状态。

        :param content: 信息栏要显示的内容（默认为空字符串）
        :param title: 信息栏的标题（默认为空字符串）
        :param parent: 信息栏的父级组件（默认为None）
        :param success: 布尔值，指示信息栏应该显示成功还是错误图标（默认为True）
        """
        self.info = InfoBar.new(
            icon=InfoBarIcon.SUCCESS if success else InfoBarIcon.ERROR,
            title=title,
            content=content,
            isClosable=True,
            duration=duration if success else -1,
            parent=parent or self,
            position=InfoBarPosition.TOP
        )
        self.info.show()

    def showSearchResult(self):
        if not self.LineEdit.text():
            self.show_info(title='错误', content='请输入标记', success=False)
            return
        for i in psw_list:
            item = i.get(self.LineEdit.text())
            if item:
                view = FlyoutView(
                    title="搜索的结果",
                    content="用户名:{0}\n密码:{1}\n{2}".format(
                        item['username'], item['password'], item['url']),
                    parent=self,
                    isClosable=True
                )
                row = QHBoxLayout()
                row.setContentsMargins(0, 10, 0, 0)
                combobox = ComboBox()
                combobox.addItems(['复制用户名', '复制密码', '复制全部'])
                combobox.setCurrentIndex(2)
                combobox.currentIndexChanged.connect(
                    lambda: self.change_copy_type(combobox.currentIndex()))
                btn = PrimaryPushButton(FluentIcon.COPY, "复制")
                btn.clicked.connect(lambda: self.copy_item(item=item))
                row.addWidget(combobox)
                row.addSpacing(10)
                row.addWidget(btn)
                view.widgetLayout.addLayout(row)
                w = Flyout.make(view, self.ToolButton, self,
                                aniType=FlyoutAnimationType.PULL_UP)
                view.closed.connect(w.close)  # type: ignore
            else:
                self.show_info(title='错误', content='没有找到标记', success=False)

    def change_copy_type(self, index=2):
        if index == 0:
            self.copy_type = CopyType.USERNAME
        elif index == 1:
            self.copy_type = CopyType.PASSWORD
        else:
            self.copy_type = CopyType.ALL

    def copy_item(self, item={}):
        if self.copy_type == CopyType.USERNAME:
            pyperclip.copy(item['username'])
        elif self.copy_type == CopyType.PASSWORD:
            pyperclip.copy(item['password'])
        else:
            pyperclip.copy(
                text=f"{item['username']}-{item['password']}-{item['url']}")
        self.show_info(title='已复制到剪切板', content='')

    def setPassword(self):
        password = generate_password()
        self.LineEdit_3.setText(password)
        pyperclip.copy(password)
        self.show_info(title='密码生成成功,已复制到剪切板', content='')

    def is_confirm(self, content="modify?"):
        dialog = MessageBox(title="提示", parent=self, content=content)
        if dialog.exec():
            return True
        return False

    def check_required(self):
        if self.LineEdit.text() == '' or self.LineEdit_2.text() == '' or self.LineEdit_3.text() == '':
            self.show_info(
                title='错误', content='请填写完整,用户名,标记和密码为必填项', success=False)
            return False
        else:
            return True

    def is_many_marked(self, psw_dict):
        global psw_list
        mark = self.LineEdit.text()
        for i, entry in enumerate(psw_list):
            if mark in entry:
                if self.is_confirm(content="标记已存在，是否覆盖?"):
                    psw_list.remove(entry)
                    psw_list.insert(i, psw_dict)
                    self.show_info(content="覆盖成功", title='覆盖成功', duration=500)
                    QTimer.singleShot(600, self.save_password_to_file)
                    return False
                else:
                    self.show_info(
                        title='错误', content='标记已存在,请重新输入', success=False)
                    return False
        return True

    def save_password_to_file(self):
        if not os.path.exists(config_path):
            os.mkdir(config_path)
        with open(os.path.join(config_path, 'psw.json'), 'w', encoding='utf-8') as f:
            f.write(dumps(psw_list))
        self.show_info(content="写入文件成功", title='保存成功')

    def save_password(self):
        global psw_list
        if not self.check_required():
            return
        mark = self.LineEdit.text()
        username = self.LineEdit_2.text()
        password = self.LineEdit_3.text()
        url = self.LineEdit_4.text() if self.LineEdit_4.text() else ''
        psw_dict = {
            mark: {
                'username': username,
                'password': password,
                'url': url
            }
        }
        if not self.is_many_marked(psw_dict):
            return
        psw_list.append(psw_dict)
        self.save_password_to_file()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = Window2()

    sys.exit(app.exec())
