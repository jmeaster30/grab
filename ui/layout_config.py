import tkinter as tk
from tkinter import font, ttk
from util.singleton import Singleton

@Singleton
class LayoutConfig:
  def __init__(self):
    self.title = 'grab'
    self.width = 1200
    self.height = 900
    self.fontSize = 10
    self.style = ttk.Style()
    self.style.configure("Treeview", font=(None, self.fontSize), rowheight=int(self.fontSize * 3.2))

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
    self.style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
    self.style.layout("CustomNotebook.Tab", [
      ("CustomNotebook.tab", {
        "sticky": "nswe",
        "children": [
          ("CustomNotebook.padding", {
            "side": "top",
            "sticky": "nswe",
            "children": [
              ("CustomNotebook.focus", {
                "side": "top",
                "sticky": "nswe",
                  "children": [
                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                  ]
              })
            ]
          })
        ]
      })
    ])

