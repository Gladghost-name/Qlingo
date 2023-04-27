from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore


class BaseWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.widget_content = []

    def setWidget(self, w):
        self.widget_content.append(w)
        w.setParent(self)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # print(self.widget_content)
        for widget in self.widget_content:
            widget.resize(400, 400)
        return super().paintEvent(a0)


class LabelBase(QLabel):
    def __init__(self):
        super().__init__()

    def setBackgroundColor(self, color):
        style = self.styleSheet()
        style += f"""background-color: {color}"""
        self.setStyleSheet(style)

    def addWidget(self, w):
        self.vbox.addWidget(w)


class Image(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)

    def setBackgroundColor(self, color):
        style = self.styleSheet()
        style += f"""background-color: {color}"""
        self.setStyleSheet(style)


class TextEdit(QTextEdit):
    def __int__(self):
        super().__init__()

    def setBackgroundColor(self, color):
        style = self.styleSheet()
        style += f"""background-color: {color}"""
        self.setStyleSheet(style)


class TextInput(QLineEdit):
    def __init__(self):
        super().__init__()

    def setBackgroundColor(self, color):
        style = self.styleSheet()
        style += f"""background-color: {color}"""
        self.setStyleSheet(style)


class Widget(QWidget):
    def __init__(self):
        super().__init__()

    def setBackgroundColor(self, color):
        style = self.styleSheet()
        style += f"""background-color: {color}"""
        self.setStyleSheet(style)


class Label(QLabel):
    def __init__(self):
        super().__init__()
        # self.content = LabelBase()
        # self.text = ''
        self.font = ''

        self.text_x = 0
        self.text_y = 0

        self.rotate = 0

        self.textalign = 'center'

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

    def setBackgroundColor(self, color):
        style = self.styleSheet()
        style += f"""background-color: {color}"""
        self.setStyleSheet(style)

    def addWidget(self, w):
        self.vbox.addWidget(w)

    def capitalize(self, b):
        if b:
            self.setText(self.text().upper())


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.frame = QFrame()
        self.vbox = QVBoxLayout()
        self.frame.setLayout(self.vbox)

        # self.cool_label = 400

        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)

        self.setCentralWidget(self.frame)

    def addWidget(self, w):
        self.vbox.addWidget(w)


class BoxLayout(QFrame):
    def __init__(self) -> None:
        super().__init__()
        # create a list of widgets.
        self.contents = []

        # define all the margins.
        self.bottom_margin = 5
        self.top_margin = 5
        self.left_margin = 5
        self.right_margin = 5

        # all total widget positions
        self.total_x = 0
        self.total_y = 0

        # get the current viewing window
        self.win = self.window()

        # self.window()
        self.spacing = 5

        # maximum repositions.
        self.max_y = 0
        self.max_x = 0

        # setting the default orientation.
        self.orientation = 'vertical'

    def addWidget(self, e):
        # add a widget to the layout.
        self.contents.append(e)

        # show the widget on the screen.
        e.setParent(self)
        e.show()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # update the widgets on the window.

        # default all the values to 0;
        self.total_y = 0
        self.total_x = 0
        self.max_y = 0

        for widget in self.contents:
            # reposition the widgets in appropriate positions.
            # print(widget)
            if self.orientation == 'vertical':
                widget.move((self.rect().x() + self.left_margin + self.total_x),
                            (self.rect().y() + self.top_margin + (self.total_y)))
                widget.resize(self.rect().width() - (self.right_margin + self.left_margin),
                              int((self.rect().height() - (self.bottom_margin + self.top_margin)) / len(
                                  self.contents)) - (int(self.spacing / 2)))
                self.total_y += widget.rect().height() + self.spacing
                self.max_y += widget.minimumHeight() + self.spacing
                self.max_x += widget.minimumWidth()
            elif 'horizontal':
                widget.move((self.rect().x() + self.left_margin + self.total_x),
                            (self.rect().y() + self.top_margin + (self.total_y)))
                widget.resize(
                    int((self.rect().width() - (self.right_margin + self.left_margin)) / len(self.contents)) - (
                            self.right_margin - self.spacing) * 2,
                    int((self.rect().height() - (self.bottom_margin + self.top_margin))))
                self.total_x += widget.rect().width() + self.spacing
                self.max_y += widget.minimumHeight() + self.spacing
                self.max_x += widget.minimumWidth()
            else:
                print(F'UNKNOWN ORIENTATION: "{self.orientation}"')
                # self.orientation = VERTICAL
        # set the size of the minwidth and minheight.
        # self.win.setMinimumHeight((self.max_y + self.spacing)* 3 + self.bottom_margin + self.top_margin)
        # self.win.setMinimumWidth((self.max_x + (self.left_margin + self.right_margin)+28))
        return super().paintEvent(a0)

    def setMargin(self, left, top, right, bottom):
        # set the margins for the layout.
        self.top_margin = top
        self.left_margin = left
        self.right_margin = right
        self.bottom_margin = bottom

    def setSpacing(self, spacing):
        # set spacing of widgets.
        self.spacing = spacing
        self.update()

    def setOrientation(self, orient: str = ...):
        self.orientation = orient

    def setBackgroundColor(self, color):
        style = self.styleSheet()
        style += f"""background-color: {color}"""
        self.setStyleSheet(style)


class BaseFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.vbox = BoxLayout()
        self.vbox.setParent(self)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.vbox.setFixedSize(self.rect().size())
        return super().paintEvent(a0)


class Frame(BaseFrame):
    def __init__(self):
        super().__init__()

    def addWidget(self, w):
        self.vbox.addWidget(w)

    def setBackgroundColor(self, color):
        style = self.styleSheet()
        style += f"""background-color: {color}"""
        self.setStyleSheet(style)


class GraphicsItem(QFrame):
    def __init__(self):
        super().__init__()
        self.bg = 'grey'
        self.opacity = 1
        self.setStyleSheet("""background-color: transparent;""")
        self.x = self.rect().top()
        self.y = self.rect().left()

    def moveby(self, x, y):
        self.x = x
        self.y = y
        self.update()

    def setOpacity(self, opacity):
        self.opacity = opacity
        self.update()


class Text(GraphicsItem):
    color = 'white'
    font_size = 32
    font_weight = 100
    font_family = "Calibri"
    italic = False
    align = Qt.AlignCenter

    def __int__(self):
        super().__init__()
        self.text = 'New Text'

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.painter = QPainter(self)

        self.painter.setPen(QPen(QColor(self.color)))
        self.painter.setFont(QFont(self.font_family, self.font_size, self.font_weight, self.italic))

        self.painter.drawText(self.rect(), self.align, self.text)

        self.setFixedSize(QSize(self.painter.font().pointSize() * len(self.text), self.painter.font().pointSize() * 2))

        self.painter.end()

    def setText(self, text):
        self.text = text
        self.update()

    def setTextColor(self, color):
        self.color = color
        self.update()

    def setFontSize(self, size):
        self.font_size = size
        self.update()

    def setFontWeight(self, weight):
        self.font_weight = weight
        self.update()

    def setFontFamily(self, family):
        self.font_family = family
        self.update()

    def setItalic(self, b):
        if b:
            self.italic = True
        else:
            self.italic = False
    def setAlignment(self, alignment):
        self.align = alignment
        self.update()


class Rectangle(GraphicsItem):
    def __init__(self):
        super().__init__()
        # self.bg = 'grey'

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.painter = QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.new_bg = self.bg.replace('rgba(', '')
        self.new_bg = self.new_bg.replace(")", '')

        # print(self.new_bg.split(','))
        if len(self.new_bg.split(',')) > 1:
            # if type(self.new_bg.split(',')) == list:
            self.new_bg = self.new_bg.split(',')
            # print(self.bg)
            self.painter.setBrush(
                QColor(int(self.new_bg[0]), int(self.new_bg[1]), int(self.new_bg[2]), int(self.new_bg[3])))
        else:
            self.painter.setBrush(QColor(self.bg))
        self.painter.setPen(QPen(Qt.NoPen))

        self.painter.setOpacity(self.opacity)

        self.painter.drawRect(QRectF(self.x, self.y, self.rect().width(), self.rect().height()))
        self.painter.end()
        return super().paintEvent(a0)

    def setBackgroundColor(self, color):
        self.bg = color
        self.update()


class Ellipse(GraphicsItem):
    def __init__(self):
        super().__init__()
        # self.bg = 'grey'

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.painter = QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.new_bg = self.bg.replace('rgba(', '')
        self.new_bg = self.new_bg.replace(")", '')

        # print(self.new_bg.split(','))
        if len(self.new_bg.split(',')) > 1:
            # if type(self.new_bg.split(',')) == list:
            self.new_bg = self.new_bg.split(',')
            # print(self.bg)
            self.painter.setBrush(
                QColor(int(self.new_bg[0]), int(self.new_bg[1]), int(self.new_bg[2]), int(self.new_bg[3])))
        else:
            self.painter.setBrush(QColor(self.bg))
        self.painter.setPen(QPen(Qt.NoPen))

        self.painter.setOpacity(self.opacity)

        self.painter.drawEllipse(QRectF(self.x, self.y, self.rect().width(), self.rect().height()))
        self.painter.end()
        return super().paintEvent(a0)

    def setBackgroundColor(self, color):
        self.bg = color
        self.update()


class Triangle(GraphicsItem):
    def __init__(self):
        super().__init__()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.painter = QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.new_bg = self.bg.replace('rgba(', '')
        self.new_bg = self.new_bg.replace(")", '')

        # print(self.new_bg.split(','))
        if len(self.new_bg.split(',')) > 1:
            # if type(self.new_bg.split(',')) == list:
            self.new_bg = self.new_bg.split(',')
            # print(self.bg)
            self.painter.setBrush(
                QColor(int(self.new_bg[0]), int(self.new_bg[1]), int(self.new_bg[2]), int(self.new_bg[3])))
        else:
            self.painter.setBrush(QColor(self.bg))
        self.painter.setPen(QPen(Qt.NoPen))

        self.painter.setOpacity(self.opacity)

        self.painter.drawPolygon(QPolygonF([QPointF(self.rect().width() / 2, 0), QPointF(0, self.rect().height()),
                                            QPointF(self.rect().width(), self.rect().height())]))
        self.painter.end()
        return super().paintEvent(a0)

    def setBackgroundColor(self, color):
        self.bg = color
        self.update()


class RoundedRect(GraphicsItem):
    def __init__(self):
        super().__init__()
        # self.bg = 'grey'
        self.radius = (1, 1)
        self.x = self.rect().top()
        self.y = self.rect().left()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.painter = QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.new_bg = self.bg.replace('rgba(', '')
        self.new_bg = self.new_bg.replace(")", '')

        # print(self.new_bg.split(','))
        if len(self.new_bg.split(',')) > 1:
            # if type(self.new_bg.split(',')) == list:
            self.new_bg = self.new_bg.split(',')
            # print(self.bg)
            self.painter.setBrush(
                QColor(int(self.new_bg[0]), int(self.new_bg[1]), int(self.new_bg[2]), int(self.new_bg[3])))
        else:
            self.painter.setBrush(QColor(self.bg))
        self.painter.setPen(QPen(Qt.NoPen))

        self.painter.setOpacity(self.opacity)

        self.painter.drawRoundedRect(QRectF(self.x, self.y, self.rect().width(), self.rect().height()), self.radius[0],
                                     self.radius[1])
        self.painter.end()
        return super().paintEvent(a0)

    def setBackgroundColor(self, color):
        self.bg = color
        self.update()

    def setRadius(self, radius):
        self.radius = (radius, radius)

    def setRadiusX(self, radius_x):
        self.radius = (radius_x, self.radius[1])

    def setRadiusY(self, radius_y):
        self.radius = (self.radius[1], radius_y)


class Line(GraphicsItem):
    def __init__(self):
        super().__init__()
        self.points = [[-self.rect().width(), self.rect().top()], [self.rect().width(), self.rect().height()]]

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.painter = QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.new_bg = self.bg.replace('rgba(', '')
        self.new_bg = self.new_bg.replace(")", '')

        # print(self.new_bg.split(','))
        if len(self.new_bg.split(',')) > 1:
            # if type(self.new_bg.split(',')) == list:
            self.new_bg = self.new_bg.split(',')
            # print(self.bg)
            self.painter.setPen(
                QColor(int(self.new_bg[0]), int(self.new_bg[1]), int(self.new_bg[2]), int(self.new_bg[3])))
        else:
            self.painter.setPen(QColor(self.bg))
        # self.painter.setPen(QPen(Qt.NoPen))

        self.painter.setOpacity(self.opacity)

        self.painter.drawLine(self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1])
        self.painter.end()
        return super().paintEvent(a0)

    def setPoints(self, x1, y1, x2, y2):
        self.points = [[x1, y1], [x2, y2]]
        self.update()

    def setBackgroundColor(self, color):
        self.bg = color
        self.update()


class Panel(QFrame):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.default_cursor = Qt.ArrowCursor
        self.draggable = False
        self.pressed = False

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.x() >= self.rect().width() - 3:
            self.setCursor(Qt.SizeHorCursor)
            self.draggable = True
        else:
            self.draggable = False
            self.setCursor(self.default_cursor)

        if self.pressed:
            self.setFixedWidth(a0.x())

    def setBackgroundColor(self, color):
        style = self.styleSheet()
        style += f"""background-color: {color}"""
        self.setStyleSheet(style)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.draggable:
            self.pressed = True
            self.draggable = False

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.pressed = False
        self.update()


class Button(QPushButton):
    def __init__(self):
        super().__init__()

    def setBackgroundColor(self, color):
        style = self.styleSheet()
        style += f"""background-color: {color}"""
        self.setStyleSheet(style)

    def capitalize(self, b):
        if b:
            self.setText(self.text().upper())