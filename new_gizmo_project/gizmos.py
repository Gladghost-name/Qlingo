from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.Qt import *
from components import Pixmap


class RectGizmo(QFrame):
    def __init__(self, scene, gizmos_list, items, paste_objects):
        super().__init__()
        self.setStyleSheet("""background-color: transparent;""")
        self.item = None
        self.all_items = items

        self.objects_to_paste = paste_objects
        self.start_rotation = False

        self.object_move_speed = 10

        self.proportional = False
        self.scene = scene
        self.hidden_check = False
        # self.setWindowOpacity(0.0)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)

        self.dragging = 'None'
        self.list = gizmos_list
        self.cur = Qt.SizeAllCursor
        self.cur_x = 0
        self.cur_y = 0
        self.setMouseTracking(True)
        self.dragging = 'None'
        self.pressed = False
        self.directer = QLabel(self)
        # self.directer.setStyleSheet("""border: 2px;""")
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
            self.dup_annual_x += self.item.rect().x() - self.item.inherited_widget.rect().x()
            self.dup_annual_y += self.item.rect().y() - self.item.inherited_widget.rect().y()
        self.new_item = type(self.item)()
        # print(self.new_item)
        self.new_item.inherited_widget = self.item
        if type(self.item) != Pixmap:
            self.new_item.setBrush(self.item.brush())
            self.new_item.setPen(self.item.pen())
        else:
            self.new_item.setPixmap(QPixmap(self.item.file_name))
            self.new_item.file_name = self.item.file_name
        self.new_item.setRect(
            QRectF(self.item.x + self.dup_annual_x, self.item.y + self.dup_annual_y, self.item.width, self.item.height))
        self.item.scene().addItem(self.new_item)

        if self.item.inherited_widget is None:
            self.dup_annual_x += 20
            self.dup_annual_y += 20

        # self.hide()
        # self.item.scene().clearSelection()
        self.item.scene().setFocusItem(self.new_item)
        self.item.scene().update()
        self.update()

    def setItem(self, item):
        self.item = item
        # self.item.setParentItem(self)
        # self.setParent(self.item)
        self.item.gizmo = self
        self.cur_x = self.item.x - self.node_size / 2
        self.cur_y = self.item.y - self.node_size / 2

        # print(self.item)
        # print(self.cur_x, self.cur_y)

        self.move(int(self.cur_x), int(self.cur_y))
        self.setFixedSize(int(self.item.width + self.node_size),
                          int(self.item.height + self.node_size))

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.painter = QPainter(self)

        self.move(int(self.cur_x), int(self.cur_y))
        # self.setFixedSize(int(self.item.rect().size().width() + self.node_size),
        #                   int(self.item.rect().size().height() + self.node_size))
        self.setFixedSize(int(self.item.width + self.node_size),
                          int(self.item.height + self.node_size))

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
            # self.item.setCursor(Qt.SizeAllCursor)

        if self.pressed:
            for item in self.all_items:
                # self.setCursor(Qt.CrossCursor)
                self.move_x = item.gizmo.pos_x
                self.move_y = item.gizmo.pos_y
                if self.cur_dragging == 'bottomRight':
                    if self.start_rotation == True:
                        item.setTransformOriginPoint(item.x+item.width, item.y+item.height)
                        item.setRotation(a0.y()-item.width)
                        item.update()
                        self.update()
                        item.scene().update()
                    else:
                        if self.proportional:
                            item.setRect(QRectF(item.rect().x(), item.rect().y(), self.move_y, self.move_y))
                        else:
                            item.setRect(QRectF(item.rect().x(), item.rect().y(), self.move_x, self.move_y))
                        self.update()
                        item.scene().update()
                elif self.cur_dragging == 'right':
                    item.setRect(
                        QRectF(item.rect().x(), item.rect().y(), self.move_x, item.rect().height()))
                    self.update()
                    item.scene().update()
                elif self.cur_dragging == 'left':
                    # self.item.rect().setLeft(a0.x())
                    self.rec = QRectF(item.rect())
                    self.new_rect = self.rec.adjusted(-(item.gizmo.pos_x - a0.x()), 0, 0, 0)
                    item.setRect(self.new_rect)
                    item.update()
                    self.update()
                    item.scene().update()
                elif self.cur_dragging == 'bottomLeft':
                    # self.item.rect().setLeft(a0.x())
                    if self.start_rotation == True:
                        item.setTransformOriginPoint(item.x, item.y+item.height)
                        item.setRotation(a0.y()-item.width)
                        item.update()
                        self.update()
                        item.scene().update()
                    else:
                        self.rec = QRectF(item.rect())
                        if self.proportional:
                            self.new_rect = self.rec.adjusted((item.gizmo.pos_y - a0.y()), 0, 0,
                                                              -(item.gizmo.pos_y - a0.y()))
                        else:
                            self.new_rect = self.rec.adjusted(-(item.gizmo.pos_x - a0.x()), 0, 0,
                                                              -(item.gizmo.pos_y - a0.y()))
                        item.setRect(self.new_rect)
                        item.update()
                        self.update()
                        item.scene().update()
                elif self.cur_dragging == 'topLeft':
                    if self.start_rotation == True:
                        item.setTransformOriginPoint(item.x, item.y)
                        item.setRotation(a0.y())
                        item.update()
                        self.update()
                        item.scene().update()
                    else:
                        self.rec = QRectF(item.rect())
                        if self.proportional:
                            self.new_rect = self.rec.adjusted(-(item.gizmo.pos_y - a0.y()), -(item.gizmo.pos_y - a0.y()), 0,
                                                              0)
                        else:
                            self.new_rect = self.rec.adjusted(-(item.gizmo.pos_x - a0.x()), -(item.gizmo.pos_y - a0.y()), 0,
                                                              0)
                        item.setRect(self.new_rect)
                        item.update()
                        self.update()
                        item.scene().update()
                elif self.cur_dragging == 'topRight':
                    if self.start_rotation == True:
                        item.setTransformOriginPoint(item.x+item.width, item.y)
                        item.setRotation(a0.y())
                        item.update()
                        self.update()
                        item.scene().update()
                    else:
                        self.rec = QRectF(item.rect())
                        if self.proportional:
                            self.new_rect = self.rec.adjusted(0, -(item.gizmo.pos_y - a0.y()), (item.gizmo.pos_y - a0.y()),
                                                              0)
                        else:
                            self.new_rect = self.rec.adjusted(0, -(item.gizmo.pos_y - a0.y()), -(item.gizmo.pos_x - a0.x()),
                                                              0)
                        item.setRect(self.new_rect)
                        item.update()
                        self.update()
                        item.scene().update()
                elif self.cur_dragging == 'bottom':
                    item.setRect(
                        QRectF(item.rect().x(), item.rect().y(), item.rect().width(), item.gizmo.move_y))
                    self.update()
                    item.scene().update()
                elif self.cur_dragging == 'center':
                    # for item in self.all_items:
                    self.rec = QRectF(item.rect())
                    self.new_rect = self.rec.translated(-(item.gizmo.pos_x - a0.x()), -(item.gizmo.pos_y - a0.y()))

                    item.setRect(self.new_rect)
                    # self.coord_label.move(int(a0.x()), int(a0.y()))

                    self.pressed = True
                    item.gizmo.update()

                    # self.coord_label.show()
                    # self.coord_label.setText(f'x: {item.x} y: {item.y}')

                    item.update()
                    item.scene().update()
                elif self.cur_dragging == 'top':
                    self.rec = QRectF(item.rect())
                    self.new_rect = self.rec.adjusted(0, -(item.gizmo.pos_y - a0.y()), 0, 0)
                    item.setRect(self.new_rect)
                    item.update()
                    self.update()
                    item.scene().update()
                item.gizmo.pos_x = a0.x()
                item.gizmo.pos_y = a0.y()
                self.update()

    def mousePressEvent(self, a0):
        if a0.button() == Qt.LeftButton:
            self.pos_x = a0.x()
            self.pos_y = a0.y()
            # print(self.scene.itemAt(a0.x(), a0.y(), self.item.view.transform()), self)
            # print(type(self.scene.itemAt(a0.x(), a0.y(), self.item.view.transform())))

            if self.dragging != 'None':
                if self.dragging != 'center':
                    self.item.setOpacity(.5)
                # else:
                # if type(self.scene.itemAt(a0.x(), a0.y(), self.item.view.transform())) == QGraphicsProxyWidget:
                #     self.item.hidden_check = True
                #     self.item.c_x = a0.x()
                #     self.item.c_y = a0.y()
                #     self.pressed = True
                #     self.item.new_gizmo = self
                #     self.hide()
                #     self.item.update()
                for i in self.all_items:
                    i.gizmo.pressed = True
                    if i is not self.item:
                        i.gizmo.pos_x = a0.x()
                        i.gizmo.pos_y = a0.y()
                        i.gizmo.cur_width = i.rect().width()
                        i.gizmo.cur_dragging = self.dragging
                        i.gizmo.update()
                        i.update()
                # self.pressed = True
                self.cur_width = self.item.width
                self.cur_dragging = self.dragging
            self.update()

    def mouseReleaseEvent(self, a0):
        # self.show()
        if a0.button() == Qt.LeftButton:
            for item in self.all_items:
                self.pressed = False
                item.setOpacity(1)
                self.setFixedSize(int(item.rect().size().width() + 15), int(item.rect().size().height() + 15))
                self.hide()
                self.new_frame = RectGizmo(self.scene, item.gizmo.list, item.gizmo.all_items,
                                           item.gizmo.objects_to_paste)
                self.gizmos.append(self.new_frame)
                self.new_frame.setItem(item)
                item.scene().addWidget(self.new_frame)
                item.gizmo.update()
                # item.gizmo.update()
                item.scene().update()
                item.gizmo.list.append(self.new_frame)
                if self in item.gizmo.list:
                    self.list.remove(self)
                self.deleteLater()
                # item.gizmo.deleteLater()
            self.update()
            # self.coord_label.hide()

    def close_all(self):
        for widget in self.list:
            widget.deleteLater()

    def handle_movement(self, a0):
        if a0.key() == Qt.Key_Right:
            self.rec = QRectF(self.item.rect())
            self.new_rect = self.rec.translated(self.object_move_speed, 0)
            self.item.setRect(self.new_rect)

            self.hide()

            self.new_frame = RectGizmo(self.scene, self.list, self.all_items, self.objects_to_paste)
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

            self.new_frame = RectGizmo(self.scene, self.list, self.all_items, self.objects_to_paste)
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

            self.new_frame = RectGizmo(self.scene, self.list, self.all_items, self.objects_to_paste)
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

            self.new_frame = RectGizmo(self.scene, self.list, self.all_items, self.objects_to_paste)
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

        self.new_frame = RectGizmo(self.scene, self.list, self.all_items, self.objects_to_paste)
        self.list.append(self.new_frame)
        self.new_frame.setItem(item)
        item.scene().addWidget(self.new_frame)

        self.new_frame = RectGizmo(self.scene, self.list, self.all_items, self.objects_to_paste)
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
        if a0.key() == Qt.Key_Control:
            self.start_rotation = True
