import os

from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore
from qlingo.runner import *
import sys
from qlingo.wid.widgets import *
from qlingo.handlers.prop_handler import *


class AppFrame(QFrame):
    # the current app frame.
    def __init__(self):
        super().__init__()
        self.content = []
        self.setStyleSheet("""background-color: black; color: white;""")

    def setBackgroundColor(self, color):
        style = self.styleSheet()
        style = style.replace(f"""background-color: {color};""", '')
        self.background = f"""background-color: {color};"""
        if self.background not in style:
            style += self.background
            self.setStyleSheet(style)

    def addWidget(self, content):
        self.content = content
        for w in self.content:
            try:
                w.resize(400, 400)
                w.show()
            except RuntimeError as r:
                print(r)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        for w in self.content:
            # w.setFixedSize(w.rect().width(), w.rect().height())
            w.update()
        return super().paintEvent(a0)


class Window(QMainWindow):
    # the main reloding window.
    def __init__(self, filename):
        super().__init__()
        self.file = filename
        self.resize(850, 600)
        self.runner = Runner()
        self.content = []

        self.new_frame = AppFrame()
        self.setCentralWidget(self.new_frame)

        self.standby_timer = QTimer(self)
        self.standby_timer.setInterval(int(1000 / 60))
        self.standby_timer.timeout.connect(self.load)

        self.run()

        self.modifiedOn = os.path.getmtime(self.file)

    def run(self):
        if self.content != []:
            # clear all the viewing widgets.
            for widget in self.content:
                try:
                    widget.deleteLater()
                    self.content = []
                except RuntimeError as r:
                    print(r)
        self.runner.run(self.file)
        propHandler = PropHandler()
        self.master_window = self.runner.master_class
        self.master_window.setFixedSize(self.size())
        for child in self.master_window.frame.children():
            if child != self.master_window.frame.layout():
                child.setParent(self)
                self.content.append(child)
                child.setFixedSize(child.size().width(), child.size().height())
                self.new_frame.addWidget(self.content)
                self.new_frame.update()
                child.update()
        for item in self.runner.master_children:
            if type(item) == dict:
                propHandler.inherit_prop(self, item)

    def load(self):
        modified = os.path.getmtime(self.file)
        if modified != self.modifiedOn:
            self.modifiedOn = modified
            self.run()

    def reload_app(self, b):
        if b == True:
            self.standby_timer.start()


class qquApp(QApplication):
    def __init__(self, filename):
        super().__init__(sys.argv)
        self.window = Window(filename)
        # self.window.load(file)

    def run(self):
        self.window.show()
        sys.exit(self.exec())

    # def load_app(self):
    def reloadable(self, b):
        self.window.reload_app(b)

    def load_app(self):
        self.window.load()

# to run the application!
# app = qquApp('app.qqu')
# app.reloadable(True)
# app.run()