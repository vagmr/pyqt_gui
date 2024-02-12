"""
@文件        :pswManage_demo.py
@说明        :只是一点尝试，我打算用PyQt重写我之前用tkinter做的应用
@时间        :2024/02/12 20:26:16
@作者        :vagmr
@版本        :1.1
"""


from PyQt6.QtWidgets import QWidget, QApplication, QGridLayout, QTableWidgetItem
import sys
from qfluentwidgets import CardWidget, TitleLabel
from ui.ui_showInfo import Ui_table


class Window(QWidget, Ui_table):
    def __init__(self):
        super().__init__()
        self.card = CardWidget()
        self.setupUi(self.card)
        grid = QGridLayout()
        title = TitleLabel('密码管理器')
        self.TableWidget.setRowCount(3)
        self.TableWidget.setColumnCount(3)
        self.TableWidget.setItem(0, 0, QTableWidgetItem("用户名"))
        self.TableWidget.setItem(0, 1, QTableWidgetItem('密码'))
        self.TableWidget.setItem(0, 2, QTableWidgetItem('邮箱'))
        grid.addWidget(title, 0, 0)
        grid.addWidget(self.card, 1, 0)
        self.setLayout(grid)
        self.show()


app = QApplication(sys.argv)
w = Window()

sys.exit(app.exec())
