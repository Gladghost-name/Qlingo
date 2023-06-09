[//]: # (# Qlingo-AppCreator)

[//]: # ()
[//]: # (---)

<p align="center">
    <img align="top" src="https://variwiki.com/images/4/4e/Qt_logo.png" alt="figma logo">
    <h1 align="center"><strong>Qlingo</strong>
        <h4 align="center">Create, Design and Convert.</h4>
    </h1>
</p>

Qlingo is a Python module that leverages the PyQt5 library for faster development and app creation. It includes a custom language called QQU (Qlingo Quick UI) for defining GUI layouts, and supports automatic reloading of changes during development.

This is a powerful tool that allows users to easily convert Figma designs into functional applications. With QQU, users can leverage the power of Python and PyQt5 to create robust applications with ease.

One of the key features of Qlingo is its ability to convert Figma designs into functional applications. Users can simply import their Figma designs into QQU and the module will automatically generate the code needed to create a functional application. This makes it simple for users to turn their designs into fully-functional applications with minimal effort.

## 💡**Introduction**

To use Qlingo, first make sure you have PyQt5 installed. You can install it using pip:

```bash
  pip install PyQt5
```

Next, download the Qlingo module and import it into your Python project:

```python
from qlingo.app import *
```

# Building with QQu 🔨

QQU is a simple language for defining GUI layouts in Qlingo. Here's an example QQU file:

```bash
Window:
    title: "My App"
    width: 400
    height: 300
    
    Label:
        text: "Hello, world!"
        
    Button:
        text: "Click me!"
```

This file defines an app that can be loaded using:

```python
class MainApp(App):
    # initialize the app class!.
    def __init__(self, "{file-name}"):
        pass
```

To provide flexibility for the user or developer, Qlingo allows them to choose whether to reload the app automatically with changes or run it once without reload, by using either ``self.reloadable(True)`` in the app class or simply calling ``self.load_app()`` as needed.

# _Figma to app_.

<p align="right">
  <img align="left" width="150" height="220" src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Figma-logo.svg/200px-Figma-logo.png" alt="figma logo">
    Qlingo offers a convenient way for users to convert their Figma designs into PyQt5 applications with stylish and modern UI. By using QQU, Qlingo's custom language for defining GUI layouts, users can quickly and easily translate their Figma designs into code. With the automatic reloading feature, users can make changes to their layout files and see them reflected immediately in their application.
    Additionally, Qlingo offers a wide range of pre-built styles that can be easily applied to the application's widgets, including buttons, labels, and input fields. These styles are designed to be visually appealing and fit well with modern design trends. By leveraging Qlingo's features and pre-built styles, users can create polished and professional-looking applications in a fraction of the time it would take to write the code manually.
    Overall, Qlingo offers a powerful solution for designers and developers looking to turn their Figma designs into PyQt5 applications quickly and easily, without sacrificing style or functionality.
</p>

# ⭐Getting Started


##### Understanding the qlingo command tool.

To generate a pyqt5 designed app from figma is made easy by using the qlingo terminal command that helps you manage your project and generate apps from design.

### Importing using pip.

```bash
pip install lingo-cmd
```

### Generating a package from url 📦

```shell
lingo -generate {FILETOKEN} {FILEURL}
```

This will generate an app package that contains your styles, A main runnable python script and a qqu script for reloading the application based on your ``figma design``, just remember to replace the ``{FILETTOKEN}`` and ``{FILEURL}`` with your token and your file-key or file-url respectively.

#### Understanding the project structure!
A project will be generated based on the title of your figma file in your current directory, after locating the directory you should see the generated pages based on their content with a simple project thumbnail png image showing the looks of the ui created from figma. inside the pages you should see a ``src`` folder with all the usable assets and files.

# Supported Widgets.

Qlingo makes it easy to convert widgets from Figma designs to PyQt5 code using the QQU language. With Qlingo, you can automatically generate the PyQt5 code. This means you can quickly and easily create fully functional PyQt5 apps from your Figma designs, without having to manually write or layout the code yourself. QQU provides a simplified syntax for creating PyQt5 widgets, making it more intuitive and easier to read than raw PyQt5 code. By using Qlingo, you can save time and effort in the development process, and create polished, professional-looking apps that match your Figma designs.

#### But wait, Differences⚠️.

This simply means we will have to do alot of conversion and naming since thay all have different names that they call their widgets expecially figma which does'nt support the adding of widget!.

Here! is a simple overview of some supported widgets and how to use them respectively in each of the frameworks.

| PyQt5       | Figma      | QQu       |
|:------------|:-----------|:----------|
| QMainWindow | Main Frame | Window    |
| QFrame      | Frame      | Frame     |
| QPushButton | Button     | Button    |
| QTextEdit   | TextEdit   | TextEdit  |
| QLineEdit   | TextInput  | TextInput |
| QFrame      | Text       | Text      |
| QLabel      | Image      | Image     |
| QLabel      | Label      | Label     |

##### _Note: This is a simple overview of some inplementations of widgets using the qqu file and the figms file, for more info pls view or click the [usage.md](docs/usage.md) file in the documentation folder!_

# __Requirements__
Here are some requirements to using Qlingo!

- Any Desktop Computer (e.g, Windows, Linux mac, e.t.c..)
- PyQt5 Support
- Figma Api token for app generation!
- FigmaPy module
- ``python 3.11`` or higher
- Basic Understanding of PyQt5 and its components!

##### _Good Luck! developing your first pyqt and qlingo app!_
All Thanks!