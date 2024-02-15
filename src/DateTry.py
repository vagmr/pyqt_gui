from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCalendarWidget
from qfluentwidgets import CardWidget, FlowLayout
from ui.ui_datepicker import Ui_Date
from customComponents.cusLabel import VTitleLabel
from customComponents import CusButton


class Window(QWidget, Ui_Date):
    def __init__(self):
        super().__init__()
        self.card = CardWidget()
        self.card2 = FlowLayout()
        self.setupUi(self.card)
        column = QVBoxLayout()
        title = VTitleLabel(text="vagmr的打卡软件")
        btn = CusButton(icon="../img/n.svg", text="下一个")
        title2 = VTitleLabel(text="第二个页面")
        cardw = QCalendarWidget()
        self.card2.addWidget(title2)
        self.card2.addWidget(cardw)
        row1 = QHBoxLayout()
        row1.addWidget(title)
        row2 = QHBoxLayout()
        row2.addWidget(btn)
        self.row3 = QHBoxLayout()
        self.row3.addWidget(self.card)
        column.addLayout(row1)
        column.addLayout(row2)
        column.addLayout(self.row3)
        btn.clicked.connect(self.change_view)
        self.setLayout(column)

    def change_view(self):
        self.card.close()
        self.row3.addLayout(self.card2)


app = QApplication([])
window = Window()
window.show()
app.exec()
