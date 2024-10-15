from tkinter import font, ttk
from util.singleton import Singleton

@Singleton
class LayoutConfig:
  def __init__(self):
    self.title = 'grab'
    self.width = 1000
    self.height = 1000
    self.fontSize = 10
    self.style = ttk.Style()
    self.style.configure("Treeview", font=(None, self.fontSize), rowheight=int(self.fontSize * 3.2))

