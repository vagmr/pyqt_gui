"""
@文件        :cusMessageBox.py
@说明        :自定义消息框 
@时间        :2024/02/11 22:14:41
@作者        :vagmr
@版本        :1.1
"""
from PyQt6.QtWidgets import QLabel
from qfluentwidgets import MessageBoxBase, SubtitleLabel, PushButton
from os import path

style = ''
try:
    with open(path.join(path.dirname(__file__), 'cusBox.qss'), 'r', encoding='utf-8') as f:
        style = f.read()
except FileNotFoundError:
    raise FileNotFoundError('cusBox.qss not found!')


class CustomWarningMessageBox(MessageBoxBase):
    """自定义的警告消息框

    Args:
        MessageBoxBase (_type_): _description_
    """

    def __init__(self, parent=None, title=None, content=''):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(title, self)
        self.label = QLabel(self)
        self.label.setObjectName('content')
        self.label.setStyleSheet(style)
        self.label.setText(content)
        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.label)

        # change the text of button
        self.yesButton.setObjectName('yesButton')
        self.yesButton.setStyleSheet(style)
        self.yesButton.setText('确定')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(200)
