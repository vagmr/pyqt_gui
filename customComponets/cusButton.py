"""
@文件        :cusButton.py
@说明        :一个简单的自定义按钮 
@时间        :2024/02/12 10:24:59
@作者        :vagmr
@版本        :1.1
"""


from PyQt6.QtWidgets import QPushButton, QApplication, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from os import path

style = ''
try:
    with open(path.join(path.dirname(__file__), 'cusButton.qss'), 'r', encoding='utf-8') as f:
        style = f.read()
except FileNotFoundError:
    raise FileNotFoundError('cusButton.qss not found!')


class CusButton(QPushButton):
    def __init__(self, icon_path=path.join(path.dirname(__file__), 'asset/py.svg'), text='', parent=None):
        super().__init__(parent)
        icon = QIcon(icon_path)
        self.setIcon(icon)
        self.setIconSize(QSize(20, 20))
        self.setObjectName('VButton')
        self.setText(text)
        self.setStyleSheet(style)

    def setIconByPath(self, icon_path: str):
        icon = QIcon(icon_path)
        super().setIcon(icon)
        self.setIconSize(QSize(20, 20))

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
        print(new_style)
        self.setStyleSheet(new_style)


if __name__ == '__main__':
    app = QApplication([])
    w = QWidget()
    btn = CusButton(text='hello', parent=w)
    btn.setIconSize(QSize(30, 30))
    btn.setColor('111')
    w.show()
    app.exec()
