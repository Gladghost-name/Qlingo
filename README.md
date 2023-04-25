# Qlingo: A PyQt5 Module for Faster Development and App Creation

---

Qlingo is a Python module that leverages the PyQt5 library for faster development and app creation. It includes a custom language called QQU (Qlingo Quick UI) for defining GUI layouts, and supports automatic reloading of changes during development.


## Getting Started


To use Qlingo, first make sure you have PyQt5 installed. You can install it using pip:

```bash
  pip install PyQt5
```

Next, download the Qlingo module and import it into your Python project:

```python
from qlingo.app import *
```

# Using QQU for GUI Layouts

QQU is a simple language for defining GUI layouts in Qlingo. Here's an example QQU file:

```toml
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

# Converting my design from figma to app.

<p align="right">
  <img align="left" src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Figma-logo.svg/200px-Figma-logo.png" alt="figma logo">
    Qlingo offers a convenient way for users to convert their Figma designs into PyQt5 applications with stylish and modern UI. By using QQU, Qlingo's custom language for defining GUI layouts, users can quickly and easily translate their Figma designs into code. With the automatic reloading feature, users can make changes to their layout files and see them reflected immediately in their application.
    Additionally, Qlingo offers a wide range of pre-built styles that can be easily applied to the application's widgets, including buttons, labels, and input fields. These styles are designed to be visually appealing and fit well with modern design trends. By leveraging Qlingo's features and pre-built styles, users can create polished and professional-looking applications in a fraction of the time it would take to write the code manually.
    Overall, Qlingo offers a powerful solution for designers and developers looking to turn their Figma designs into PyQt5 applications quickly and easily, without sacrificing style or functionality.
</p>