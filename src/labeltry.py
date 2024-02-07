from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMenu
import sys
from PyQt6.QtCore import QRect, QSize
import warnings
from qfluentwidgets import FlowLayout, FlyoutView, FluentIcon, PrimaryPushButton, CardWidget, RoundMenu

warnings.filterwarnings("ignore", category=DeprecationWarning)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("label try")
        self.setGeometry(QRect(600, 300, 800, 350))
        self.label1 = QLabel(self)
        self.label1.setText("hello world")
        self.label1.move(5,0)
        self.label1.setFont(QFont('宋体', 20))
        self.create_button()

    def create_button(self):
        sbtn = QPushButton('click', self)
        sbtn.setGeometry(100, 100, 100, 100)
        sbtn.setFont(QFont('Arial', 20))
        sbtn.setIcon(FluentIcon.BACKGROUND_FILL.qicon())
        sbtn.setIconSize(QSize(30, 50))
        sbtn.move(10, 100)
        menu = QMenu()
        menu.addAction(FluentIcon.COPY.qicon(), 'copy')
        menu.addAction(FluentIcon.PASTE.qicon(), 'paste')
        sbtn.setMenu(menu)


app = QApplication(sys.argv)
w = Window()
f = FlyoutView(
    title="笨蛋陌猪",
    content="如你所见这是一个笨蛋",
    icon=FluentIcon.ACCEPT,
    image=QPixmap('../img/cs.png')
)
f2 = FlyoutView(
    title="另一个弹出组件",
    content="这是一个另一个弹出组件",
    icon=FluentIcon.ACCEPT_MEDIUM,
    isClosable=True,
)
card = CardWidget()
card.setStyleSheet("background-color: #ff0000;")
card.setWindowIcon(FluentIcon.ALBUM.qicon())
layout = FlowLayout(parent=card)
layout.addWidget(f)
layout.addWidget(f2)
btn = PrimaryPushButton(icon=FluentIcon.ADD_TO, text="click me", parent=w)
btn.setFixedSize(200, 100)
btn.clicked.connect(lambda: card.show())
btn.move(200, 100)
w.show()
sys.exit(app.exec())
