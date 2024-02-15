"""
@文件        :cusButton.py
@说明        :一个简单的自定义按钮 
@时间        :2024/02/12 10:24:59
@作者        :vagmr
@版本        :1.1
"""


from PyQt6.QtWidgets import QPushButton, QApplication, QWidget
from PyQt6.QtGui import QIcon
from typing import Union
from PyQt6.QtCore import QSize
from qfluentwidgets import PushButton
from os import path

style = ''
try:
    with open(path.join(path.dirname(__file__), 'cusButton.qss'), 'r', encoding='utf-8') as f:
        style = f.read()
except FileNotFoundError:
    raise FileNotFoundError('cusButton.qss not found!')


class CusButton(QPushButton):
    """自定义按钮

    Methods:
        - __init__(self, icon: Union[str, QIcon] = QDir.currentPath() + '/asset/py.svg', text='', parent=None):
            初始化按钮。
            参数:
                - icon: Union[str, QIcon]，按钮的图标，可以是图标的路径字符串或 QIcon 对象，默认为 py.svg 图标。
                - text: str，按钮显示的文本，默认为空。
                - parent: QWidget，父级窗口，默认为 None。
        - setIconByPath(self, icon_path: str, size: tuple = (20, 20)):
            设置按钮的图标。
            参数:
                - icon_path: str，图标的路径字符串。
                - size: tuple，图标的大小，默认为 (20, 20)。
        - setColor(self, color):
            设置按钮的背景颜色。
            参数:
                - color: str，颜色字符串，例如 '#RRGGBB'。
    """

    def __init__(self, icon: Union[str, QIcon] = path.join(path.dirname(__file__), 'asset/py.svg'), text='', parent=None):
        super().__init__(parent)
        if isinstance(icon, str):
            icon = QIcon(icon)
        self.setIcon(icon)
        self.setIconSize(QSize(20, 20))
        self.setObjectName('VButton')
        self.setText(text)
        self.setMaximumSize(180, 45)
        self.setStyleSheet(style)

    def setIcon(self, icon: Union[QIcon, str], size: tuple = (20, 20)):
        self.setProperty('hasIcon', icon is not None)
        self.setStyleSheet(style)
        if isinstance(icon, str):
            icon = QIcon(icon)
        super().setIcon(icon)
        self.setIconSize(QSize(*size))

    def setColor(self, color):
        # 获取当前的样式表
        current_style = self.styleSheet()
        # 使用正则表达式删除 #VButton 的背景色定义
        # 验证或转换颜色值
        from PyQt6.QtGui import QColor
        color = QColor(color)
        if color.isValid():
            color = color.name()
        else:
            print('invalid color')
            color = '#23c7dd'  # 默认颜色
        import re
        new_style = re.sub(
            r'#VButton\s*\{\s*(background-color: [^;]+;)?', f'#VButton {{\nbackground-color: {color};', current_style)
        self.setStyleSheet(new_style)


if __name__ == '__main__':
    app = QApplication([])
    w = QWidget()
    btn = CusButton(text='hello', parent=w)
    btn.setIconSize(QSize(30, 30))
    btn.setColor('111')
    w.show()
    app.exec()
