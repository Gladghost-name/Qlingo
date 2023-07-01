from Qlingo.lingo.app import *

class MyApp(qquApp):
    def __init__(self):
        super().__init__('cook.qqu')
        self.reloadable(True)

if __name__ == '__main__':
    app = MyApp()
    app.run()