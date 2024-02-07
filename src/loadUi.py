from PyQt6.QtWidgets import QApplication, QWidget
import sys
from PyQt6 import uic


class UI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("w1.ui", self)
        self.show()


app = QApplication(sys.argv)
window = UI()
sys.exit(app.exec())
