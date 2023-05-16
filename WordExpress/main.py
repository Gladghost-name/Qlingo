from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
import os


class PageText(QGraphicsTextItem):
    def __init__(self):
        super().__init__()
        self.focusItem()
        self.setDefaultTextColor(QColor('black'))
        self.setCursor(Qt.IBeamCursor)
        self.setTextInteractionFlags(
            Qt.TextEditable | Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse)

        self.block_format = QTextBlockFormat()
        self.block_format.setLineHeight(500.0, QTextBlockFormat.ProportionalHeight)

        # self.text_cursor.setBlockFormat(self.block_format)

    def paint(self, painter, option, a):
        option.state = QStyle.State_None
        return super(PageText, self).paint(painter, option, a)

class PageBoard(QGraphicsRectItem):
    def __init__(self, size, text_widget):
        super().__init__()
        self.setRect(0, 0, size[0], size[1])
        self.setBrush(QBrush(QColor('white')))
        self.setCursor(Qt.IBeamCursor)
        self.overlay_text = text_widget
        self.setPen(QPen(QColor('grey'), .5))
    def setPos(self, x, y):
        self.setRect(QRectF(x, y, self.rect().width(), self.rect().height()))
    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.scene().setFocusItem(self.overlay_text)
        self.scene().update()
        # print('yes')

class GraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self._zoom = 0
    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        # self.scale(a0.angleDelta().y(), a0.angleDelta().y())
        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            # self._zoom -= 1
        if self._zoom > 0:
            # print(self._zoom)
            if self._zoom <= 11:
                self.scale(factor, factor)
            else:
                self._zoom = 10
            # else:
            #     self._zoom = 0
        elif self._zoom == 0:
            self.scale(factor, factor)
        else:
            self._zoom = 0
        # print(a0.angleDelta().y())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(950, 780)
        self.scene = QGraphicsScene()
        self.view = GraphicsView()
        self.view.setScene(self.scene)
        self.setWindowTitle("WordExpress ~ Unititled*")
        self.view.setStyleSheet("""background-color: transparent; border: 0px; selection-background-color: grey;""")
        self.page_size = (900, 1000)
        # self.page_board = PageBoard(self.page_size)
        # self.scene.addItem(self.page_board)

        palette = QPalette()
        palette.setColor(QPalette.Highlight, QColor('grey'))
        self.setPalette(palette)


        self.document = QTextDocument()
        self.document.setDefaultFont(QFont('Open Sans', 9))
        self.document.setPageSize(QSizeF(self.page_size[0], self.page_size[1]))
        self.document.setDocumentMargin(20.0*2)
        # self.document.setDefaultTextOption()

        self.page_amount = 1

        self.sample_text = PageText()
        self.sample_text.boundingRect().setSize(QSizeF(self.page_size[0], self.page_size[1]))
        # print(self.sample_text.boundingRect().height())
        # self.sample_text.boundingRect().setRect(0, 0, self.page_size[0], self.page_size[1])
        self.scene.addItem(self.sample_text)
        self.sample_text.setDocument(self.document)


        self.shortcut_dup = QShortcut(QKeySequence('ctrl+i'), self)
        self.shortcut_dup.activated.connect(self.insert_image)

        self.main_menu = QMenuBar()
        self.current_document = None

        self.file_menu = QMenu("File")
        self.file_menu.addAction("New Document", self.open_new, 'ctrl+n')
        self.file_menu.addAction("Open Document", self.open_doc, 'ctrl+o')
        self.file_menu.addSeparator()
        self.file_menu.addAction("Save As", self.save_as, 'ctrl+alt+s')
        self.file_menu.addAction("Save", self.save, 'ctrl+s')
        self.file_menu.addAction("Reload from Disk", self.reload, 'ctrl+r')
        # self.file_menu.addAction("Show File in Directory", self.save, 'ctrl+s')
        self.main_menu.addMenu(self.file_menu)

        self.edit_menu = QMenu("Edit")
        self.main_menu.addMenu(self.edit_menu)

        self.setMenuBar(self.main_menu)

        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)


        self.iter_height = self.page_size[1]
        self.timer = QTimer(self)
        self.timer.setInterval(int(1000/60))
        self.timer.timeout.connect(self.is_paged)
        self.timer.start()


        self.setCentralWidget(self.view)

    def open_new(self):
        self.sample_text.document().clear()
        self.current_document = None
        self.setWindowTitle("Unitled* Document")
    def reload(self):
        if self.current_document is not None:
            f = open(self.current_document, 'r+')
            self.sample_text.document().setPlainText(f.read())
    def open_doc(self):
        self.file_viewer = QFileDialog()
        self.file_data = self.file_viewer.getOpenFileName()
        if self.file_data[0]:
            f = open(self.file_data[0], 'r+')
            self.current_document = self.file_data[0]
            self.setWindowTitle(f"WordExpress ~ {self.file_data[0]}")
            self.sample_text.document().setPlainText(f.read())
    def save_as(self):
        filedialog = QFileDialog()
        file_save_loc = filedialog.getSaveFileName(self, "Save the document!")
        if file_save_loc[0]:
            f = open(file_save_loc[0], 'w+')
            self.current_document = file_save_loc[0]
            self.setWindowTitle(f"WordExpress ~ {file_save_loc[0]}")
            f.write(self.sample_text.document().toPlainText())
    def save(self):
        if self.current_document is None:
            self.save_as()
        else:
            f = open(self.current_document, 'w+')
            f.write(self.sample_text.document().toPlainText())
    def insert_image(self):
        # self.sample_text.textCursor().insertTable(5, 5)
        self.file_dialog = QFileDialog()
        self.file_data = self.file_dialog.getOpenFileName(self, "Open an image", '.')
        if self.file_data[0]:
            self.sample_text.textCursor().insertImage(QImage(self.file_data[0]).scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            print(self.file_data[0])
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
            self.new_page = PageBoard(self.page_size, self.sample_text)
            self.scene.addItem(self.new_page)
            self.new_page.setPos(0, self.iter_height)
            self.new_page.setZValue(-1)
            self.iter_height += self.new_page.rect().height()


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