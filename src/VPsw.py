from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from ui.ui_VPsw import Ui_password_manage
from qfluentwidgets import (InfoBar, InfoBarIcon,
                            InfoBarPosition, MessageBox, FluentIcon)
from psw import generate_password
import sys
import os
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

if os.path.exists(config_path):
    try:
        with open(os.path.join(config_path, 'psw.json'), 'r', encoding='utf-8') as f:
            psw_list = loads(f.read())
    except Exception as e:
        print(e)


class Window2(QWidget, Ui_password_manage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        os.chdir(application_path)
        self.setWindowIcon(QIcon('./assets/password.png'))
        self.setFixedSize(600, 400)
        # 小部件设置
        self.ImageLabel.setImage('./assets/password.png')
        self.ImageLabel.setFixedSize(100, 100)
        self.ToolButton.setIcon(FluentIcon.SEARCH)
        self.ToolButton.setFixedWidth(80)
        self.ToolButton.setIconSize(QSize(30, 20))
        self.LineEdit.setClearButtonEnabled(True)
        self.LineEdit_2.setClearButtonEnabled(True)
        self.LineEdit_3.setClearButtonEnabled(True)
        self.LineEdit_4.setClearButtonEnabled(True)
        self.PushButton.setIcon(QIcon('./assets/gen.svg'))
        self.save_btn.setIcon(FluentIcon.SAVE)
        self.show_btn.setIcon(FluentIcon.SHARE)
        # 信号和槽
        self.PushButton.clicked.connect(self.setPassword)
        self.save_btn.clicked.connect(self.save_password)
        self.show()

    def show_info(self, content='', title='', parent=None, success=True):
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
            duration=2000 if success else -1,
            parent=parent or self,
            position=InfoBarPosition.TOP
        )
        self.info.show()

    def setPassword(self):
        password = generate_password()
        self.LineEdit_3.setText(password)
        self.show_info(title='密码生成成功', content=password)

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
                    psw_list[i] = psw_dict
                    return True
                else:
                    self.show_info(
                        title='错误', content='标记已存在', success=False)
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
        password = self.LineEdit_4.text()
        url = self.LineEdit_3.text() if self.LineEdit_3.text() else ''
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
