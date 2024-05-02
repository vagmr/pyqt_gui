from email import message
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QSlider
from PyQt6.QtGui import QIcon, QDesktopServices
from PyQt6.QtCore import QUrl, QTimer, QThread, pyqtSignal
from qfluentwidgets import (InfoBar, InfoBarIcon, InfoBarPosition, MessageBox)
from ui.ui_m3u8_dl import Ui_MainUi
from os import makedirs, path
from string import ascii_letters, digits
from random import choices
from datetime import datetime
import subprocess
import sys
import configparser


application_path = ''
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    application_path = sys._MEIPASS  # type: ignore
    config_save_path = path.dirname(sys.executable)
else:
    application_path = path.dirname(path.abspath(__file__))
    config_save_path = application_path


class DownloadThread(QThread):
    """
    下载线程类 DownloadThread
    DownloadThread 是一个继承自 QThread 的类，用于处理下载任务。
    它有两个信号，finished 和 error，分别在下载完成和出现错误时发出。

    方法
    - __init__(self, download_cmd): 构造函数，接受一个 download_cmd 参数，用于指定下载命令。
    - run(self): 重写了 QThread 的 run 方法。它运行 download_cmd 命令，使用 subprocess.run() 函数。
    如果命令成功运行，它会发出 finished 信号，并传递字符串 "下载完成"。
    如果命令运行失败，它会发出 error 信号，并传递 CalledProcessError 异常。
    """
    finished = pyqtSignal(str)
    error = pyqtSignal(Exception)

    def __init__(self, download_cmd):
        super().__init__()
        self.download_cmd = download_cmd

    def run(self):
        try:
            subprocess.run(self.download_cmd, shell=True, check=True)
            self.finished.emit("下载完成")
        except subprocess.CalledProcessError as e:
            self.error.emit(e)


class M3u8DownloadGui(QWidget, Ui_MainUi):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self._init_variables()
        self._init_window()
        self.read_config()
        self._init_output_name()
        self.signalToSlot()

    # 初始化主要的变量
    def _init_variables(self):

        self.download_url = ""
        self.output_name = ""
        self.output_path = ""
        self.download_threads = 6
        self.CaptionLabel_2.setText(
            str(self.download_threads)
        )
        self.config = configparser.ConfigParser()

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现窗口关闭时执行一些操作
        如果保存路径发生变化，则保存路径信息到配置文件中
        """
        config_file = path.join(config_save_path, 'settings.ini')
        self.config.read(config_file)
        old_output_path = self.config.get(
            section="Settings", option="output_path")
        if old_output_path != self.output_path:
            if self.is_confirm(content="检测到下载目录发生变化，是否保存?"):
                self.write_config()
        event.accept()

    def read_config(self):
        """
        读取配置文件中的下载目录信息，并设置到文本框中
        如果不存在配置文件，则创建配置文件
        """
        config_file = path.join(config_save_path, 'settings.ini')
        if path.exists(config_file):
            self.config.read(config_file)
            self.output_path = self.config.get(
                'Settings', 'output_path', fallback=self.output_path)
            self.LineEdit_2.setText(self.output_path)
        else:
            self.__init__download_dir()
            self.write_config()

    def write_config(self):
        """
        保存下载目录信息到配置文件中
        """

        self.config['Settings'] = {'output_path': self.output_path}
        config_file = path.join(config_save_path, 'settings.ini')
        with open(config_file, 'w') as f:
            self.config.write(f)

    # 初始化窗口

    def _init_window(self):
        self.setWindowIcon(QIcon("../assets/1.ico"))
        self.setFixedSize(600, 400)
        self.LineEdit_3.setClearButtonEnabled(True)
        self.Slider.setMinimum(3)
        self.Slider.setMaximum(16)
        self.Slider.setValue(6)
        self.Slider.setTickInterval(1)
        self.Slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        # self.setFixedSize(665, 400)

    # 初始化下载目录
    def __init__download_dir(self):
        print("初始化下载目录")
        self.output_path = path.join(config_save_path, 'download')
        if not path.exists(self.output_path):
            makedirs(path.join(config_save_path, 'download'))
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

        self.show_info(
            content=f"开始下载,线程数{self.download_threads}，请查看控制台输出", parent=self, success=True)

        exc_path = path.join(application_path, 'lib/m3u8Lib.exe')
        download_cmd = f'{exc_path} "{self.download_url}" --save-dir "{self.output_path}" --save-name {self.output_name} --thread-count {self.download_threads}'

        message = f"下载完成, 文件路径：{self.output_path}"
        self.download_thread = DownloadThread(download_cmd)
        self.download_thread.finished.connect(
            lambda: self.on_download_finished(message))
        self.download_thread.error.connect(self.on_download_error)
        self.download_thread.start()

    def on_download_finished(self, message):
        print(message)
        if self.is_confirm(content="是否打开下载目录?"):
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.output_path))

    def on_download_error(self, exception):
        self.show_info(content=f"下载失败，错误信息：{exception.stderr.decode()}",
                       parent=self, success=False, duration=3000)

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
