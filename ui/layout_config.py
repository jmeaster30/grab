from enum import Enum
import tkinter as tk
from tkinter import font as tkfont, ttk
from lilytk.utils import Singleton

class Colors(Enum):
  BLACK = '#000000'
  RED = '#ff0000'
  ORANGE = '#ffa500'
  YELLOW = '#ffff00'
  GREEN = '#00ff00'
  BLUE = '#0000ff'
  PURPLE = '#9f00ff'
  WHITE = '#ffffff'
  def __str__(self):
    return self.value

class HighlightConfig:
  def __init__(self):
    self.color = Colors.RED
    self.width = 2
    self.blink_delay = 100
    self.blink_duration = 2

class WindowConfig:
  def __init__(self):
    self.title = 'grab'
    self.width = 1200
    self.height = 900

  def size(self) -> str:
    return f'{self.width}x{self.height}'

@Singleton
class LayoutConfig:
  def __init__(self):
    self.fontSize = 10

    self.highlight = HighlightConfig()
    self.window = WindowConfig()

    self.style = ttk.Style()
    self.style.configure("Treeview", font=(None, self.fontSize), rowheight=int(self.fontSize * 3.2))

    font = tkfont.Font(font=(None, self.fontSize))
    self.text_tab = font.measure('    ')

    #
    #  THE FOLLOWING IS ALL CONFIG FOR WorkArea SO THE TABS CAN HAVE A CLOSE BUTTON
    #
    self.images = (
      tk.PhotoImage("img_close", data='''
        R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
        d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
        5kEJADs=
        '''),
      tk.PhotoImage("img_closeactive", data='''
        R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
        AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
        '''),
      tk.PhotoImage("img_closepressed", data='''
        R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
        d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
        5kEJADs=
        ''')
    )

    self.style.element_create("close", "image", "img_close",
      ("active", "pressed", "!disabled", "img_closepressed"),
      ("active", "!disabled", "img_closeactive"), border=8, sticky='')
    self.style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": tk.NSEW})])
    self.style.layout("CustomNotebook.Tab", [
      ("CustomNotebook.tab", {
        "sticky": tk.NSEW,
        "children": [
          ("CustomNotebook.padding", {
            "side": tk.TOP,
            "sticky": tk.NSEW,
            "children": [
              ("CustomNotebook.focus", {
                "side": tk.TOP,
                "sticky": tk.NSEW,
                  "children": [
                    ("CustomNotebook.label", {"side": tk.LEFT, "sticky": ''}),
                    ("CustomNotebook.close", {"side": tk.LEFT, "sticky": ''}),
                  ]
              })
            ]
          })
        ]
      })
    ])
