from PyQt6.QtWidgets import QApplication, QWidget
from ui_login import Ui_cardWin
import sys


class Window(QWidget, Ui_cardWin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()


app = QApplication(sys.argv)
w = Window()


sys.exit(app.exec())
