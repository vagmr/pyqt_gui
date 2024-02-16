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
        self.createBtn.clicked.connect(self.create_database)
        self.show()

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
        pass


app = QApplication([])
w = Window()
app.exec()
