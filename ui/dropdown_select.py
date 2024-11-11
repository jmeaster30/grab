import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Optional

class DropDownSelect(ttk.Combobox):
  def __init__(self, *args, placeholder: Optional[str] = None, values: list[Any] = [], default_selected: Optional[Any] = None,
              label_selector: Optional[Callable[[Any], str]] = None,
              on_selection_change: Optional[Callable[[Optional[Any]], None]] = None,
              **kwargs):
    self.internal_label_value_map: dict[str, Any] = {}
    self.internal_label_list: list[str] = []
    self.label_selector: Optional[Callable[[Any], str]] = label_selector
    self.selected_value_var: tk.StringVar = tk.StringVar()
    self.on_selection_change = on_selection_change
    super().__init__(*args, textvariable=self.selected_value_var, **kwargs)

    for item in values:
      text_value = self.__get_label_from_value(item)
      
      self.internal_label_value_map[text_value] = item
      self.internal_label_list.append(text_value)
      
    super().config(values=self.internal_label_list)

    if default_selected is not None:
      self.select(default_selected)

    self.bind('<<ComboboxSelected>>', self.__internal_selection_change)

  def selected(self) -> Optional[Any]:
    if self.current() == -1:
      return None
    return self.internal_label_value_map[self.selected_value_var.get()]

  def select(self, value: Any):
    label = self.__get_label_from_value(value)
    if label not in self.internal_label_list:
      raise ValueError
    idx = self.internal_label_list.index(label)
    self.current(idx)
    self.event_generate('<<ComboboxSelected>>', data=label)

  def deselect(self):
    self.current(-1)

  def __internal_selection_change(self, _: tk.Event):
    if self.on_selection_change is not None:
      self.on_selection_change(self.selected())

  def __get_label_from_value(self, value) -> str:
    if self.label_selector is None:
      return str(value)
    else:
      return self.label_selector(value)

