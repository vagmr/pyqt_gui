"""
@文件        :cusLabel.py
@说明        :自定义标签 
@时间        :2024/02/13 12:42:31
@作者        :vagmr
@版本        :1.1
"""


from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from qfluentwidgets.components.widgets.acrylic_label import AcrylicLabel


class VTitleLabel(AcrylicLabel):
    """一个自定义的标签类，继承自 AcrylicLabel 类。

    这个类显示一些文本，具有字体、对齐和着色效果。
    它使用了 qfluentwidgets 库中的 AcrylicLabel 类，提供了一个模糊背景效果。

    属性:
        blurRadius: 一个整数，表示模糊效果的半径。默认值是 25。
        tintColor: 一个 QColor 对象，表示着色效果的颜色。默认值是黑色，不透明度为 40%。
        text: 一个字符串，表示要显示在标签上的文本。默认值是 "默认标题"。
    """

    def __init__(self, blurRadius=25, tintColor=QColor(0, 0, 0, 102), text="默认标题", parent=None):
        """Initialize the VTitleLabel object with the given parameters.

        Args:
            blurRadius: An int indicating the radius of the blur effect. The default is 25.
            tintColor: A QColor object indicating the color of the tint effect. The default is black with 40% opacity.
            text: A str indicating the text to be displayed on the label. The default is "默认标题".
            parent: A QWidget object indicating the parent widget of the label. The default is None.
        """
        super().__init__(blurRadius=blurRadius, tintColor=tintColor, parent=parent)
        self.setFont(QFont("Lato", 20))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText(text)
