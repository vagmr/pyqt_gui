from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QSlider
from PyQt6.QtGui import QIcon, QDesktopServices
from PyQt6.QtCore import QUrl
from qfluentwidgets import (InfoBar, InfoBarIcon, InfoBarPosition, MessageBox)
from ui.ui_m3u8_dl import Ui_MainUi
from os import makedirs, path
from string import ascii_letters, digits
from random import choices
from datetime import datetime
import subprocess
import sys


application_path = ''
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    application_path = sys._MEIPASS  # type: ignore
else:
    application_path = path.dirname(path.abspath(__file__))


class M3u8DownloadGui(QWidget, Ui_MainUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__init__download_dir()
        self._init_window()
        self._init_variables()
        self._init_output_name()
        self.signalToSlot()

    # 初始化主要的变量
    def _init_variables(self):

        self.download_url = ""
        self.output_name = ""
        self.download_threads = 6
        self.CaptionLabel_2.setText(
            str(self.download_threads)
        )

    # 初始化窗口
    def _init_window(self):
        self.setWindowIcon(QIcon("../assets/1.ico"))
        self.LineEdit_3.setClearButtonEnabled(True)
        self.Slider.setMinimum(3)
        self.Slider.setMaximum(16)
        self.Slider.setValue(6)
        self.Slider.setTickInterval(1)
        self.Slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        # self.setFixedSize(665, 400)

    # 初始化下载目录
    def __init__download_dir(self):
        self.output_path = path.join(application_path, 'download')
        if not path.exists(self.output_path):
            makedirs(path.join(application_path, 'download'))
        self.LineEdit_2.setText(self.output_path)

    def show_info(self, content='', title='', parent=None, success=True, duration=2000):
        """
        显示信息栏，包含指定的内容、标题、父级和成功状态。

        :param content: 信息栏要显示的内容（默认为空字符串）
        :param title: 信息栏的标题（默认为空字符串）
        :param parent: 信息栏的父级组件（默认为None）
        :param success: 布尔值，指示信息栏应该显示成功还是错误图标（默认为True）
        """
        self.info = InfoBar.new(
            icon=InfoBarIcon.SUCCESS if success else InfoBarIcon.ERROR,
            title=title,
            content=content,
            isClosable=True,
            duration=duration,
            parent=parent or self,
            position=InfoBarPosition.TOP
        )
        self.info.show()

    def is_confirm(self, content="是否删除原文件?"):
        dialog = MessageBox(title="提示", parent=self, content=content)
        if dialog.exec():
            return True
        return False

    def select_output_path(self):
        path_dir = QFileDialog.getExistingDirectory(self, "选取文件夹", self.output_path
                                                    )
        if path_dir:
            self.output_path = path_dir
            self.LineEdit_2.setText(self.output_path)
            self.show_info(
                content=f"下载目录已设置为：{self.output_path}", parent=self, success=True)

    def random_output_name(self, length=6):
        """
        生成随机的输出文件名


        :param length: 输出文件名的长度（默认6）
        :return: 随机的输出文件名
        """
        random_str = ''.join(choices(ascii_letters + digits, k=length))
        date_str = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"{date_str}_{random_str}.mp4"

    def _init_output_name(self):
        """
        初始化输出文件名


        """
        self.output_name = self.random_output_name()
        self.LineEdit_3.setText(self.output_name)

    def change_download_threads(self):
        self.download_threads = self.Slider.value()
        self.CaptionLabel_2.setText(f"{self.download_threads}")

    def download_video(self):
        """下载主函数

        """
        if self.LineEdit.text() == "":
            self.show_info(content="下载链接不能为空", parent=self,
                           success=False, duration=3000)
            return
        self.download_url = self.LineEdit.text()
        self.output_name = self.LineEdit_3.text()

        if not self.output_path or not self.output_name:
            self.show_info(
                content="请检查下载目录和文件名是否正确",
                parent=self,
                success=False,
            )
            return
        print("开始下载")
        exc_path = path.join(application_path, 'lib/m3u8Lib.exe')
        download_cmd = f" {exc_path} {self.download_url}   --save-dir {self.output_path} --save-name {self.output_name}  --thread-count {self.download_threads}"
        try:
            subprocess.run(download_cmd, shell=True, check=True)
            self.show_info(
                content=f"下载成功，文件保存至：{self.output_path}",
                parent=self,
                success=True)
            if self.is_confirm(content="是否打开下载目录?"):
                QDesktopServices.openUrl(QUrl.fromLocalFile(self.output_path))

        except subprocess.CalledProcessError as e:
            self.show_info(
                content=f"下载失败，错误信息：{e.stderr.decode()}",
                parent=self,
                success=False,
                duration=3000,
            )
            return

    def signalToSlot(self):
        """ 信号与槽的绑定

        """
        self.PushButton.clicked.connect(self.select_output_path)
        self.Slider.valueChanged.connect(self.change_download_threads)
        self.PrimaryPushButton.clicked.connect(self.download_video)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = M3u8DownloadGui()
    w.show()
    sys.exit(app.exec())
