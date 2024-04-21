from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel
from PySide6.QtGui import QIcon, QMouseEvent, QTextDocument, QPainter, QPen, QBrush
from PySide6.QtCore import Qt, QRectF

import sys


class DrawWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._init_window()
        self.setMouseTracking(True)
        self.show()

    def _init_window(self):
        self.setFixedSize(600, 500)
        self.setWindowTitle("Qt 绘制")
        self.setWindowIcon(QIcon("../img/author.jpg"))
        self.vLayout = QVBoxLayout()
        self.setLayout(self.vLayout)
        self.label = QLabel()
        self.vLayout.addWidget(self.label)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        rect = QRectF(0, 0, 400, 100)
        document = QTextDocument()
        document.setTextWidth(rect.width())
        document.setHtml(
            "<h1>PyQt6 learn</h1> <b>窗口标题</b><i>vagmr studio</i><font size='10' color='red'>这是一个字体</font>")
        document.drawContents(painter, rect)

    def mouseMoveEvent(self, event) -> None:
        x = event.pos().x()
        y = event.pos().y()
        text = f"x:{x},y:{y}"
        self.label.setText(text)
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DrawWindow()
    sys.exit(app.exec())
