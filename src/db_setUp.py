from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from ui.ui_DbDemo import Ui_ui_Db
import mysql.connector as ms


class Window(QWidget, Ui_ui_Db):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.HostEdit.setText('127.0.0.1')
        self.usernameEdit.setText('root')
        self.DbNameEdit.setPlaceholderText('请输入要创建的数据库名称')
        self.data_base = None
        self.signalToSlot()
        self.show()

    def signalToSlot(self):
        #  创建数据库
        self.createBtn.clicked.connect(self.create_database)
        self.conBtn.clicked.connect(self.connect_database)

    def create_database(self):
        try:
            db = ms.connect(
                host=self.HostEdit.text(),
                user=self.usernameEdit.text(),
                password=self.passwordEdit.text()
            )
            cursor = db.cursor()
            dbname = self.DbNameEdit.text()
            cursor.execute(
                f'CREATE DATABASE if not exists {dbname} CHARACTER SET utf8mb4;')
            self.label.setText(f'数据库 {dbname} 创建成功')
        except ms.Error as e:
            self.PlainTextEdit.setPlainText(f'数据库连接失败: {e}')

    def connect_database(self):
        self.PlainTextEdit.appendPlainText("正在连接数据库...")
        try:
            my_db = ms.connect(
                host=self.HostEdit.text(),
                user=self.usernameEdit.text(),
                password=self.passwordEdit.text(),
                database=self.DbNameEdit.text()
            )
            self.data_base = my_db
            self.PlainTextEdit.appendPlainText(
                f'数据库 {self.DbNameEdit.text()} 连接成功')
        except ms.Error as e:
            self.PlainTextEdit.setPlainText(
                f'数据库{self.DbNameEdit.text()}连接失败: {e}')


app = QApplication([])
w = Window()
app.exec()
