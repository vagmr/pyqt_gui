from qfluentwidgets import (ScrollArea, ExpandLayout, SettingCardGroup, FolderListValidator,
                            FolderListSettingCard, PushSettingCard, ConfigItem, FolderValidator,
                            QConfig, FluentIcon as FIF, CardWidget,
                            HyperlinkCard, PrimaryPushSettingCard)
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtCore import QStandardPaths, Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from datetime import datetime
from ui.ui_helpCard import Ui_Form

now = datetime.now()
YEAR = now.year
AUTHOR = "vagmr"
MONTH = now.month
DAY = now.day
VERSION = "0.0.1"
userInfo = None


class Config(QConfig):
    musicFolders = ConfigItem(
        "Folders", "LocalMusic", [], FolderListValidator())
    downloadFolder = ConfigItem(
        "Folders", "Download", "assets/download", FolderValidator())


class SettingInterface(ScrollArea, Ui_Form):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        cfg = Config()
        self.setupUi(self)
        self.scrollWidget = CardWidget(self)
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.settingLabel = QLabel("设置", self)
        self.settingLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.settingLabel.setStyleSheet("font-size: 25px;")
        self.musicInThisPCGroup = SettingCardGroup(
            "本机音乐", self.scrollWidget)
        self.musicFolderCard = FolderListSettingCard(
            cfg.musicFolders,
            "本地音乐库",
            directory=QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.MusicLocation),
            parent=self.musicInThisPCGroup
        )
        self.downloadFolderCard = PushSettingCard(
            "选择下载文件夹",
            FIF.DOWNLOAD,
            "下载文件夹",
            cfg.get(cfg.downloadFolder),
            self.musicInThisPCGroup
        )
        # 关于
        self.aboutGroup = SettingCardGroup("关于", self.scrollWidget)
        self.help_card = HyperlinkCard(
            text="帮助项",
            icon=FIF.HELP,
            title="帮助",
            url='',
            content="此功能正在开发中",
            parent=self.aboutGroup
        )
        self.about = PrimaryPushSettingCard(
            title="关于",
            icon=FIF.INFO,
            text="关于",
            content=f"此应用由{AUTHOR}开发\n@{YEAR}-{MONTH}-{DAY}\n版本：{VERSION}",
            parent=self.aboutGroup
        )
        self.loginGroup = SettingCardGroup("登录", self.scrollWidget)
        self.userInfo = PrimaryPushSettingCard(
            title="跳转至登录页",
            icon=FIF.CARE_RIGHT_SOLID,
            text="登录(可选项)",
            content="登录后可将密码以加密形式保存至服务器",
            parent=self.loginGroup
        )

        self.__init_widget()

    def __init_widget(self):
        self.resize(660, 400)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 50, 0, 10)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        self._init_layout()
        self._init_connect()

    def _init_layout(self):
        self.musicInThisPCGroup.addSettingCard(self.musicFolderCard)
        self.musicInThisPCGroup.addSettingCard(self.downloadFolderCard)

        self.aboutGroup.addSettingCard(self.help_card)
        self.aboutGroup.addSettingCard(self.about)

        self.loginGroup.addSettingCard(self.userInfo)

        self.expandLayout.addWidget(self.settingLabel)
        self.expandLayout.addWidget(self.musicInThisPCGroup)
        self.expandLayout.addWidget(self.aboutGroup)
        self.expandLayout.addWidget(self.loginGroup)
        self.scrollWidget.setLayout(self.expandLayout)

    def _init_connect(self):
        self.about.clicked.connect(
            lambda: QDesktopServices.openUrl
            (QUrl('https://github.com/vagmr')))  # type: ignore
        global userInfo
        userInfo = self.userInfo


if __name__ == "__main__":
    app = QApplication([])
    window = SettingInterface()
    window.show()
    app.exec()
