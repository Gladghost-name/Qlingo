from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import *


class Rectangle(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.inherited_widget = None
        self.gizmo = None
        self.x = self.rect().x()
        self.y = self.rect().y()
        self.width = self.rect().width()
        self.height = self.rect().height()
        self.setBrush(QColor('black'))
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        # self.setBrush(QColor('black'))

    def paint(self, painter, option, widget):
        is_selected = option.state & QStyle.State_Selected
        # Remove default paint from selection
        self.x = self.rect().x()
        self.y = self.rect().y()
        self.width = self.rect().width()
        self.height = self.rect().height()
        option.state &= ~QStyle.State_Selected
        super().paint(painter, option, widget)


class Ellipse(QGraphicsEllipseItem):
    def __init__(self):
        super().__init__()

        self.inherited_widget = None

        self.gizmo = None
        self.new_gizmo = None
        self.hidden_check = False
        self.c_x = 0
        self.c_y = 0
        # self.setRotation()
        # self.setTransformOriginPoint()
        self.x = self.rect().x()
        self.y = self.rect().y()
        self.width = self.rect().width()
        self.height = self.rect().height()
        self.setBrush(QColor('black'))
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)

    def paint(self, painter, option, widget):
        is_selected = option.state & QStyle.State_Selected
        # Remove default paint from selection
        self.x = self.rect().x()
        self.y = self.rect().y()
        self.width = self.rect().width()
        self.height = self.rect().height()

        option.state &= ~QStyle.State_Selected
        super().paint(painter, option, widget)
    def setView(self, view):
        self.view = view

class Text(QGraphicsTextItem):
    def __init__(self):
        super().__init__()
        self.inherited_widget = None
        self.gizmo = None
        self.x = self.pos().x()
        self.y = self.pos().y()
        self.width = self.boundingRect().width()
        self.height = self.boundingRect().height()
        self.grabKeyboard()
        self.grabMouse()
        # self.update()
        self.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextEditable | Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        # self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsMovable)

    def paint(self, painter, option, widget):
        is_selected = option.state & QStyle.State_Selected
        # Remove default paint from selection
        self.x = self.pos().x()
        self.y = self.pos().y()
        self.width = self.boundingRect().width()
        self.height = self.boundingRect().height()
        option.state &= ~QStyle.State_Selected
        super().paint(painter, option, widget)


class Pixmap(QGraphicsPixmapItem):
    def __init__(self):
        super().__init__()
        self.inherited_widget = None
        self.gizmo = None

        self.x = self.pos().x()
        self.y = self.pos().y()
        self.width = 100
        self.height = 100
        self.file_name = None

        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)

    def paint(self, painter, option, widget):
        is_selected = option.state & QStyle.State_Selected
        # Remove default paint from selection
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        self.x = self.pos().x()
        self.y = self.pos().y()
        self.width = self.pixmap().width()
        self.height = self.pixmap().height()
        option.state &= ~QStyle.State_Selected
        super().paint(painter, option, widget)

    def setRect(self, rect):
        if rect.width() != self.width:
            # adding and scaling the image with smooth pixel transformation.
            self.setPixmap(QPixmap(self.file_name).scaled(int(rect.width()), int(rect.height()), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.width = self.pixmap().width()
            self.height = self.pixmap().height()
        self.setPos(rect.x(), rect.y())
        self.update()

    def rect(self):
        return QRectF(self.x, self.y, self.width, self.height)


class Entity():
    def __init__(self, scene, type: str = ..., size: tuple = ..., pos: tuple = ..., color: str = 'black',
                 pen_color: str = 'black', filename: str = 'obj-edit.png'):
        super().__init__()
        self.scene = scene
        self.type = type
        self.size = size
        self.pos = pos
        self.pen_color = pen_color
        self.color = color
        self.filename = filename

    def draw(self):
        match self.type:
            case "rectangle":
                self.item = Rectangle()
                self.item.setPen(QColor(self.pen_color))
                self.item.setBrush(QColor(self.color))
                self.item.setRect(self.pos[0], self.pos[1], self.size[0], self.size[1])
                self.scene.addItem(self.item)
            case "ellipse":
                self.item = Ellipse()
                self.item.setPen(QColor(self.pen_color))
                self.item.setBrush(QColor(self.color))
                self.item.setRect(self.pos[0], self.pos[1], self.size[0], self.size[1])
                self.scene.addItem(self.item)
            case "pixmap":
                self.item = Pixmap()
                self.item.file_name = self.filename
                self.item.setPixmap(QPixmap(self.filename))
                self.scene.addItem(self.item)
                self.item.setRect(QRectF(self.pos[0], self.pos[1], self.size[0], self.size[1]))
            case "text":
                self.item = Text()
                self.item.setHtml('<h1>Text</h1>')
                self.scene.addItem(self.item)
        self.item.setCursor(Qt.SizeAllCursor)
