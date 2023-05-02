# A New Commit!
# -------------------->

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import *


class Rectangle(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.inherited_widget = None
        self.gizmo = None
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)

    def paint(self, painter, option, widget):
        is_selected = option.state & QStyle.State_Selected
        # Remove default paint from selection
        option.state &= ~QStyle.State_Selected
        super().paint(painter, option, widget)


class Ellipse(QGraphicsEllipseItem):
    def __init__(self):
        super().__init__()
        self.inherited_widget = None
        self.gizmo = None
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
    def paint(self, painter, option, widget):
        is_selected = option.state & QStyle.State_Selected
        # Remove default paint from selection
        option.state &= ~QStyle.State_Selected
        super().paint(painter, option, widget)


class RectGizmo(QFrame):
    def __init__(self, gizmos_list, items, paste_objects):
        super().__init__()
        self.setStyleSheet("""background-color: transparent;""")
        self.item = None
        self.all_items = items

        self.objects_to_paste = paste_objects

        self.object_move_speed = 10

        self.proportional = False

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
        self.grabKeyboard()

        self.node_size = 9
        self.node_offset = 2
        self.dup_annual_x = 0
        self.dup_annual_y = 0

        self.shortcut_dup = QShortcut(QKeySequence('ctrl+D'), self)
        self.shortcut_dup.activated.connect(self.duplicate_item)

        self.shortcut_copy = QShortcut(QKeySequence('ctrl+C'), self)
        self.shortcut_copy.activated.connect(self.copy_item)
    def copy_item(self):
        self.objects_to_paste.append([type(self.item), self.item])
    def duplicate_item(self):
        if self.item.inherited_widget is not None and self.item.inherited_widget in self.item.scene().items():
            self.dup_annual_x += self.item.rect().x()-self.item.inherited_widget.rect().x()
            self.dup_annual_y += self.item.rect().y() - self.item.inherited_widget.rect().y()
        self.new_item = type(self.item)()
        self.new_item.inherited_widget = self.item
        self.new_item.setBrush(self.item.brush())
        self.new_item.setPen(self.item.pen())
        self.new_item.setRect(QRectF(self.item.rect().x()+self.dup_annual_x, self.item.rect().y()+self.dup_annual_y, self.item.rect().width(), self.item.rect().height()))
        self.item.scene().addItem(self.new_item)
        self.item.scene().setFocusItem(self.new_item)
        if self.item.inherited_widget is None:
            self.dup_annual_x += 20
            self.dup_annual_y += 20
    def setItem(self, item):
        self.item = item
        # self.item.setParentItem(self)
        # self.setParent(self.item)
        self.item.gizmo = self
        self.cur_x = self.item.rect().x() - self.node_size / 2
        self.cur_y = self.item.rect().y() - self.node_size / 2

        # print(self.item)
        # print(self.cur_x, self.cur_y)

        self.move(int(self.cur_x), int(self.cur_y))
        self.setFixedSize(int(self.item.rect().width() + self.node_size),
                          int(self.item.rect().height() + self.node_size))

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.painter = QPainter(self)

        self.move(int(self.cur_x), int(self.cur_y))
        self.setFixedSize(int(self.item.rect().size().width() + self.node_size),
                          int(self.item.rect().size().height() + self.node_size))

        # self.painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        if not self.pressed:
            self.painter.setBrush(Qt.NoBrush)
            self.painter.setPen(QPen(QColor('#41a4ee'), 1))
            self.painter.drawRect(
                QRectF(self.rect().topLeft().x() + self.node_size / 2, self.rect().topLeft().y() + self.node_size / 2,
                       self.rect().width() - (self.node_size - 1), self.rect().height() - (self.node_size - 1)))
            self.painter.setBrush(QColor('white'))
            self.painter.setPen(QPen(QColor('#41a4ee'), 2))
            self.painter.drawRect(
                QRect(self.rect().topLeft().x() + 3, self.rect().topLeft().y() + 3, self.node_size, self.node_size))
            self.painter.drawRect(
                QRect(self.rect().topRight().x() - (self.node_size + 1), self.rect().topRight().y() + 4, self.node_size,
                      self.node_size))

            self.painter.drawRect(
                QRect(self.rect().bottomLeft().x() + 4, self.rect().bottomLeft().y() - (self.node_size + 1),
                      self.node_size, self.node_size))

            self.painter.drawRect(
                QRectF(self.rect().width() - (self.node_size + 1), (self.rect().height() / 2) - self.node_size / 2,
                       self.node_size, self.node_size))
            self.painter.drawRect(
                QRectF(2, (self.rect().height() / 2) - self.node_size / 2, self.node_size, self.node_size))
            self.painter.drawRect(
                QRectF(self.rect().width() / 2 - self.node_size / 2, 2, self.node_size, self.node_size))
            self.painter.drawRect(
                QRectF(self.rect().width() / 2 - self.node_size / 2, self.rect().height() - (self.node_size + 1),
                       self.node_size, self.node_size))

            self.painter.drawRect(
                QRect(self.rect().bottomRight().x() - (self.node_size + 1),
                      self.rect().bottomRight().y() - (self.node_size + 1), self.node_size, self.node_size))

        self.painter.end()
        return super().paintEvent(a0)

    def mouseMoveEvent(self, a0):
        # self.item.setRec
        # print(a0.y())
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
                if self.proportional:
                    self.item.setRect(QRectF(self.item.rect().x(), self.item.rect().y(), self.move_y, self.move_y))
                else:
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
                if self.proportional:
                    self.new_rect = self.rec.adjusted((self.pos_y - a0.y()), 0, 0, -(self.pos_y - a0.y()))
                else:
                    self.new_rect = self.rec.adjusted(-(self.pos_x - a0.x()), 0, 0, -(self.pos_y - a0.y()))
                self.item.setRect(self.new_rect)
                self.item.update()
                self.update()
                self.item.scene().update()
            elif self.cur_dragging == 'topLeft':
                self.rec = QRectF(self.item.rect())
                if self.proportional:
                    self.new_rect = self.rec.adjusted(-(self.pos_y - a0.y()), -(self.pos_y - a0.y()), 0 , 0)
                else:
                    self.new_rect = self.rec.adjusted(-(self.pos_x - a0.x()), -(self.pos_y - a0.y()), 0, 0)
                self.item.setRect(self.new_rect)
                self.item.update()
                self.update()
                self.item.scene().update()
            elif self.cur_dragging == 'topRight':
                self.rec = QRectF(self.item.rect())
                if self.proportional:
                    self.new_rect = self.rec.adjusted(0, -(self.pos_y - a0.y()), (self.pos_y - a0.y()), 0)
                else:
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
                for item in self.all_items:
                    self.rec = QRectF(item.rect())
                    self.new_rect = self.rec.translated(-(self.pos_x - a0.x()), -(self.pos_y - a0.y()))
                    item.setRect(self.new_rect)
                    item.update()
                    # self.hide()
                    self.pressed = True
                    self.update()
                    item.scene().update()
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
        if a0.button() == Qt.LeftButton:
            # self.all_items = []
            self.pos_x = a0.x()
            self.pos_y = a0.y()
            if self.dragging != 'None':
                if self.dragging != 'center':
                    self.item.setOpacity(.5)
                for i in self.all_items:
                    i.gizmo.pressed = True
                    if i is not self.item:
                        i.gizmo.pos_x = a0.x()
                        i.gizmo.pos_y = a0.y()
                        i.gizmo.cur_width = i.rect().width()
                        i.gizmo.cur_dragging = self.dragging
                        i.gizmo.update()
                # self.pressed = True
                self.cur_width = self.item.rect().width()
                self.cur_dragging = self.dragging
            self.update()

    def mouseReleaseEvent(self, *args, **kwargs):
        for item in self.all_items:
            self.pressed = False
            item.setOpacity(1)
            self.setFixedSize(int(item.rect().size().width() + 15), int(item.rect().size().height() + 15))
            self.hide()
            self.new_frame = RectGizmo(item.gizmo.list, item.gizmo.all_items, item.gizmo.objects_to_paste)
            self.gizmos.append(self.new_frame)
            self.new_frame.setItem(item)
            item.scene().addWidget(self.new_frame)
            self.update()
            item.scene().update()
            self.list.append(self.new_frame)
            # print(self.item.scene().items())
            if self in self.list:
                self.list.remove(self)
            self.deleteLater()

    def close_all(self):
        # self.all_items = []
        for widget in self.list:
            widget.deleteLater()

    def handle_movement(self, a0):
        if a0.key() == Qt.Key_Right:
            self.rec = QRectF(self.item.rect())
            self.new_rect = self.rec.translated(self.object_move_speed, 0)
            self.item.setRect(self.new_rect)

            self.hide()

            self.new_frame = RectGizmo(self.list, self.all_items, self.objects_to_paste)
            self.gizmos.append(self.new_frame)
            self.new_frame.setItem(self.item)
            self.item.scene().addWidget(self.new_frame)

            self.update()
            self.item.scene().update()
            self.list.append(self.new_frame)

            if self in self.list:
                self.list.remove(self)
            # print(self.list)
            self.deleteLater()
        elif a0.key() == Qt.Key_Left:
            self.rec = QRectF(self.item.rect())
            self.new_rect = self.rec.translated(-self.object_move_speed, 0)
            self.item.setRect(self.new_rect)

            self.hide()

            self.new_frame = RectGizmo(self.list, self.all_items, self.objects_to_paste)
            self.gizmos.append(self.new_frame)
            self.new_frame.setItem(self.item)
            self.item.scene().addWidget(self.new_frame)

            self.update()
            self.item.scene().update()
            self.list.append(self.new_frame)

            if self in self.list:
                self.list.remove(self)
            # print(self.list)
            self.deleteLater()
        elif a0.key() == Qt.Key_Down:
            self.rec = QRectF(self.item.rect())
            self.new_rect = self.rec.translated(0, self.object_move_speed)
            self.item.setRect(self.new_rect)

            self.hide()

            self.new_frame = RectGizmo(self.list, self.all_items, self.objects_to_paste)
            self.gizmos.append(self.new_frame)
            self.new_frame.setItem(self.item)
            self.item.scene().addWidget(self.new_frame)

            self.update()
            self.item.scene().update()
            self.list.append(self.new_frame)

            if self in self.list:
                self.list.remove(self)
            # print(self.list)
            self.deleteLater()
        elif a0.key() == Qt.Key_Up:
            self.rec = QRectF(self.item.rect())
            self.new_rect = self.rec.translated(0, -self.object_move_speed)
            self.item.setRect(self.new_rect)

            self.hide()

            self.new_frame = RectGizmo(self.list, self.all_items, self.objects_to_paste)
            self.gizmos.append(self.new_frame)
            self.new_frame.setItem(self.item)
            self.item.scene().addWidget(self.new_frame)

            self.update()
            self.item.scene().update()
            self.list.append(self.new_frame)

            if self in self.list:
                self.list.remove(self)
            # print(self.list)
            self.deleteLater()
        elif a0.key() == Qt.Key_Shift:
            self.proportional = True
        elif a0.key() == Qt.Key_Delete:
            self.item.scene().removeItem(self.item)
            self.deleteLater()
    def moveBy(self, item, x, y):
        self.rec = QRectF(item.rect())
        self.new_rect = self.rec.translated(x, y)
        item.setRect(self.new_rect)

        self.rec = QRectF(self.item.rect())
        self.new_rect = self.rec.translated(x, y)
        self.item.setRect(self.new_rect)

        item.update()
        self.item.update()
        self.update()

        if self in self.list:
            self.list.remove(self)

        for gizmo in self.list:
            gizmo.hide()

        self.new_frame = RectGizmo(self.list, self.all_items, self.objects_to_paste)
        self.list.append(self.new_frame)
        self.new_frame.setItem(item)
        item.scene().addWidget(self.new_frame)

        self.new_frame = RectGizmo(self.list, self.all_items, self.objects_to_paste)
        self.list.append(self.new_frame)
        self.new_frame.setItem(self.item)
        self.item.scene().addWidget(self.new_frame)

        item.update()
        self.item.scene().update()
        self.item.update()

        self.deleteLater()
    def handle_multi_movement(self, a0, item):
        if a0.key() == Qt.Key_Right:
            self.moveBy(item, self.object_move_speed, 0)
        elif a0.key() == Qt.Key_Left:
            self.moveBy(item, -self.object_move_speed, 0)
        elif a0.key() == Qt.Key_Down:
            self.moveBy(item, 0, self.object_move_speed)
        elif a0.key() == Qt.Key_Up:
            self.moveBy(item, 0, -self.object_move_speed)
        elif a0.key() == Qt.Key_Shift:
            self.proportional = True
        elif a0.key() == Qt.Key_Delete:
            # print('item')
            item.scene().removeItem(item)
            # self.item.scene().removeItem(self.item)
            self.deleteLater()
    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        # print(self.all_items)
        if len(self.all_items) > 1:
            for item in self.all_items:
                self.handle_multi_movement(a0, item)
        else:
            self.handle_movement(a0)


class GraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.scene().selectionChanged.connect(self.object_selected)
        # self.scene()

        self.shortcut_paste = QShortcut(QKeySequence('ctrl+v'), self)
        self.shortcut_paste.activated.connect(self.paste_item)

        self.selected_item = []
        self.gizmos = []
        self.shift_pressed = False

        self.items_to_paste = []

        self.setStyleSheet("""selection-background-color: #272727; border: 0px;""")

        self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRubberBandSelectionMode(Qt.ItemSelectionMode.ContainsItemShape)

        self.board = QGraphicsRectItem()
        self.board.setRect(20, 20, 700, 500)
        # self.board.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        self.scene().addItem(self.board)

        self.board.setPen(QPen(QColor('black'), .3))
        self.board.setBrush(QColor('white'))

        self.demo_rect = Ellipse()
        self.demo_rect.setPen(QPen(Qt.NoPen))
        self.demo_rect.setPen(QPen(QColor('black'), .5))
        self.demo_rect.setBrush(QColor('blue'))
        self.demo_rect.setRect(50, 50, 100, 100)

        self.demo_rect2 = Rectangle()
        self.demo_rect2.setPen(QPen(QColor('black'), .5))
        self.demo_rect2.setBrush(QColor('#d9d9d9'))
        self.demo_rect2.setRect(50, 50, 100, 100)

        self.demo_rect3 = Rectangle()
        self.demo_rect3.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        self.demo_rect3.setPen(QPen(QColor('black'), .5))
        self.demo_rect3.setBrush(QColor('#d9d9d9'))
        self.demo_rect3.setRect(50, 50, 100, 100)

        self.scene().addItem(self.demo_rect)
        self.scene().addItem(self.demo_rect2)
        self.scene().addItem(self.demo_rect3)

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
                    self.gizmo = RectGizmo(self.gizmos, self.selected_item, self.items_to_paste)
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

        self.scene = QGraphicsScene()
        # self.scene.del
        self.view = GraphicsView(self.scene)
        self.view.setBackgroundBrush(QColor('#D9D9D9'))
        # self.view.setStyleSheet("""border: 0px;""")
        self.body_layout.addWidget(self.view)

        self.main.setCentralWidget(self.body)

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
