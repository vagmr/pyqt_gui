from PyQt6.QtWidgets import QApplication
from qfluentwidgets import SplitFluentWindow
from calculate import CalculateWindow
from w1 import W1


class Window(SplitFluentWindow):
    def __init__(self):
        super().__init__()
        self.addSubInterface(icon="../img/c.svg",
                             interface=CalculateWindow(), text="计算器")
        self.addSubInterface(icon="../img/l.svg",
                             interface=W1(), text="列表")
        self.show()


app = QApplication([])
w = Window()
app.exec()
