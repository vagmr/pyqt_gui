from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import SplitFluentWindow, FluentIcon, NavigationItemPosition
from VChange import Window
from VPsw import Window2
from settings import SettingInterface
from loginPage import Login
from sys import exit, argv


class MainWindow(SplitFluentWindow):
    def __init__(self):
        super().__init__()
        self.window_interface = Window2(self)
        self.navigationInterface.setAcrylicEnabled(True)
        self.setting = SettingInterface(self)
        self.change_tool = Window(self)
        self.loginPage = Login(parent=self)
        self.init_window()
        self.init_navigation()
        self.show()

    def init_navigation(self):
        self.addSubInterface(
            self.change_tool, icon=FluentIcon.CHAT, text="视频转换")
        self.addSubInterface(
            self.window_interface, icon=FluentIcon.PLAY_SOLID, text="密码管理")
        s1 = self.addSubInterface(self.loginPage, icon="./assets/login.svg",
                                  text="登录")
        self.addSubInterface(self.setting, icon=FluentIcon.SETTING,
                             text="设置", position=NavigationItemPosition.BOTTOM)

        from settings import userInfo
        userInfo.clicked.connect(lambda: s1.click())

    def init_window(self):
        self.setFixedSize(665, 400)
        self.setWindowTitle("VApplication")
        self.setWindowIcon(QIcon("./assets/1.ico"))


if __name__ == "__main__":
    app = QApplication(argv)
    window = MainWindow()
    exit(app.exec())
