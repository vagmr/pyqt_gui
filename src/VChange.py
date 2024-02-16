from PyQt6.QtWidgets import (QApplication, QWidget, QFileDialog)
from ui.ui_VChange import Ui_changeTool
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor
from qfluentwidgets.components.widgets.acrylic_label import AcrylicLabel
from qfluentwidgets import (InfoBar, InfoBarIcon, InfoBarPosition,
                            FluentIcon, MessageBox, StateToolTip)
from PIL import Image
import subprocess
import sys
from os import remove


class Window(QWidget, Ui_changeTool):
    def __init__(self):
        super().__init__()
        self.background_label = AcrylicLabel(
            blurRadius=25, tintColor=QColor(255, 255, 255, 62), parent=self)
        self.background_label.setImage("../img/author.jpg")
        self.background_label.resize(self.size())
        self.setupUi(self)
        # 窗口设置
        self.setFixedSize(600, 400)
        self.setWindowIcon(QIcon("../img/change.svg"))
        self.HyperlinkButton.setIcon(FluentIcon.GITHUB)
        self.SwitchButton.setFixedWidth(80)

        self.stateTip = None
        # 标记变量
        self.isVideo = False
        self.img_format = ['png', 'jpg', 'jpeg', 'bmp']
        self.update_file_filter()
        # 部件设置
        self.formatSelect.addItems(self.img_format)
        self.formatSelect.setCurrentIndex(0)
        # 信号槽
        self.PushButton.clicked.connect(self.select_input_file)
        self.PushButton_2.clicked.connect(self.select_output_file)
        self.PrimaryPushButton.clicked.connect(self.file_change)
        self.formatSelect.currentIndexChanged.connect(self.change_img_format)
        self.SwitchButton.checkedChanged.connect(self.change_isVideo)
        self.show()

    def show_info(self, content='', title='', parent=None, success=True):
        self.info = InfoBar.new(
            icon=InfoBarIcon.SUCCESS if success else InfoBarIcon.ERROR,
            title=title,
            content=content,
            isClosable=True,
            duration=2000 if success else -1,
            parent=parent or self,
            position=InfoBarPosition.TOP_RIGHT
        )
        self.info.show()

    def update_file_filter(self):
        self.input_video_filter = "视频文件(*.ts *.avi *.mkv);;所有文件(*)"
        self.output_video_filter = "视频文件(*.mp4);;所有文件(*)"
        self.input_image_filter = "图片文件(*.webp *.jfif *.bmp);;所有文件(*)"
        self.output_image_filter = "图片文件(*.png);;所有文件(*)"
        self.refresh_filter()

    def refresh_filter(self):
        self.input_file_filter = self.input_video_filter if self.isVideo \
            else self.input_image_filter
        self.output_file_filter = self.output_video_filter if self.isVideo \
            else self.output_image_filter

    def change_img_format(self):
        self.output_image_filter = "图片文件(*." + \
            self.formatSelect.currentText() + ");;所有文件(*)"
        self.refresh_filter()
        if self.LineEdit_2.text():
            self.LineEdit_2.setText(self.LineEdit_2.text().split(
                ".")[0] + "." + self.formatSelect.currentText())
        self.show_info(content="格式更改成功")

    def select_input_file(self):
        file = QFileDialog.getOpenFileName(
            self, "选择输入文件", "", self.input_file_filter
        )
        if file[0]:
            self.LineEdit.setText(file[0])
        else:
            self.show_info(
                content="未选择文件",
                title="错误",
                success=False
            )

    def select_output_file(self):
        defaultFileName = self.LineEdit.text().split("/")[-1].split(".")[0]
        file = QFileDialog.getSaveFileName(
            self, "输出文件", defaultFileName, self.output_file_filter
        )
        if file[0]:
            self.LineEdit_2.setText(file[0])
        else:
            self.show_info(
                content="未选择文件",
                title="错误",
                success=False
            )

    def image_change(self):
        try:
            with Image.open(self.LineEdit.text()) as img:
                input_format = img.format.upper() if img.format else None
                target_format = self.formatSelect.currentText().upper()
                if target_format == 'JPG':
                    target_format = 'JPEG'
                if input_format == target_format:
                    img.save(self.LineEdit_2.text())
                    self.show_info(
                        content="转换成功",
                        title="成功",
                        success=True
                    )
                else:
                    img.convert(mode='RGBA').save(
                        fp=self.LineEdit_2.text(), format=self.formatSelect.currentText())
            log_text = (
                f'<font color="green">【Log】执行成功，转换格式：{self.formatSelect.currentText()}, ' +
                f'保存路径：{self.LineEdit_2.text()}</font><br>'
            )
            self.TextEdit.insertHtml(log_text)

        except Exception as e:
            # 添加错误信息（失败）
            error_text = (
                f'<font color="red">【Error】输入文件{self.LineEdit.text()} 输出文件{self.LineEdit_2.text()} 错误：{e}</font><br>'
            )
            self.TextEdit.append(error_text)
            self.show_info(
                content=f"错误",
                title="错误",
                success=False
            )

    def is_delete(self):
        dialog = MessageBox(title="提示", parent=self, content="是否删除原文件?")
        if dialog.exec():
            return True
        return False

    def show_tip(self):
        if not self.stateTip:
            self.stateTip = StateToolTip(
                title="正在转换中", content='请稍后', parent=self)
            self.stateTip.move(340, 0)
            self.stateTip.setState(False)
            self.stateTip.show()
        else:
            self.stateTip.setContent('视频转换完成啦 😆')
            self.stateTip.setState(True)
            self.stateTip = None

    def video_change(self):
        try:
            input_file = self.LineEdit.text()
            output_file = self.LineEdit_2.text()
            # FFmpeg 命令
            ffmpeg_command = f'ffmpeg -i "{input_file}" -c:v copy -c:a copy "{output_file}"'
            # 调用 FFmpeg 命令
            subprocess.run(
                ffmpeg_command, shell=True, check=True)
            # out_log = process.stdout.decode('utf-8')
            # self.TextEdit.append(out_log)
            # 添加成功日志信息
            log_text = (
                f'<font color="green">【Log】视频转换成功，保存路径：{output_file}</font><br>'
            )
            self.TextEdit.insertHtml(log_text)
            self.show_tip()

            if self.is_delete():
                print(input_file)
                remove(input_file)
                self.show_info(
                    content="删除成功"
                )

        except subprocess.CalledProcessError as e:
            # 添加错误日志信息
            error_text = (
                f'<font color="red">【Error】视频转换失败：{e}</font><br>'
            )
            self.TextEdit.insertHtml(error_text)

    def change_isVideo(self):
        self.isVideo = not self.isVideo
        log_text = (
            f'<font color="green">【Log】是否为视频模式：{self.isVideo}</font><br>'
        )
        self.TextEdit.insertHtml(log_text)
        if self.isVideo:
            self.formatSelect.setEnabled(False)
        else:
            self.formatSelect.setEnabled(True)
        self.update_file_filter()

    def file_change(self):
        if not self.LineEdit.text() or not self.LineEdit_2.text():
            self.show_info(
                content="未选择文件",
                title="错误",
                success=False
            )
            return
        if self.isVideo:
            self.show_tip()
            self.video_change()
        else:
            self.image_change()


app = QApplication(sys.argv)
w = Window()

sys.exit(app.exec())
