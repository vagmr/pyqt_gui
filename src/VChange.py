"""
@文件        :VChange.py
@说明        :视频转换工具 
@时间        :2024/02/18 16:02:20
@作者        :vagmr
@版本        :1.1
"""


from PyQt6.QtWidgets import (QApplication, QWidget, QFileDialog)
from ui.ui_VChange import Ui_changeTool
from PyQt6.QtGui import QIcon, QDesktopServices
from PyQt6.QtCore import Qt, QTimer, QUrl
from qfluentwidgets import (
    InfoBar, InfoBarIcon, InfoBarPosition, MessageBox, StateToolTip,
    FlyoutView, Flyout, HyperlinkButton, FlyoutAnimationType, ImageLabel)
from PIL import Image
from subprocess import run, CalledProcessError
from json import loads, dumps
from os import makedirs, remove, path
from check_ffmpeg import is_ffmpeg_installed, download_ffmpeg
import sys

# 获取应用程序路径
application_path = ''
config_file_save_path = ""
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    application_path = sys._MEIPASS  # type: ignore
    config_file_save_path = path.dirname(sys.executable)
else:
    application_path = path.dirname(path.abspath(__file__))
    config_file_save_path = application_path

# 输入输出文件路径的默认值
select_input_path = application_path
select_output_path = application_path
# 读取保存文件路径
if path.exists(path.join(config_file_save_path, './history')):
    try:
        with open(path.join(config_file_save_path, './history/history.json'), 'r', encoding='utf-8') as f:
            history = loads(f.read())
            select_input_path = history['input']
            select_output_path = history['output']
        file_log = "【log】写入保存文件路径成功"
        print(file_log)
    except Exception as e:
        print(e)


class Window(QWidget, Ui_changeTool):
    def __init__(self, parent=None):
        """
        构造函数用于初始化类，包括设置用户界面、窗口属性、信号与槽的连接以及小部件配置。
        """
        super().__init__(parent=parent)
        # self.background_label = AcrylicLabel(
        #     blurRadius=25, tintColor=QColor(255, 255, 255, 62), parent=self)
        # self.background_label.setImage("../img/author.jpg")
        # self.background_label.setScaledContents(True)
        # self.background_label.resize(self.size())
        self.setupUi(self)
        # 窗口设置
        self.setFixedSize(600, 400)
        self.setWindowIcon(QIcon("../img/change.svg"))
        self.SwitchButton.setFixedWidth(80)
        self.ToolButton.setIcon("../img/about.svg")
        self.ToolButton.setFixedWidth(40)
        self.LineEdit.setClearButtonEnabled(True)
        self.LineEdit_2.setClearButtonEnabled(True)
        self._save_file_dir = False
        self.about = None
        self.stateTip = None
        # 标记变量
        self.isVideo = False
        self.img_format = ['png', 'jpg', 'jpeg', 'bmp', 'ico']
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
        self.ToolButton.clicked.connect(self.show_about)
        self.show()

    def show_info(self, content='', title='', parent=None, success=True):
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
            duration=2000 if success else -1,
            parent=parent or self,
            position=InfoBarPosition.TOP_RIGHT
        )
        self.info.show()

    def update_file_filter(self):
        """
        更新文件选择器的过滤器设置。

        设置输入视频、输出视频、输入图片和输出图片的文件过滤器。
        这些过滤器用于文件对话框中，以便用户可以选择相应类型的文件。
        """
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
        """
        更改输出图片的格式，并更新界面显示和日志。

        根据下拉选择框中选定的格式，更新输出文件的格式，并在界面上显示成功信息。
        同时在文本编辑框中插入格式更改的日志。
        """
        self.output_image_filter = "图片文件(*." + \
            self.formatSelect.currentText() + ");;所有文件(*)"
        self.refresh_filter()
        if self.LineEdit_2.text():
            self.LineEdit_2.setText(self.LineEdit_2.text().split(
                ".")[0] + "." + self.formatSelect.currentText())
            self.show_info(content="格式更改成功")
        change_log = (
            f'<font color="green">【Log】图片格式更改为：{self.formatSelect.currentText()}</font><br>'
        )
        self.TextEdit.insertHtml(change_log)

    def select_input_file(self):
        global select_input_path
        print(select_input_path)
        file = QFileDialog.getOpenFileName(
            self, "选择输入文件", select_input_path, self.input_file_filter
        )
        if file[0]:
            self.LineEdit.setText(file[0])
            # dir = file[0][:file[0].rindex("/")+1]
            fileDir = file[0][:file[0].index(file[0].split("/")[-1])]
            select_input_path = fileDir
            print(fileDir)
        else:
            self.show_info(
                content="未选择文件",
                title="错误",
                success=False
            )

    def select_output_file(self):
        global select_output_path
        defaultFileName = self.LineEdit.text().split("/")[-1].split(".")[0]
        file = QFileDialog.getSaveFileName(
            self, "输出文件", select_output_path + defaultFileName, self.output_file_filter
        )
        if file[0]:
            self.LineEdit_2.setText(file[0])
            file_dir = path.dirname(file[0])
            fileDir = file[0][:file[0].index(file[0].split("/")[-1])]
            select_output_path = fileDir
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

    def is_confirm(self, content="是否删除原文件?"):
        dialog = MessageBox(title="提示", parent=self, content=content)
        if dialog.exec():
            return True
        return False

    def show_tip(self):
        if not self.stateTip:
            self.stateTip = StateToolTip(
                title="正在转换中", content='请稍后', parent=self)
            self.stateTip.move(340, 0)
            self.stateTip.animation.setDuration(1000)
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
            run(
                ffmpeg_command, shell=True, check=True)
            # out_log = process.stdout.decode('utf-8')
            # self.TextEdit.append(out_log)
            # 添加成功日志信息
            log_text = (
                f'<font color="green">【Log】视频转换成功，保存路径：{output_file}</font><br>'
            )
            self.TextEdit.insertHtml(log_text)
            self.show_tip()

            if self.is_confirm():
                print(input_file)
                remove(input_file)
                self.show_info(
                    content="删除成功"
                )

        except CalledProcessError as e:
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
            self.check_ffmpeg_dependency()
            self.formatSelect.setEnabled(False)
        else:
            self.formatSelect.setEnabled(True)
        self.update_file_filter()

    def check_ffmpeg_dependency(self):
        """
    检查ffmpeg依赖并提示用户如何安装
    """
        self.show_info(content="开始检测ffmpeg依赖")
        if not is_ffmpeg_installed():
            message_box = MessageBox(
                title="依赖缺失",
                content="ffmpeg被本应用的功能所依赖，但未安装。\n "
                        "是否进行自动安装?",
                parent=self,
            )
            if message_box.exec():
                try:
                    download_ffmpeg()
                except Exception as e:
                    self.TextEdit.append(
                        f'<font color="red">【Error】自动下载ffmpeg失败：{e}</font><br>'
                    )
            else:
                self.show_info(
                    content="未安装ffmpeg",
                    title="错误",
                    success=False
                )

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
            QTimer.singleShot(2000, self.video_change)
        else:
            self.image_change()
            file_dir = self.LineEdit_2.text(
            )[:self.LineEdit_2.text().rindex('/')+1]
            if self.is_confirm(content="是否打开文件所在文件夹?"):
                QDesktopServices.openUrl(QUrl.fromLocalFile(file_dir))

    def show_about(self):
        self.about = FlyoutView(
            title="关于",
            content="此应用由vagmr开发, 仅供学习使用,仅为本人学习PyQt6的练手项目",
            icon="../img/change.svg",
            isClosable=True,
            parent=self
        )
        self.about.contentLabel.setWordWrap(True)
        self.about.setFixedWidth(300)

        # 组件
        link = HyperlinkButton("https://github.com/vagmr",
                               "vagmr", None, "../img/github.svg")
        link.setFixedWidth(120)
        image = ImageLabel("../img/author.jpg")
        image.setFixedSize(200, 200)
        self.about.addWidget(image, align=Qt.AlignmentFlag.AlignCenter)
        self.about.addWidget(link, align=Qt.AlignmentFlag.AlignCenter)
        # 显示
        w = Flyout.make(self.about,
                        self.ToolButton, self,
                        aniType=FlyoutAnimationType.SLIDE_RIGHT)
        self.about.closed.connect(w.close)  # type:ignore

    def should_save_fileDir(self):
        if path.exists(path.join(config_file_save_path, './history')):  # type: ignore
            file_log = (
                f"【log】检测到已保存文件夹,input：{select_input_path}, output：{select_output_path} ")
            print(file_log)
            try:
                with open(path.join(config_file_save_path, './history/history.json'), 'r', encoding='utf-8') as f:
                    history = loads(f.read())
                    ex_select_input_path = history['input']
                    ex_select_output_path = history['output']
                if ex_select_input_path != select_input_path or ex_select_output_path != select_output_path:
                    return True
                else:
                    return False
            except Exception as e:
                print(e)
                return True
        else:
            if select_input_path != application_path or select_output_path != application_path:
                return True
            else:
                return False

    def save_fileDir(self):
        historyDir = path.join(config_file_save_path, './history')
        if not path.exists(historyDir):
            makedirs(historyDir)
        Dir = {
            'input': select_input_path,
            'output': select_output_path,
        }
        with open(path.join(historyDir, 'history.json'), 'w', encoding='utf-8') as f:
            f.write(dumps(Dir))

    def is_save_fileDir(self):
        if not self.should_save_fileDir():
            return
        if self.is_confirm(content="检测你切换了文件夹路径，是否保存文件夹路径?"):
            self.save_fileDir()
        else:
            pass

    def closeEvent(self, event):
        self.is_save_fileDir()
        event.accept()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = Window()

    sys.exit(app.exec())
