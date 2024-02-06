from PyQt6.QtWidgets import QApplication, QWidget
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        print("__init__", self.__repr__())
        self.setGeometry(600, 300, 800, 350)

    def show(self):
        print(self.__str__())
        super().show()


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
