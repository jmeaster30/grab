from math import floor
import platform
import tkinter as tk
from tkinter import ttk
from typing import Literal, Optional

class ScrollableWidgetList(tk.Frame):
  def __init__(self, root, *args, **kwargs):
    self.full_container = tk.Frame(root, *args, *kwargs)
    self.canvas = tk.Canvas(self.full_container)
    self.scrollbar = ttk.Scrollbar(self.full_container, orient=tk.VERTICAL, command=self.canvas.yview)
    self.canvas.configure(yscrollcommand=self.scrollbar.set)
    super().__init__(self.canvas)

    # set up function overrides fro geometry managers
    #geometry_manager_method_list = [func for func in dir(self.__class__) if callable(getattr(self, func)) and (func.startswith("pack") or func.startswith("grid") or func.startswith("place"))]
    geometry_manager_method_list = []
    for func in dir(self.__class__):
      print(func)
      if callable(getattr(self, func)):
        print(f"FUNC: {func}")
        if func.startswith("pack"):
          print("pack")
          geometry_manager_method_list.append(func)
        elif func.startswith("grid"):
          print("grid")
          geometry_manager_method_list.append(func)
        elif func.startswith("place"):
          print("place")
          geometry_manager_method_list.append(func)
        else:
          print("NO IDEA")
    
    for method in geometry_manager_method_list:
      setattr(self, f'internal_{method}', getattr(super(tk.Frame, self), method))
      setattr(self, method, getattr(self.full_container, method))

    self.internal_pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
    self.inner_frame_id = self.canvas.create_window((0,0), window=self, anchor=tk.NW)

    # Track changes to the canvas and frame width and sync them,
    # also updating the scrollbar.
    def _configure_interior(event):
      # Update the scrollbars to match the size of the inner frame.
      self.canvas.config(scrollregion=self.canvas.bbox("all"))
      if self.winfo_reqwidth() != self.canvas.winfo_width():
        # Update the canvas's width to fit the inner frame.
        self.canvas.config(width=self.winfo_reqwidth())
    self.bind('<Configure>', _configure_interior)

    def _configure_canvas(event):
      if self.winfo_reqwidth() != self.canvas.winfo_width():
        # Update the inner frame's width to fill the canvas.
        self.canvas.itemconfigure(self.inner_frame_id, width=self.canvas.winfo_width())
    self.canvas.bind('<Configure>', _configure_canvas)

    self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    self.scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

  # TODO: this name feels weird
  def get_items(self):
    return sorted(self.children, key=lambda x: x.row_id) # FIXME: I don't actually think sorting is necessary and it will help make stuff not dependent on entry grid

  def show(self, widget: tk.Widget):
    if widget in self.get_items():
      self.canvas.yview_moveto(widget.winfo_y(), self.winfo_y())
