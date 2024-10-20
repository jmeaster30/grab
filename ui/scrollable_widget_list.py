from math import floor
import tkinter as tk
from tkinter import ttk
from typing import Literal, Optional

class ScrollableWidgetList(tk.Frame, tk.XView, tk.YView):
  def __init__(self, root, orient=tk.VERTICAL):
    super().__init__(root)
    self.scrollbar = ttk.Scrollbar(self, orient=orient, command=self.__view)

    self.orient = orient
    if orient == tk.VERTICAL:
      self.scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
    else:
      self.scrollbar.pack(fill=tk.X, side=tk.BOTTOM)

    self.internal_widgets: list[InternalWidget] = []
    self.widget_view: tuple[int, int] = (0, 0);

    self.bind('<Map>', self.__on_widget_add)
    self.bind('<Configure>', self.__on_configure)
    self.bind('<Enter>', self.__enter)
    self.bind('<Leave>', self.__leave)

  def show(self, index: int):
    widget = self.internal_widgets[index]
    widget.shown = True
    widget.pack(fill=tk.X if self.orient == tk.VERTICAL else tk.Y)

  def hide(self, index: int):
    widget = self.internal_widgets[index]
    widget.shown = False
    widget.pack_forget()

  def move_view_to(self, index: int) -> Optional[tk.Widget]:
    self.viewed_widget_index_start = index

  def insert(self, index: int, widget: tk.Widget) -> int:
    self.internal_widgets.insert(index, InternalWidget(widget))
    widget.pack(fill=tk.X)
    return index

  def remove(self, index: int) -> tk.Widget:
    widget = self.internal_widgets.pop(index)
    widget.destroy()
    return widget

  def push(self, widget: tk.Widget) -> int:
    index = len(self.internal_widgets)
    self.internal_widgets.append(InternalWidget(widget))
    widget.pack(fill=tk.X if self.orient == tk.VERTICAL else tk.Y)
    return index

  def pop(self) -> tk.Widget:
    widget = self.internal_widgets.pop()
    widget.destroy()
    return widget

  def __on_widget_add(self, event: tk.Event):
    print("ITEM ADDED")
    print(event.widget)

  def __on_configure(self, event):
    print("scrollable widget configure")

  def __enter(self, event):
    self.y_scroll_func_id = self.bind_all('<MouseWheel>', self.__on_y_mouse_scroll)
    self.x_scroll_func_id = self.bind_all('<Shift-MouseWheel>', self.__on_x_mouse_scroll)

  def __leave(self, event):
    if self.y_scroll_func_id is not None:
      self.unbind('<MouseWheel>', self.y_scroll_func_id)
    if self.x_scroll_func_id is not None:
      self.unbind('<Shift-MouseWheel>', self.x_scroll_func_id)

  def __on_x_mouse_scroll(self, event: tk.Event):
    print(f"x scroll delta: {event.delta}")

  def __on_y_mouse_scroll(self, event: tk.Event):
    print(f"y scroll delta: {event.delta}")

  def __scrollcommand(self, first: float, last: float):
    # the percentages of the scrollbar size over the range of the length of the scrollbar
    # first = 0.25 , last = 0.5
    # means the view should be changed to only show the first quartile of widgets (if 40 widgets it will show widgets 10 thru 19)
    
    # sets the scrollbar position and size
    #self.scrollbar.set(first, last)
    length = len(self.internal_widgets)

    step = 1 / length
    start = floor(first * length) * step
    end = floor(last * length) * step
    self.scrollbar.set(start, end)

  def __view(self, command: str, value: float, unit: Literal['units'] | Literal['pages'] = 'units'):
    # gets / sets the view on the frame
    match command:
      case 'scroll':
        print('here scroll')
      case 'moveto':
        print('here moveto')
        # value is a percentage of the scrollbar amount
      case _:
        print(f"idk: {command}")

class InternalWidget:
  def __init__(self, widget: tk.Widget, shown: bool = True):
    self.widget = widget
    self.shown = shown