# python Gui Dev Note(pyqt开发笔记)

[learn pyqt]: # README.md

## 1.初识

### 1.创建第一个pyqt程序

```python
from PyQt6.QtWidgets import QApplication, QWidget
import sys
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
from ui_w1 import Ui_window


class Window(QWidget, Ui_window):
    def __init__(self):
        super().__init__()
        print("__init__", self.__repr__())
        self.setupUi(self)
        self.setGeometry(600, 300, 730, 400)
        self.setWindowTitle("python Gui Dev")
        self.setWindowIcon(QIcon("../img/1.ico"))
        self.setFixedHeight(400)
        self.setFixedWidth(730)
        self.show()


app = QApplication(sys.argv)
window = Window()
if sys.flags.interactive != 1 or not hasattr(QtCore, "PYQT_VERSION"):
    sys.exit(app.exec())
```

### 2.使用图标

```python
from PyQt6.QtWidgets import QWidget,QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QRect
import sys

class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(QRect(600, 300, 800, 350))
        self.setWindowTitle("python Gui Dev")
        self.setWindowIcon(QIcon("../img/1.ico"))

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
```

### 3.使用ui文件的三种方式

- 1,通过pyuic6 name.ui -o name.py转化成py文件
    然后使用另外一个文件进行加载类似这种

    ```python
    from PyQt6.QtWidgets import QApplication, QWidget
    from ui_login import Ui_cardWin
    import sys

    class Window(QWidget, Ui_cardWin):
        def __init__(self):
            super().__init__()
            self.setupUi(self)
            self.show()

    app = QApplication(sys.argv)
    w = Window()

    sys.exit(app.exec())
    直接可以使用self.对象名对组件进行操作

- 2,通过pyuic6 -x name.ui -o name.py转化成py文件,这种方式可以直接在该文件进行操作
- 3 通过uic模块的loadUi方法进行加载ui文件

    ```python
    from PyQt6.QtWidgets import QApplication, QWidget
    import sys
    from PyQt6 import uic
    class UI(QWidget):
        def __init__(self):
            super().__init__()
            uic.loadUi("w1.ui", self)  # type:ignore
            self.show()

    app = QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec())
    ```

使用对象需要通过```self.findChild(组件名,对象名)```进行获取

### 4.常用组件和方法

#### 1.常用组件

- 1.```QApplication```：创建应用程序
- 2.```QWidget```：创建窗口
- 3.```QIcon```：设置窗口图标
- 4.```QRect```：设置窗口大小
- 5.```QLabel```：创建标签
- 6.```QSpinBox```：创建数字输入框
- 7.```QCheckBox```：创建复选框
- 8.```QMenu```：创建菜单
- 9.```QPushButton```：创建按钮
- 10.```QVBoxLayout```：创建垂直布局
- 11.```QHBoxLayout```：创建水平布局
- 12.```QGridLayout```：创建网格布局
- 13.```QTableWidget```：创建表格

#### 2.常用方法

- 1.```show```：显示窗口
- 2.```setGeometry```：设置窗口大小
- 3.```setWindowTitle```：设置窗口标题
- 4.```setWindowIcon```：设置窗口图标
- 5.```setFixedHeight```：设置窗口高度
- 6.```setFixedWidth```：设置窗口宽度
- 7.```setStyleSheet```：设置窗口样式
- 8.```setIcon```：设置图标
- 9.```setIconSize```：设置图标大小
- 10.```setMaximumHeight```：设置窗口最大高度
- 11.```setMaximumWidth```：设置窗口最大宽度
- 12.```setMinimumHeight```：设置窗口最小高度
- 13.```setMinimumWidth```：设置窗口最小宽度

[其它笔记](note.Md)
