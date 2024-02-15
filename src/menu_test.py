from PyQt6.QtWidgets import (QApplication, QMenu,
                             QMenuBar, QMainWindow)
from PyQt6.QtGui import QAction
from qfluentwidgets import RoundMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)
        fileMenu = QMenu('File', parent=menubar)
        fileMenu.addAction(QAction('New', self))
        menubar.addAction(fileMenu.menuAction())
        editMenu = menubar.addMenu('Edit')
        editMenu.addAction(QAction('Copy', self))
        editMenu.addAction(QAction('Paste', self))
        editMenu.addAction(QAction('Cut', self))


app = QApplication([])
w = MainWindow()

w.show()
app.exec()
