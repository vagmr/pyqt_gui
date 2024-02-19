from PyQt6.QtWidgets import QApplication
from qfluentwidgets import SplitFluentWindow, FluentIcon
from VChange import Window
from VPsw import Window2


class MainWindow(SplitFluentWindow):
    def __init__(self):
        super().__init__()
        self.window_interface = Window2(self)

        self.addSubInterface(Window(), icon=FluentIcon.CHAT, text="视频转换")
        self.addSubInterface(
            self.window_interface, icon=FluentIcon.PLAY_SOLID, text="密码管理")
        self.setFixedSize(660, 400)
        self.navigationInterface.setAcrylicEnabled(True)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec()
