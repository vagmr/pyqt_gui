from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QLabel,
                             QMessageBox, QFontDialog, QColorDialog, QGridLayout)
from dotenv import set_key
from customComponents import cusLessWidget
from ui.ui_vNotePad import Ui_MainWindow
from PyQt6.QtGui import QIcon, QFont
from resources import rc_image
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt6.QtCore import QFileInfo, Qt
import sys
from qfluentwidgets import FolderListDialog, InfoBar, InfoBarIcon, InfoBarPosition, TitleLabel


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("../img/app/icon.svg"))
        self.action.triggered.connect(self.select_folder)
        self.action_3.triggered.connect(self.save)
        self.action_2.triggered.connect(lambda: self.TextEdit.clear())
        self.actionNew.triggered.connect(self.file_new)
        self.actionOpen.triggered.connect(self.file_open)
        # 打印
        self.action_5.triggered.connect(self.file_print)
        # 打印预览
        self.action_6.triggered.connect(self.file_print_preview)
        self.action_PDF.triggered.connect(self.export_Pdf)
        self.action_8.triggered.connect(lambda: self.close())  # type:ignore
        # 编辑部分
        self.action_16.triggered.connect(self.TextEdit.undo)
        self.action_14.triggered.connect(self.TextEdit.redo)
        self.action_9.triggered.connect(self.TextEdit.cut)
        self.action_10.triggered.connect(self.TextEdit.copy)
        self.action_15.triggered.connect(self.TextEdit.paste)
        # 格式部分
        self.action_17.triggered.connect(self.font_bold)
        self.action_18.triggered.connect(self.font_italic)
        self.action_19.triggered.connect(self.font_underline)
        self.action_21.triggered.connect(
            lambda: self.TextEdit.setAlignment(Qt.AlignmentFlag.AlignLeft))
        self.action_22.triggered.connect(
            lambda: self.TextEdit.setAlignment(Qt.AlignmentFlag.AlignRight))
        self.action_23.triggered.connect(
            lambda: self.TextEdit.setAlignment(Qt.AlignmentFlag.AlignCenter))
        self.action_25.triggered.connect(self.choose_font)
        self.action_26.triggered.connect(self.change_color)
        self.action_27.triggered.connect(self.about)
        self.folder = ''
        self.show()

    def show_info(self, content='', title='', parent=None, success=True):
        self.info = InfoBar.new(
            icon=InfoBarIcon.SUCCESS if success else InfoBarIcon.ERROR,
            title=title,
            content=content,
            isClosable=True,
            duration=2000 if success else -1,
            parent=parent or self,
            position=InfoBarPosition.BOTTOM
        )
        self.info.show()

    def maybe_save(self):
        if self.TextEdit.document().isModified():
            warning = QMessageBox.warning(self, "警告", "文档已修改，是否保存",
                                          QMessageBox.StandardButton.Save
                                          | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,)
            if warning == QMessageBox.StandardButton.Save:
                self.save()
            elif warning == QMessageBox.StandardButton.Cancel:
                return False
            return True

    def select_folder(self):
        # 选择文件夹
        folder = FolderListDialog(
            folderPaths=[], title="选择文件夹", parent=self, content="请选择文件夹")
        folder.show()
        if folder.exec():
            pass
        else:
            self.folder = folder.folderPaths[0]
            self.show_info(content=f"已选择文件夹：{self.folder}")

    def save(self):
        # 保存文件
        filename = QFileDialog.getSaveFileName(
            self, "保存文件", filter="文本文件 (*.txt);;所有文件 (*)", directory=self.folder)
        if filename[0]:
            with open(filename[0], 'w', encoding='utf-8') as f:
                f.write(self.TextEdit.toPlainText())
            self.show_info(content="保存成功")

    def file_new(self):
        if not self.TextEdit.document().isModified():
            self.show_info(content="新建文件成功")
        elif self.maybe_save():
            self.TextEdit.clear()
            self.show_info(content="新建文件成功")

    def file_open(self):
        text = ''
        file = QFileDialog.getOpenFileName(
            self, "打开文件", self.folder, "文本文件 (*.txt);;所有文件 (*)")
        if file[0]:
            try:
                with open(file[0], 'r', encoding='utf-8') as f:
                    text = f.read()
            except UnicodeDecodeError:
                try:
                    with open(file[0], 'r', encoding='ISO-8859-1') as f:
                        text = f.read()
                except UnicodeDecodeError:
                    self.show_info(content="无法识别文件编码，打开失败", success=False)
                    return
        else:
            self.show_info(content="打开文件失败", success=False)
            return
        self.TextEdit.setText(text)
        self.show_info(content="打开文件成功")

    def file_print(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.TextEdit.print(printer)

    def file_print_preview(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setResolution(100)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(lambda p: self.TextEdit.print(p))
        previewDialog.exec()

    def export_Pdf(self):
        file, _ = QFileDialog.getSaveFileName(
            self, "导出为PDF", filter="PDF文件 (*.pdf);;所有文件 (*)", directory=self.folder
        )
        if file != '':
            if QFileInfo(file).suffix() == '':
                file += '.pdf'
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setResolution(50)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file)
            self.TextEdit.document().print(printer)
            self.show_info(content="导出pdf成功")

    def font_bold(self):
        font = self.TextEdit.currentFont()
        font.setBold(not font.bold())
        self.TextEdit.setFont(font)

    def font_italic(self):
        font = self.TextEdit.currentFont()
        font.setItalic(not font.italic())
        self.TextEdit.setFont(font)

    def font_underline(self):
        font = self.TextEdit.currentFont()
        font.setUnderline(not font.underline())
        self.TextEdit.setFont(font)

    def choose_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.TextEdit.setFont(font)

    def change_color(self):
        color = QColorDialog.getColor()
        self.TextEdit.setTextColor(color)

    def about(self):
        card = cusLessWidget()
        card.setHeader(title="关于")
        grid = QGridLayout()
        title = TitleLabel('VNotePad')
        text = "此应用由vagmr开发, 仅供学习使用,仅为本人学习PyQt6的练手项目"
        content = QLabel(text)
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content.setMaximumWidth(card.width())
        content.setWordWrap(True)  # 开启文本换行
        content.setFont(QFont("行楷", 18))
        grid.addWidget(title, 0, 0)
        grid.addWidget(content, 1, 0)
        card.addLayout(grid)
        card.show()


app = QApplication(sys.argv)
w = MainWindow()
sys.exit(app.exec())
