from PyQt6.QtWidgets import QApplication, QWidget
import sys
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
from ui_w1 import Ui_window


class Window(QWidget, Ui_window):
    def __init__(self):
        super().__init__()
        print("__init__", self.__repr__())
        self.setupUi(self)
        self.setGeometry(600, 300, 730, 400)
        self.setWindowTitle("python Gui Dev")
        self.setWindowIcon(QIcon("../img/1.ico"))
        self.setFixedHeight(400)
        self.setFixedWidth(730)
        self.show()


app = QApplication(sys.argv)
window = Window()
if sys.flags.interactive != 1 or not hasattr(QtCore, "PYQT_VERSION"):
    sys.exit(app.exec())
