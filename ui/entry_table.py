import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from lilytk import ScrollableFrame

from ui.highlightable import Highlightable

class EntryTable(tk.Frame):
  def __init__(self, root, columns: tuple[str,...], initial_data: list[tuple[str,...]] = [], on_row_change: Optional[Callable[[int, int, list[str]], None]] = None):
    super().__init__(root)

    self.heading_entry = EntryRow(self, -1, values=columns, editable=False)
    self.heading_entry.pack(fill=tk.X)

    self.table_frame = ScrollableFrame(self, orient=tk.VERTICAL)
    self.table_frame.pack(expand=True, fill=tk.BOTH)

    self.variable_table: list[EntryRow] = []
    self.on_row_change: Optional[callable[[int, int, list[str]], None]] = on_row_change

    for row_idx in range(0, len(initial_data)):
      row = EntryRow(self.table_frame, row_idx, initial_data[row_idx], on_row_change_action=self.on_row_change)
      row.pack(fill=tk.X)
      self.variable_table.append(row)

  def append_row(self, values: tuple[str,...]):
    entry_row = EntryRow(self, len(self.variable_table), values, on_row_change_action=self.on_row_change)
    entry_row.pack(fill=tk.X, side=tk.LEFT)
    self.variable_table.append(entry_row)

  def remove_row(self, index: int) -> list[str]:
    to_remove = self.variable_table[index]
    self.variable_table.remove(to_remove)
    for idx in range(to_remove.row_id, len(self.variable_table)):
      self.variable_table[idx].row_id -= 1
    return to_remove.values()

  def highlight_row(self, row: tuple[str,...]):
    index = self.variable_table.index(row)
    widget = self.variable_table[index]
    widget.highlight()
    self.table_frame.show(widget)

  def unhighlight_row(self, row: tuple[str,...]):
    index = self.variable_table.index(row)
    self.variable_table[index].unhighlight()
    
  def unhighlight_all_rows(self):
    for row in self.variable_table:
      row.unhighlight()
    
  def set_row_change_action(self, row_change_action: Callable[[int, int, list[str]], None]):
    self.on_row_change = row_change_action
    for entry_row in self.variable_table:
      entry_row.set_row_change_action(row_change_action)

class EntryRow(tk.Frame, Highlightable):
  def __init__(self, root, row_id: int, values: tuple[str,...], editable: bool = True, on_row_change_action: Optional[Callable[[int, int, list[str]], None]] = None, on_select_change_action: Optional[Callable[[int, bool], None]] = None):
    super().__init__(root)

    self.row_id = row_id
    self.editable = editable
    self.internal_values: list[tuple[tk.StringVar, tk.Entry]] = []

    self.on_row_change_action: Optional[Callable[[int, int, list[str]], None]] = on_row_change_action
    self.on_select_change_action: Optional[Callable[[int, bool], None]] = on_select_change_action

    self.selected = tk.BooleanVar(value=False)
    self.check_box = tk.Checkbutton(self, variable=self.selected, offvalue=False, onvalue=True, command=self.__bind_select_change())
    self.check_box.grid(row=0, column=0)

    for idx in range(0, len(values)):
      self.columnconfigure(idx+1, weight=1)
      var = tk.StringVar(value=values[idx])
      entry = tk.Entry(self, textvariable=var)
      if self.editable:
        entry.configure(state=tk.NORMAL, relief='sunken')
      else:
        entry.configure(state='readonly', relief='raised')
      entry.bind('<KeyRelease>', self.__bind_row_change(idx))
      entry.grid(row=0, column=idx+1, sticky=tk.NSEW)
      self.internal_values.append((var, entry))

  def values(self) -> list[str]:
    return [val[0].get() for val in self.internal_values]

  def get(self, idx: int) -> Optional[str]:
    if idx < 0 or idx >= len(self.internal_values):
      return None
    return self.internal_values[idx][0].get()

  def set(self, idx: int, value: str):
    if idx < 0 or idx >= len(self.internal_values):
      return None
    self.internal_values[idx][0].set(value)

  def set_editable(self, editable: bool):
    self.editable = editable
    if self.editable:
      for entry in self.internal_values:
        entry[1].configure(state=tk.NORMAL, relief='sunken')
    else:
      for entry in self.internal_values:
        entry[1].configure(state='readonly', relief='raised')

  def set_row_change_action(self, action: Callable[[int, int, list[str]], None]):
    self.on_row_change_action = action

  def __bind_row_change(self, col_idx: int) -> Callable[[tk.Event], None]:
    return lambda event: self.on_row_change_action(self.row_id, col_idx, self.values()) if self.on_row_change_action is not None else None

  def __bind_select_change(self) -> Callable[[tk.Event], None]:
    return lambda event: self.on_select_change_action(self.row_id, self.values()) if self.on_select_change_action is not None else None

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.values() == other.values()
    if isinstance(other, list):
      return self.values() == other
    if isinstance(other, tuple):
      return self.values() == list(other)
    return False