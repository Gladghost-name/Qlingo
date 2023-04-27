# Use pprint to print data with style!.
from qlingo.parser import *
from qlingo.wid.widgets import *
from qlingo.langvals.vals import *


class Compiler():
    def __init__(self, filename):
        try:
            self.parser = Parse(filename)
            appData = self.parser.parse()
            # except PermissionError as p:
            #     print(p)
            cell = []
            self.properties = []
            self.others_list = []
            self.new_list = []
            self.child_total = 0
            self.window_contents = []
            self.compiled = []
            # This is just for a test run.
            # app = QApplication(sys.argv)
            for data in appData:
                children = []
                for contents in data:
                    name = contents
                    content = data[contents]
                    if content['type'] != 'property':
                        new_name = self.parser.filler(name)
                        if new_name != "Window":
                            try:
                                widget = eval(new_name)()
                                for child in content['children']:
                                    if self.parser.is_class(child):
                                        children.append(child)
                                    else:
                                        children.append(child)
                                new_dict = {
                                    widget: {"children": children, "line_no": content['line_no'], "type": "class",
                                             "name": name}}
                                # print(new_dict)
                                self.others_list.append(new_dict)
                            except NameError as name:
                                print(name)
                        else:
                            self.top_class_line_no = content['line_no']
                            self.top_class_name = new_name
                            self.top_class_raw_name = name
                            self.top_window_content = data
                    else:
                        if name in properties:
                            # print(data)
                            self.properties.append(data)
                        else:
                            print(f'[ERROR] No property named "{name}".')

            for new_order in self.others_list:
                self.new_children = []
                # print(new_order)
                for data in new_order:
                    class_order = new_order[data]
                    # print(class_order)
                    for child in class_order['children']:
                        if self.parser.is_class(child) == True:
                            for more_children in self.others_list:
                                for context in more_children:
                                    names = more_children[context]['name']
                                    if names == child:
                                        self.new_children.append(context)
                        else:
                            for property in self.properties:
                                for prop in property:

                                    identifier = property[prop]['actual-name']
                                    if child == identifier:
                                        self.new_children.append(property)
                new_dict = {data: {"children": self.new_children, "line_no": class_order['line_no'], "type": "class",
                                   "name": class_order['name']}}
                # print(new_dict)

                self.new_list.append(new_dict)

            for top_class_data in self.top_window_content:
                class_data = self.top_window_content[top_class_data]
                for master_children in class_data['children']:
                    if self.parser.is_class(master_children) == True:
                        for more_children in self.new_list:
                            for context in more_children:
                                names = more_children[context]['name']
                                if names == master_children:
                                    self.child_total += 1
                                    if self.child_total < len(class_data['children']) - 1:
                                        self.window_contents.append(context)
                    else:
                        for property in self.properties:
                            for prop in property:
                                identifier = property[prop]['actual-name']
                                if master_children == identifier:
                                    self.window_contents.append(property)
                window_class = eval(self.top_class_name)()
                new_window_iter = {window_class: {"children": self.window_contents, "line_no": self.top_class_line_no,
                                                  "type": "master-class", "name": self.top_class_raw_name}}
                self.compiled.append(new_window_iter)
            for item in self.new_list:
                self.compiled.append(item)
        except PermissionError as p:
            print(p)

    def compile(self):
        return self.compiled