# Note: This is a test demo, Use at your own risk!.
# Warning: More than 300 lines of code!
# ------------------------------------------------------ >
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import *


class Rectangle(QGraphicsRectItem):
    def __init__(self):
        super().__init__()

    def paint(self, painter, option, widget):
        is_selected = option.state & QStyle.State_Selected
        # Remove default paint from selection
        option.state &= ~QStyle.State_Selected
        super().paint(painter, option, widget)


class Ellipse(QGraphicsEllipseItem):
    def __init__(self):
        super().__init__()

    def paint(self, painter, option, widget):
        is_selected = option.state & QStyle.State_Selected
        # Remove default paint from selection
        option.state &= ~QStyle.State_Selected
        super().paint(painter, option, widget)


class RectGizmo(QFrame):
    def __init__(self, gizmos_list):
        super().__init__()
        self.setStyleSheet("""background-color: transparent;""")
        self.item = None
        self.dragging = 'None'
        self.list = gizmos_list
        self.cur = Qt.SizeAllCursor
        self.cur_x = 0
        self.cur_y = 0
        self.setMouseTracking(True)
        self.dragging = 'None'
        self.pressed = False
        self.directer = QLabel(self)
        self.directer.hide()

        self.gizmos = []

        # get the keyboard input!.
        self.grabKeyboard()

        # setting the node size and offset!
        self.node_size = 13
        self.node_offset = 2

    def setItem(self, item):
        # Set the item to be displayed and controlled by the gizmo!
        self.item = item
        self.cur_x = self.item.rect().x() - self.node_size / 2
        self.cur_y = self.item.rect().y() - self.node_size / 2

        self.move(int(self.cur_x), int(self.cur_y))
        self.setFixedSize(int(self.item.rect().width() + self.node_size),
                          int(self.item.rect().height() + self.node_size))

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.painter = QPainter(self)
        self.move(int(self.cur_x), int(self.cur_y))
        self.setFixedSize(int(self.item.rect().size().width() + self.node_size),
                          int(self.item.rect().size().height() + self.node_size))

        self.painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        if not self.pressed:
            self.painter.setBrush(Qt.NoBrush)
            self.painter.setPen(QPen(QColor('#A200D6'), 1))
            self.painter.drawRect(
                QRectF(self.rect().topLeft().x() + self.node_size / 2, self.rect().topLeft().y() + self.node_size / 2,
                       self.rect().width() - (self.node_size - 1), self.rect().height() - (self.node_size - 1)))
            self.painter.setBrush(QColor('white'))
            self.painter.setPen(QPen(QColor('#A200D6'), 2))
            self.painter.drawEllipse(
                QRect(self.rect().topLeft().x() + 3, self.rect().topLeft().y() + 3, self.node_size, self.node_size))
            self.painter.drawEllipse(
                QRect(self.rect().topRight().x() - (self.node_size + 1), self.rect().topRight().y() + 4, self.node_size,
                      self.node_size))

            self.painter.drawEllipse(
                QRect(self.rect().bottomLeft().x() + 4, self.rect().bottomLeft().y() - (self.node_size + 1),
                      self.node_size, self.node_size))

            self.painter.drawEllipse(
                QRectF(self.rect().width() - (self.node_size + 1), (self.rect().height() / 2) - self.node_size / 2,
                       self.node_size, self.node_size))
            self.painter.drawEllipse(
                QRectF(2, (self.rect().height() / 2) - self.node_size / 2, self.node_size, self.node_size))
            self.painter.drawEllipse(
                QRectF(self.rect().width() / 2 - self.node_size / 2, 2, self.node_size, self.node_size))
            self.painter.drawEllipse(
                QRectF(self.rect().width() / 2 - self.node_size / 2, self.rect().height() - (self.node_size + 1),
                       self.node_size, self.node_size))

            self.painter.drawEllipse(
                QRect(self.rect().bottomRight().x() - (self.node_size + 1),
                      self.rect().bottomRight().y() - (self.node_size + 1), self.node_size, self.node_size))

        self.painter.end()
        return super().paintEvent(a0)

    def mouseMoveEvent(self, a0):
        # handle all the various dragging of corners!
        if a0.x() <= self.rect().topLeft().x() + 15 and a0.y() <= self.rect().topLeft().y() + 15:
            self.directer.show()
            self.directer.setFixedSize(10, 10)
            self.setCursor(Qt.SizeFDiagCursor)
            self.dragging = "topLeft"
            self.directer.move(a0.x(), a0.y())
            self.update()
        elif a0.x() >= self.rect().topRight().x() - 15 and a0.y() <= self.rect().topRight().y() + 15:
            self.directer.show()
            self.dragging = "topRight"
            self.directer.setFixedSize(10, 10)
            self.setCursor(Qt.SizeBDiagCursor)
            self.directer.move(a0.x(), a0.y())
            self.update()
        elif a0.x() <= self.rect().bottomLeft().x() + 15 and a0.y() >= self.rect().bottomLeft().y() - 15:
            self.directer.show()
            self.dragging = "bottomLeft"
            self.directer.setFixedSize(10, 10)
            self.setCursor(Qt.SizeBDiagCursor)
            self.directer.move(a0.x(), a0.y())
            self.update()
        elif a0.x() >= self.rect().bottomRight().x() - 15 and a0.y() >= self.rect().bottomRight().y() - 15:
            self.directer.show()
            self.dragging = "bottomRight"
            self.directer.setFixedSize(10, 10)
            self.setCursor(Qt.SizeFDiagCursor)
            self.directer.move(a0.x(), a0.y())
            self.update()
        elif a0.x() >= self.rect().width() - 15:
            self.directer.show()
            self.dragging = "right"
            self.directer.setFixedSize(10, 10)
            self.setCursor(Qt.SizeHorCursor)
            self.directer.move(a0.x(), a0.y())
            self.update()
        elif a0.x() <= 20:
            self.directer.show()
            self.dragging = "left"
            self.directer.setFixedSize(10, 10)
            self.setCursor(Qt.SizeHorCursor)
            self.directer.move(a0.x(), a0.y())
            self.update()
        elif a0.y() >= self.rect().height() - 17:
            self.directer.show()
            self.dragging = "bottom"
            self.directer.setFixedSize(10, 10)
            self.setCursor(Qt.SizeVerCursor)
            self.directer.move(a0.x(), a0.y())
            self.update()
        elif a0.y() <= 17:
            self.directer.show()
            self.dragging = "top"
            self.directer.setFixedSize(10, 10)
            self.setCursor(Qt.SizeVerCursor)
            self.directer.move(a0.x(), a0.y())
            self.update()
        else:
            self.dragging = "center"
            self.directer.show()
            # self.dragging = "center"
            self.directer.setFixedSize(10, 10)
            self.directer.move(a0.x(), a0.y())
            self.setCursor(self.cur)

        if self.pressed:
            # self.setCursor(Qt.CrossCursor)
            self.move_x = self.pos_x
            self.move_y = self.pos_y
            if self.cur_dragging == 'bottomRight':
                self.item.setRect(QRectF(self.item.rect().x(), self.item.rect().y(), self.move_x, self.move_y))
                self.update()
                self.item.scene().update()
            elif self.cur_dragging == 'right':
                self.item.setRect(
                    QRectF(self.item.rect().x(), self.item.rect().y(), self.move_x, self.item.rect().height()))
                self.update()
                self.item.scene().update()
            elif self.cur_dragging == 'left':
                # self.item.rect().setLeft(a0.x())
                self.rec = QRectF(self.item.rect())
                self.new_rect = self.rec.adjusted(-(self.pos_x - a0.x()), 0, 0, 0)
                self.item.setRect(self.new_rect)
                self.item.update()
                self.update()
                self.item.scene().update()
            elif self.cur_dragging == 'bottomLeft':
                # self.item.rect().setLeft(a0.x())
                self.rec = QRectF(self.item.rect())
                self.new_rect = self.rec.adjusted(-(self.pos_x - a0.x()), 0, 0, -(self.pos_y - a0.y()))
                self.item.setRect(self.new_rect)
                self.item.update()
                self.update()
                self.item.scene().update()
            elif self.cur_dragging == 'topLeft':
                self.rec = QRectF(self.item.rect())
                self.new_rect = self.rec.adjusted(-(self.pos_x - a0.x()), -(self.pos_y - a0.y()), 0, 0)
                self.item.setRect(self.new_rect)
                self.item.update()
                self.update()
                self.item.scene().update()
            elif self.cur_dragging == 'topRight':
                self.rec = QRectF(self.item.rect())
                self.new_rect = self.rec.adjusted(0, -(self.pos_y - a0.y()), -(self.pos_x - a0.x()), 0)
                self.item.setRect(self.new_rect)
                self.item.update()
                self.update()
                self.item.scene().update()
            elif self.cur_dragging == 'bottom':
                self.item.setRect(
                    QRectF(self.item.rect().x(), self.item.rect().y(), self.item.rect().width(), self.move_y))
                self.update()
                self.item.scene().update()
            elif self.cur_dragging == 'center':
                self.rec = QRectF(self.item.rect())
                self.new_rect = self.rec.translated(-(self.pos_x - a0.x()), -(self.pos_y - a0.y()))
                self.item.setRect(self.new_rect)
                self.item.update()
                self.update()
                self.item.scene().update()
            elif self.cur_dragging == 'top':
                self.rec = QRectF(self.item.rect())
                self.new_rect = self.rec.adjusted(0, -(self.pos_y - a0.y()), 0, 0)
                self.item.setRect(self.new_rect)
                self.item.update()
                self.update()
                self.item.scene().update()
            self.pos_x = a0.x()
            self.pos_y = a0.y()
            self.update()

    def mousePressEvent(self, a0):
        self.pos_x = a0.x()
        self.pos_y = a0.y()
        if self.dragging != 'None':
            # start dragging the item!
            self.item.setOpacity(.5)
            self.pressed = True
            self.cur_width = self.item.rect().width()
            self.cur_dragging = self.dragging
        self.update()

    def mouseReleaseEvent(self, *args, **kwargs):
        # update the item and its constituents!
        self.pressed = False
        self.item.setOpacity(1)
        self.setFixedSize(int(self.item.rect().size().width() + 15), int(self.item.rect().size().height() + 15))
        self.hide()
        self.new_frame = RectGizmo(self.list)
        self.gizmos.append(self.new_frame)
        self.new_frame.setItem(self.item)
        self.item.scene().addWidget(self.new_frame)
        self.update()
        self.item.scene().update()
        self.list.append(self.new_frame)
        if self in self.list:
            self.list.remove(self)
        self.deleteLater()

    def close_all(self):
        # remove all the gizmos displayed!
        for widget in self.gizmos:
            widget.deleteLater()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key_Right:
            self.rec = QRectF(self.item.rect())
            self.new_rect = self.rec.translated(2, 0)
            self.item.setRect(self.new_rect)

            self.hide()

            self.new_frame = RectGizmo(self.list)
            self.gizmos.append(self.new_frame)
            self.new_frame.setItem(self.item)
            self.item.scene().addWidget(self.new_frame)

            self.update()
            self.item.scene().update()
            self.list.append(self.new_frame)

            if self in self.list:
                self.list.remove(self)
            self.deleteLater()
        elif a0.key() == Qt.Key_Left:
            self.rec = QRectF(self.item.rect())
            self.new_rect = self.rec.translated(-2, 0)
            self.item.setRect(self.new_rect)

            self.hide()

            self.new_frame = RectGizmo(self.list)
            self.gizmos.append(self.new_frame)
            self.new_frame.setItem(self.item)
            self.item.scene().addWidget(self.new_frame)

            self.update()
            self.item.scene().update()
            self.list.append(self.new_frame)

            if self in self.list:
                self.list.remove(self)
            self.deleteLater()
        elif a0.key() == Qt.Key_Down:
            self.rec = QRectF(self.item.rect())
            self.new_rect = self.rec.translated(0, 2)
            self.item.setRect(self.new_rect)

            self.hide()

            self.new_frame = RectGizmo(self.list)
            self.gizmos.append(self.new_frame)
            self.new_frame.setItem(self.item)
            self.item.scene().addWidget(self.new_frame)

            self.update()
            self.item.scene().update()
            self.list.append(self.new_frame)

            if self in self.list:
                self.list.remove(self)
            self.deleteLater()
        elif a0.key() == Qt.Key_Up:
            self.rec = QRectF(self.item.rect())
            self.new_rect = self.rec.translated(0, -2)
            self.item.setRect(self.new_rect)

            self.hide()

            self.new_frame = RectGizmo(self.list)
            self.gizmos.append(self.new_frame)
            self.new_frame.setItem(self.item)
            self.item.scene().addWidget(self.new_frame)

            self.update()
            self.item.scene().update()
            self.list.append(self.new_frame)

            if self in self.list:
                self.list.remove(self)
            self.deleteLater()

class GraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.scene().selectionChanged.connect(self.object_selected)
        # self.scene()

        self.selected_item = []
        self.gizmos = []

        self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        self.setDragMode(QGraphicsView.RubberBandDrag)

        self.board = QGraphicsRectItem()
        self.board.setRect(20, 20, 700, 500)
        self.scene().addItem(self.board)

        self.board.setPen(QPen(QColor('black'), .3))
        self.board.setBrush(QColor('white'))

        self.demo_rect = Ellipse()
        self.demo_rect.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        self.demo_rect.setPen(QPen(Qt.NoPen))
        self.demo_rect.setBrush(QColor('blue'))
        self.demo_rect.setRect(50, 50, 100, 100)

        self.demo_rect2 = Rectangle()
        self.demo_rect2.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        self.demo_rect2.setPen(QPen(Qt.NoPen))
        self.demo_rect2.setBrush(QColor('blue'))
        self.demo_rect2.setRect(50, 50, 100, 100)

        self.scene().addItem(self.demo_rect)
        self.scene().addItem(self.demo_rect2)

    def object_selected(self):
        for item in self.gizmos:
            item.close_all()
            item.deleteLater()
        self.gizmos = []
        self.selected_item = []
        if self.scene().selectedItems() != []:
            for item in self.scene().selectedItems():
                if item not in self.selected_item:
                    # create a gizmo for selected item.
                    self.gizmo = RectGizmo(self.gizmos)
                    self.gizmo.setItem(item)
                    self.scene().addWidget(self.gizmo)
                    self.gizmos.append(self.gizmo)
                    self.selected_item.append(item)
        self.update()
        self.scene().update()


class MyApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.main = QMainWindow()
        self.main.resize(850, 600)

        self.body = QFrame()
        self.body_layout = QVBoxLayout()
        self.body.setLayout(self.body_layout)

        self.change_color = QPushButton("Change item color!")
        self.change_color.clicked.connect(self.change_item_color)
        self.body_layout.addWidget(self.change_color)

        self.scene = QGraphicsScene()
        # self.scene.del
        self.view = GraphicsView(self.scene)
        self.view.setBackgroundBrush(QColor('#D9D9D9'))
        self.view.setStyleSheet("""border: 0px;""")
        self.body_layout.addWidget(self.view)

        self.main.setCentralWidget(self.body)

    def change_item_color(self):
        self.color_diag = QColorDialog()
        self.color_diag.colorSelected.connect(self.selected_color)
        self.color_diag.show()

    def selected_color(self):
        if self.scene.selectedItems():
            for item in self.scene.selectedItems():
                item.setBrush(QColor(self.color_diag.selectedColor().name()))

    def run(self):
        self.main.show()
        sys.exit(self.exec())

# You can simply run the program from here!.
if __name__ == '__main__':
    app = MyApp()
    app.run()