from Qlingo.lingo.parser import *
import sys
from Qlingo.lingo.wid.widgets import *
from Qlingo.lingo.compiler import *
from Qlingo.lingo.handlers.prop_handler import *

class Runner():
    def __init__(self):
        # creating an app class to handle the widgets!
        # self.app = QApplication(sys.argv)
        self.master_class = None
    def run(self, filename):
        try:
            self.compiler = Compiler(filename)
        except AttributeError as a:
            print(a)
        self.prop_handler = PropHandler()
        new_child = 0
        try:
            for compiled in self.compiler.compile():
                for com in compiled:
                    contents = compiled[com]
                    children = contents['children']
                    name = contents['name']
                    if contents['type'] == 'master-class':
                        self.master_class = com
                        self.master_children = children
                    for child in children:
                        if str(child).startswith('<'):
                            com.addWidget(child)
                        else:
                            if contents['type'] != 'master-class':
                                self.handle_properties(child, com)
        except:
            print("Empty file detected!.")

        # A Window Test!
        # self.master_class.resize(950, 700)
        # self.master_class.show()
        # sys.exit(self.app.exec_())
    def handle_properties(self, prop, widget):
        self.prop_handler.inherit_prop(widget, prop)

# To start a simple build!.
# runner = Runner()
# runner.run('lingo/app.qqu')