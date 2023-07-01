from Qlingo.lingo.langvals.vals import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from Qlingo.lingo.wid.widgets import *


class PropHandler:
    def __init__(self) -> None:
        self.properties = properties

    def inherit_prop(self, widget, prop):
        for p in prop:
            self._prop = prop[p]
            self.prop_value = self._prop['value']
            self._prop_value_type = self._prop['value-type']
            self._prop_value_name = p
            self.line_number = self._prop['line_no']
        if self._prop_value_type == 'STRING':
            self.prop_value = str(self.prop_value)
        elif self._prop_value_type == 'INT':
            self.prop_value = int(self.prop_value)
            # widget.setText(int(self.prop_value))
        elif self._prop_value_type == 'FUNCTION':
            # print(widget.window())
            filtered = self.prop_value.replace('root', 'widget.parent()')
            filtered = filtered.replace('self', 'widget')

            total_filtered = self.prop_value.replace('root.', '')
            try:
                self.prop_value = eval(filtered)
            except:
                print(f"""[ERROR] root widget as no attribute "{total_filtered}" in line {self.line_number};""")
            # widget.setText(str(eval(filtered)))
        elif self._prop_value_type == "BOOL":
            real_value = self.prop_value[0].upper() + self.prop_value[1:]
            self.prop_value = real_value
            if self.prop_value == 'True':
                self.prop_value = True
            elif self.prop_value == 'False':
                self.prop_value = False
        elif self._prop_value_type == "RUN_FUNCTION":
            eval(self.prop_value)
        # print(widget, prop, self.prop_value)
        try:
            match self._prop_value_name:
                case "orientation":
                    widget.setOrientation(self.prop_value)
                case "text_align":
                    if self.prop_value == 'center':
                        widget.setAlignment(Qt.AlignCenter)
                    elif self.prop_value == 'right':
                        widget.setAlignment(Qt.AlignRight)
                    elif self.prop_value == 'left':
                        widget.setAlignment(Qt.AlignLeft)
                    elif self.prop_value == 'top':
                        widget.setAlignment(Qt.AlignTop)
                    elif self.prop_value == 'bottom':
                        widget.setAlignment(Qt.AlignBottom)
                case "radius":
                    widget.setRadius(self.prop_value)
                case "radius_x":
                    widget.setRadiusX(self.prop_value)
                case "radius_y":
                    widget.setRadiusY(self.prop_value)
                case "text":
                    widget.setText(self.prop_value)
                case "background_color":
                    if "Window" in str(type(widget)):
                        widget.new_frame.setBackgroundColor(self.prop_value)
                    else:
                        widget.setBackgroundColor(self.prop_value)
                case "spacing":
                    widget.setSpacing(int(self.prop_value))
                case "color":
                    widget.setTextColor(str(self.prop_value))
                case "font_family":
                    widget.setFontFamily(str(self.prop_value))
                case "font_weight":
                    widget.setFontWeight(int(self.prop_value))
                case "font_size":
                    widget.setFontSize(int(self.prop_value))
                case "italic":
                    widget.setItalic(bool(self.prop_value))
                case "width":
                    # print(str(self.prop_value) + '2')
                    widget.setFixedWidth(int(self.prop_value))
                case "height":
                    widget.setFixedHeight(int(self.prop_value))
                case "min_width":
                    # print('yes')
                    widget.setMinimumWidth(int(self.prop_value))
                case "min_height":
                    # print('yes')
                    widget.setMinimumHeight(int(self.prop_value))
                case "title":
                    # print('yes')
                    widget.setWindowTitle(str(self.prop_value))
                case "hidden":
                    # print('yes')
                    widget.setHidden(self.prop_value)
                case "capitalize":
                    widget.capitalize(self.prop_value)
                case 'style':
                    widget.setStyleSheet(self.prop_value)
                case "maximize":
                    # print('yes')
                    if bool(self.prop_value) == True:
                        widget.showMaximized()
                case "minimize":
                    # print('yes')
                    if bool(self.prop_value) == True:
                        widget.showMinimized()
                case "fullscreen":
                    # print('yes')
                    if bool(self.prop_value) == True:
                        widget.showFullScreen()
                case "frameless":
                    if bool(self.prop_value) == True:
                        widget.setWindowFlags(Qt.WindowType.FramelessWindowHint)
                case "app_icon":
                    # print()
                    widget.setWindowIcon(QIcon(f"""{self.prop_value.strip('"')}"""))
                case "icon":
                    path = str(self.prop_value).strip('"')
                    widget.setIcon(QIcon(str(f"""{path}""")))
                case "source":
                    path = str(self.prop_value).strip('"')
                    width = widget.size().width()
                    height = widget.size().height()
                    widget.setPixmap(QPixmap(path).scaled(width, height, Qt.KeepAspectRatio))
                case "x":
                    widget.move(int(self.prop_value), widget.pos().y())
                case "y":
                    widget.move(widget.pos().x(), int(self.prop_value))
                case 'name':
                    widget.setObjectName(str(self.prop_value))
                case "line_points":
                    self.prop_value = self.prop_value.split(',')
                    widget.setPoints(int(self.prop_value[0]), int(self.prop_value[1]), int(self.prop_value[2]), int(self.prop_value[3]))
                case "styles":
                    # print(widget)
                    f = open(str(self.prop_value), 'r+')
                    widget.setStyleSheet(f.read())
                    # widget.styles = self.prop_value
                    # widget.style_content = f.read()
                case "margin":
                    self.prop_value = self.prop_value.split(',')
                    # for value in self.prop_value:
                    widget.setMargin(int(self.prop_value[0]), int(self.prop_value[1]), int(self.prop_value[2]), int(self.prop_value[3]))
                case "pos":
                    self.prop_value = self.prop_value.split(',')
                    widget.move(int(self.prop_value[0]), int(self.prop_value[1]))
                case "size":
                    self.prop_value = self.prop_value.split(',')
                    widget.setFixedSize(int(self.prop_value[0]), int(self.prop_value[1]))
                case "opacity":
                    widget.setOpacity(self.prop_value)
                case _:
                    print(f'no property named "{self.prop_type}"')
        except AttributeError as a:
            print(a)

    def is_function(self, value):
        if value.endswith("()"):
            return True
        else:
            return False

    def filter_out(self, code):
        code = code.replace('self', 'widget')
        return code