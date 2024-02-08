from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGridLayout
from PyQt6.QtCore import QSize, QPoint
from PyQt6.QtGui import QFont
from qfluentwidgets import (PrimaryPushButton, FlowLayout, ToolButton,
                            TransparentPushButton, TogglePushButton, FluentIcon,
                            ComboBox, EditableComboBox, IconWidget, HyperlinkLabel)


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QHBoxLayout()
        btn1 = QPushButton("btn1")
        btn2 = QPushButton("btn2")
        btn3 = QPushButton("btn3")
        btn4 = QPushButton("btn4")
        btn5 = QPushButton("click me", self)
        btn6 = PrimaryPushButton("click me", self)
        btn7 = ToolButton(FluentIcon.ADD_TO, parent=self)
        btn5.setBaseSize(QSize(50, 30))
        btn6.setBaseSize(QSize(50, 30))
        btn7.setBaseSize(QSize(50, 30))
        btn5.move(QPoint(100, 100))
        btn6.move(QPoint(220, 100))
        btn7.move(QPoint(330, 100))
        btn5.setFont(QFont("Arial", 20))
        btn6.setFont(QFont("Arial", 20))
        btn7.setFont(QFont("Arial", 20))
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)
        layout.addWidget(btn4)
        btn5.clicked.connect(lambda: self.setLayout(layout))
        btn6.clicked.connect(self.showSubWindow)
        btn7.clicked.connect(self.showthreeWindow)

    def showSubWindow(self):
        self.sub_window = subWindow()
        self.sub_window.show()

    def showthreeWindow(self):
        self.three_window = threeWindow()
        self.three_window.show()


class subWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = FlowLayout()
        btn1 = PrimaryPushButton("close window")
        btn2 = PrimaryPushButton("btn2")
        btn3 = TransparentPushButton("btn3")
        btn4 = TogglePushButton("btn4")
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)
        layout.addWidget(btn4)
        self.setLayout(layout)
        btn1.clicked.connect(lambda: self.close())  # type: ignore


class threeWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        c1 = ComboBox()
        c2 = EditableComboBox()
        c3 = IconWidget(FluentIcon.BROOM)
        c4 = HyperlinkLabel("link")
        layout.addWidget(c1, 0, 0)
        layout.addWidget(c2, 0, 1)
        layout.addWidget(c3, 1, 0, 1, 2)
        layout.addWidget(c4, 2, 0, 1, 2)
        self.setLayout(layout)


app = QApplication([])
w = Window()
w.show()
app.exec()
