from PyQt6.QtWidgets import QApplication, QWidget
from ui.ui_loginPage import Ui_login
from requests import get, post
from qfluentwidgets import InfoBar, InfoBarIcon, InfoBarPosition
import json

BASEURL = "https://vagmr.pythonanywhere.com/user/"


class Login(QWidget, Ui_login):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.__init_widget()
        self._signalToSlot()
        self.show()

    def __init_widget(self):
        self.ImageLabel.setImage("./assets/s1.png")
        self.ImageLabel.setFixedWidth(300)

    def _signalToSlot(self):
        self.PrimaryPushButton.clicked.connect(self.login)

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
            duration=duration,
            parent=parent or self,
            position=InfoBarPosition.TOP
        )
        self.info.show()

    def login(self):
        username = self.LineEdit_2.text()
        password = self.LineEdit.text()
        if not username or not password:
            self.show_info("用户名或密码不能为空", "错误", success=False, duration=5000)
            return
        data = {"username": username, "password": password}
        print(data)
        try:
            res = post(BASEURL + "login", json=data)
            res.raise_for_status()
            if res.status_code == 200:
                try:
                    response_data = res.json()
                    print(response_data)
                except json.decoder.JSONDecodeError:
                    self.show_info("无法解析服务器响应", "错误",
                                   success=False, duration=5000)
        except Exception as e:
            print(e)
            self.show_info(str(e), "错误", success=False, duration=5000)


if __name__ == "__main__":
    app = QApplication([])
    w = Login()
    app.exec()
