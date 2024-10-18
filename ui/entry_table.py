import tkinter as tk
from typing import Callable, Optional

class EntryTable(tk.Frame):
  def __init__(self, root, columns: tuple[str,...], initial_data: list[tuple[str,...]] = [], on_row_change: Optional[Callable[[int, int, list[str]], None]] = None):
    super().__init__(root)

    self.heading_entry = EntryRow(self, -1, values=columns, editable=False)
    self.heading_entry.pack(fill=tk.X)

    self.variable_table: list[EntryRow] = []
    self.on_row_change: Optional[callable[[int, int, list[str]], None]] = on_row_change

    for row_idx in range(0, len(initial_data)):
      row = EntryRow(self, row_idx, initial_data[row_idx], self.on_row_change)
      row.pack(fill=tk.X)
      self.variable_table.append(row)

  def append_row(self, values: tuple[str,...]):
    idx = len(self.variable_table)
    entry_row = EntryRow(self, idx, values, on_row_change_action=self.on_row_change)
    entry_row.pack(fill=tk.X, side=tk.LEFT)
    self.variable_table.append(entry_row)

  def insert_row(self, index: int, values: tuple[str,...]):
    # TODO need to do this and update rowids 
    pass

  def remove_row(self, index: int) -> list[str]:
    to_remove = self.variable_table[index]
    self.variable_table.remove(to_remove)
    for idx in range(to_remove.row_id, len(self.variable_table)):
      self.variable_table[idx].row_id -= 1
    return to_remove.values()

  def set_row_change_action(self, row_change_action: Callable[[int, int, list[str]], None]):
    self.on_row_change = row_change_action
    for entry_row in self.variable_table:
      entry_row.set_row_change_action(row_change_action)

class EntryRow(tk.Frame):
  def __init__(self, root, row_id: int, values: tuple[str,...], on_row_change_action: Optional[Callable[[int, int, list[str]], None]] = None, editable: bool = True):
    super().__init__(root)
    self.row_id = row_id
    self.editable = editable
    self.internal_values: list[tuple[tk.StringVar, tk.Entry]] = []
    self.on_row_change_action: Optional[Callable[[int, int, list[str]], None]] = on_row_change_action
    for idx in range(0, len(values)):
      self.columnconfigure(idx, weight=1)
      var = tk.StringVar(value=values[idx])
      entry = tk.Entry(self, textvariable=var)
      if self.editable:
        entry.configure(state=tk.NORMAL, relief='sunken')
      else:
        entry.configure(state='readonly', relief='raised')
      entry.bind('<KeyRelease>', self.__bind_row_change(idx))
      entry.grid(row=0, column=idx, sticky=tk.NSEW)
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
