from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import *


class PageText(QGraphicsTextItem):
    def __init__(self):
        super().__init__()
        self.focusItem()
        self.setCursor(Qt.IBeamCursor)
        # self.setFlag(QGraphicsItem.ItemIsFocusable, False)
        # self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setTextInteractionFlags(
            Qt.TextEditable | Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse)
        # self.setDocument(self.document)

    def paint(self, painter, option, a):
        option.state = QStyle.State_None
        return super(PageText, self).paint(painter, option, a)

class PageBoard(QGraphicsRectItem):
    def __init__(self, size):
        super().__init__()
        self.setRect(0, 0, size[0], size[1])
        self.setBrush(QBrush(QColor('white')))
        self.setCursor(Qt.IBeamCursor)
        self.setPen(QPen(QColor('grey'), .5))
    def setPos(self, x, y):
        self.setRect(QRectF(x, y, self.rect().width(), self.rect().height()))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(950, 780)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setStyleSheet("""background-color: transparent; border: 0px;""")
        self.page_size = (900, 1000)
        # self.page_board = PageBoard(self.page_size)
        # self.scene.addItem(self.page_board)

        self.document = QTextDocument()
        self.document.setPageSize(QSizeF(self.page_size[0], self.page_size[1]))
        self.document.setDocumentMargin(20.0*2)
        self.document.setPlainText("Hello, World")
        # self.document.setDefaultStyleSheet("""border: 0px;""")
        self.document.blockCountChanged.connect(self.is_paged)

        self.page_amount = 1

        self.sample_text = PageText()
        self.scene.addItem(self.sample_text)
        self.sample_text.setDocument(self.document)


        self.setCentralWidget(self.view)
    def is_paged(self):
        if self.sample_text.boundingRect().height() > self.iter_height:
            self.page_amount += 1
        else:
            if self.page_amount != 1:
                if self.iter_height-self.page_size[1] > self.sample_text.boundingRect().height():
                    self.page_amount -= 1
                    self.iter_height -= self.page_size[1]
                    self.update()
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.iter_height = 0
        for item in self.scene.items():
            if type(item) == PageBoard:
                self.scene.removeItem(item)
        for i in range(self.page_amount):
            self.new_page = PageBoard(self.page_size)
            self.scene.addItem(self.new_page)
            self.new_page.setPos(0, self.iter_height)
            self.new_page.setZValue(-1)
            self.iter_height += self.new_page.rect().height()+10


class MainApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.main = MainWindow()
    def run(self):
        self.main.show()
        sys.exit(self.exec())

if __name__ == '__main__':
    app = MainApp()
    app.run()