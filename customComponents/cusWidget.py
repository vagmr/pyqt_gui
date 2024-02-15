"""
@文件        :cusWidget.py
@说明        :自定义无边框窗口 
@时间        :2024/02/12 11:05:57
@作者        :vagmr
@版本        :1.1
"""


from cProfile import label
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QMouseEvent

from customComponents.cusButton import CusButton


class cusLessWidget(QWidget):
    """自定义无标题栏窗口

    该类继承自QWidget，实现了一个无标题栏窗口，支持拖动移动窗口。

    Attributes:
        drag_flag (bool): 标志，表示是否处于拖动窗口状态。
        drag_pos (QPoint): 存储拖动起始点的位置。

    Methods:
        - __init__(self, parent=None):
            构造方法，用于初始化无标题栏窗口。
            参数:
                - parent: QWidget，父级窗口，默认为None。
        - paintEvent(self, event):
            重写的绘制事件，用于绘制窗口的背景。
        - mousePressEvent(self, event: QMouseEvent):
            重写的鼠标按下事件，用于处理鼠标按下操作。
        - mouseMoveEvent(self, event: QMouseEvent):
            重写的鼠标移动事件，用于处理窗口的拖动。
        - mouseReleaseEvent(self, event: QMouseEvent):
            重写的鼠标释放事件，用于处理鼠标释放操作。
        - setHeader(self, title: str = "默认标题"):
            设置窗口的标题栏。
            参数:
                - title: str，窗口标题，默认为"默认标题"。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(300, 300, 400, 300)
        self.viewLayout = QVBoxLayout(self)
        self.viewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)  # 设置布局顶部对齐
        self.drag_flag = False
        self.drag_pos = QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.GlobalColor.white)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_flag = True
            self.drag_pos = event.globalPosition().toPoint() - self.pos()  # type: ignore

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drag_flag:
            self.move(event.globalPosition().toPoint() -
                      self.drag_pos)  # type: ignore

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_flag = False

    def setHeader(self, title: str = "默认标题"):
        title_style = """
        #title{
            font-size: 16px;
            font-weight: 500;
            font-family: "Microsoft YaHei";
            color: #000;
        }
        """
        self.header_row = QHBoxLayout()
        self.titleLabel = QLabel(title)
        self.titleLabel.setObjectName('title')
        self.titleLabel.setStyleSheet(title_style)
        self.close_btn = CusButton(icon='../img/close.svg')
        self.close_btn.setColor('white')
        self.header_row.addWidget(self.titleLabel)
        self.header_row.addWidget(self.close_btn)
        self.viewLayout.insertLayout(0, self.header_row)
        self.close_btn.clicked.connect(lambda: self.close())  # type: ignore
        self.close_btn.setFixedSize(20, 20)  # 设置关闭按钮的大小

    def addWidget(self, widget):
        row = QHBoxLayout()
        row.addWidget(widget)
        self.viewLayout.addLayout(row)

    def addLayout(self, layout):
        self.viewLayout.addLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    w = cusLessWidget()
    w.setHeader(title="自定义无边框窗口")
    w.show()
    app.exec()
