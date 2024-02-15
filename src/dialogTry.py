from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QInputDialog
from qfluentwidgets import Dialog, PushButton, MessageDialog, MessageBox
from customComponents import CusButton, VInputDialog


class Window(QWidget):
    def __init__(self):
        super().__init__()
        row = QHBoxLayout()
        self.btn1 = QPushButton('打开对话框')
        self.btn1.clicked.connect(self.showDialog)
        self.btn2 = CusButton(text="打开消息对话框")
        self.btn2.clicked.connect(self.showMessageDialog)
        self.btn3 = PushButton(text="打开消息对话框")
        self.btn3.clicked.connect(self.showMessageBox)
        self.btn4 = CusButton(text="打开输入对话框")
        self.btn4.clicked.connect(self.showInput)
        self.btn5 = CusButton()
        self.dialog = None
        self.btn5.setText('test')
        self.btn5.clicked.connect(self.show_input_dialog)
        row.addWidget(self.btn1)
        row.addWidget(self.btn2)
        row.addWidget(self.btn3)
        row.addWidget(self.btn4)
        row.addWidget(self.btn5)
        self.setLayout(row)
        self.show()

    def showDialog(self):
        dialog = Dialog(title='对话框', parent=self, content='测试内容')
        dialog.show()

    def showMessageDialog(self):
        dialog = MessageDialog(title='对话框', parent=self, content='测试内容')
        dialog.show()

    def showMessageBox(self):
        dialog = MessageBox(title='对话框', parent=self, content='测试内容')
        dialog.show()

    def showInput(self):
        self.dialog = VInputDialog(parent=self, title='对话框', items=[
            '1', '2', '3'], content='测试内容')
        self.dialog.show()
        if self.dialog.exec():
            print(self.dialog.getItem())

    def show_input_dialog(self):
        dialog, ok = QInputDialog.getInt(self, '输入对话框', '输入一个数字:')
        if ok:
            print(dialog)


app = QApplication([])
window = Window()
app.exec()
