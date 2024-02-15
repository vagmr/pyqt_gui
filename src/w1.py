from PyQt6.QtWidgets import QApplication, QWidget
from ui_w1 import Ui_window


class W1(QWidget, Ui_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    w = W1()
    app.exec()
