# A New Commit!
# -------------------->

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from components import *
from gizmos import *


class GraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        # self.scene().itemAt()
        self.scene().selectionChanged.connect(self.object_selected)
        # self.scene()

        self.shortcut_paste = QShortcut(QKeySequence('ctrl+v'), self)
        self.shortcut_paste.activated.connect(self.paste_item)

        self.selected_item = []
        self.gizmos = []
        self.shift_pressed = False

        self.items_to_paste = []

        self.setStyleSheet("""selection-background-color: #272727; border: 0px; background-color: transparent;""")

        self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRubberBandSelectionMode(Qt.ItemSelectionMode.ContainsItemShape)
        self.scene().mouseGrabberItem()

        self.board = QGraphicsRectItem()
        self.backdrop = QGraphicsDropShadowEffect()
        self.backdrop.setBlurRadius(12.0)
        self.backdrop.setOffset(0.4, 0.7)
        self.backdrop.setColor(QColor('#CCCCCC'))
        self.board.setGraphicsEffect(self.backdrop)

        self.board.setRect(20, 20, 900, 500)
        # self.board.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        self.scene().addItem(self.board)
        self.board.setPen(QPen(Qt.NoPen))
        self.board.setBrush(QColor('white'))

        self.demo_rect2 = Entity(self.scene(), 'rectangle', (100, 100), (50, 50), "black")
        self.demo_rect2.draw()

        self.demo_rect1 = Entity(self.scene(), 'ellipse', (100, 100), (100, 100), "black")
        self.demo_rect1.draw()
        self.grabKeyboard()


    def object_selected(self):
        for item in self.gizmos:
            item.close_all()
            item.deleteLater()
        self.gizmos = []
        self.selected_item = []
        if self.scene().selectedItems() != []:
            for item in self.scene().selectedItems():
                if item not in self.selected_item:
                    self.selected_item.append(item)
                    self.gizmo = RectGizmo(self.scene(), self.gizmos, self.selected_item, self.items_to_paste)
                    self.gizmo.setItem(item)
                    self.scene().addWidget(self.gizmo)
                    self.gizmos.append(self.gizmo)
        self.update()
        self.scene().update()
    def paste_item(self):
        for items in self.items_to_paste:
            self.pasted_item = items[0]()
            self.pasted_item.setRect(items[1].rect())
            self.pasted_item.setPen(items[1].pen())
            self.pasted_item.setBrush(items[1].brush())
            self.scene().addItem(self.pasted_item)
        self.items_to_paste = []


class MyApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        super().__init__(sys.argv)
        self.main = QMainWindow()
        self.main.resize(850, 600)

        # Test for undo and redo functionality.
        # self.undo_stack = QUndoStack()
        # self.commend = QUndoCommand()
        # self.undo_stack.push(self.command)
        self.shortcut_open_image = QShortcut(QKeySequence('ctrl+i'), self.main)
        self.shortcut_open_image.activated.connect(self.open_image)

        self.body = QFrame()
        self.body_layout = QVBoxLayout()
        self.body.setLayout(self.body_layout)

        self.change_color = QPushButton("Change item(s) color!")
        self.change_color.clicked.connect(self.change_item_color)
        self.body_layout.addWidget(self.change_color)

        self.change_pen = QPushButton("Change item(s) pen color!")
        self.change_pen.clicked.connect(self.change_item_pen_color)
        self.body_layout.addWidget(self.change_pen)

        self.change_bg_color = QPushButton("Change background color")
        self.change_bg_color.clicked.connect(self.change_bg)
        self.body_layout.addWidget(self.change_bg_color)

        self.BringToFront = QPushButton("Bring to front!")
        self.BringToFront.clicked.connect(self.bringfront)
        self.body_layout.addWidget(self.BringToFront)

        self.BringToBack = QPushButton("Bring to back!")
        self.BringToBack.clicked.connect(self.bringback)
        self.body_layout.addWidget(self.BringToBack)

        self.scene = QGraphicsScene()
        # self.scene.del
        self.view = GraphicsView(self.scene)
        #self.view.setBackgroundBrush(QColor('#D9D9D9'))
        # self.view.setStyleSheet("""border: 0px;""")
        self.body_layout.addWidget(self.view)

        self.main.setCentralWidget(self.body)
    def open_image(self):
        self.file_dialog = QFileDialog()
        self.file = self.file_dialog.getOpenFileName(self.main, "Open An Image")
        if self.file[0]:
            self.entity = Entity(self.scene, 'pixmap', size=(500, 500), pos=(50, 50), filename=self.file[0])
            self.entity.draw()
            print(self.file[0])
    def bringfront(self):
        for item in self.scene.selectedItems():
            item.setZValue(1)
            # print(item)
    def bringback(self):
        for item in self.scene.selectedItems():
            item.setZValue(-1)
            # print(item)
    def change_item_color(self):
        if self.scene.selectedItems() != []:
            self.color_diag = QColorDialog(self.scene.selectedItems()[0].brush().color())
            self.color_diag.colorSelected.connect(self.selected_color)
            self.color_diag.show()

    def change_bg(self):
        # if self.scene.selectedItems() != []:
        self.color_diag = QColorDialog(self.view.board.brush().color())
        self.color_diag.colorSelected.connect(self.background_color)
        self.color_diag.show()

    def background_color(self):
        self.view.board.setBrush(QBrush(QColor(self.color_diag.selectedColor().name())))

    def change_item_pen_color(self):
        # print(self.view.demo_rect.pen().color().name())
        if self.scene.selectedItems() != []:
            self.color_diag = QColorDialog()
            self.color_diag.colorSelected.connect(self.pen_color)
            self.color_diag.show()

    def selected_color(self):
        for item in self.scene.selectedItems():
            item.setBrush(QColor(self.color_diag.selectedColor().name()))

    def pen_color(self):
        for item in self.scene.selectedItems():
            item.setPen(QColor(self.color_diag.selectedColor().name()))

    def run(self):
        self.main.show()
        sys.exit(self.exec())


if __name__ == '__main__':
    app = MyApp()
    app.run()
