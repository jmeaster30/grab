import tkinter as tk
from typing import Callable, Optional

from model.collection import Collection
from model.request import Request
from lilytk import ScrollableFrame

from ui.left_right_buttons import LeftRightButtons

class CollectionRequestRow(tk.Frame):
  def __init__(self, root, request: Request, 
              on_row_selected: Optional[Callable[[str, Request], None]] = None,
              on_row_open: Optional[Callable[[Request], None]] = None):
    super().__init__(root)
    self.request = request
    self.on_row_selected = on_row_selected
    self.on_row_open_action = on_row_open

    self.rowconfigure(0, weight=1)
    self.columnconfigure(2, weight=1)

    self.selected = tk.BooleanVar(value=False)
    self.check_box = tk.Checkbutton(self, variable=self.selected, offvalue=False, onvalue=True, command=self.__bind_select_change())
    self.check_box.grid(row=0, column=0)

    self.name_var = tk.StringVar(value=self.request.name)
    self.name = tk.Entry(self, textvariable=self.name_var)
    self.name.grid(row=0, column=2, sticky=tk.EW)
    self.name.bind('<KeyRelease>', self.on_name_change)

    self.open_button = tk.Button(self, text='Open', command=self.on_row_open)
    self.open_button.grid(row=0, column=3, sticky=tk.EW)

  def set_on_row_open(self, on_row_open: Optional[Callable[[Request], None]]):
    self.on_row_open_action = on_row_open

  def on_name_change(self, event: tk.Event):
    self.request.name = self.name_var.get()
    self.request.refresh()

  def on_row_open(self):
    if self.on_row_open_action is not None:
      self.on_row_open_action(self.request)

  def __bind_select_change(self) -> Callable[[tk.Event], None]:
    return lambda: None if self.on_row_selected is None else self.on_row_selected(self.request)

class CollectionEditGrid(ScrollableFrame):
  def __init__(self, root, requests: list[Request]):
    super().__init__(root, orient=tk.VERTICAL)

    self.on_row_open = None
    self.on_row_selected = None
    self.on_row_added = None
    self.on_rows_removed = None
    self.selected_rows: list[str] = []
    self.request_rows: dict[str, CollectionRequestRow] = {}

    for request in requests:
      self.request_rows[request.tree_id] = CollectionRequestRow(self, request, on_row_selected=self.row_selected, on_row_open=self.on_row_open)
      self.request_rows[request.tree_id].pack(fill=tk.X)

  def add_row(self, request: Request):
    self.request_rows[request.tree_id] = CollectionRequestRow(self, request, on_row_selected=self.row_selected, on_row_open=self.on_row_open)
    self.request_rows[request.tree_id].pack(fill=tk.X)
    if self.on_row_added is not None:
      self.on_row_added(request)

  def remove_selected_rows(self):
    removed_requests = []
    for selected in self.selected_rows:
      removed_requests.append(self.request_rows[selected].request)
      self.request_rows[selected].forget()
      self.request_rows.pop(selected)
    self.selected_rows = []
    if self.on_rows_removed is not None:
      self.on_rows_removed(removed_requests)

  def row_selected(self, request: Request):
    if request.tree_id in self.selected_rows:
      print("removing selected row")
      self.selected_rows.remove(request.tree_id)
    else:
      print("adding selected row")
      self.selected_rows.append(request.tree_id)
    if self.on_row_selected is not None:
      self.on_row_selected(request, self.selected_rows)

  def set_on_row_open(self, on_row_open: Callable[[Request], None]):
    self.on_row_open = on_row_open
    for row in self.request_rows.values():
      row.set_on_row_open(on_row_open)

  def set_on_row_selected(self, on_row_selected: Callable[[Request, list[str]], None]):
    self.on_row_selected = on_row_selected

  def set_on_row_added(self, on_row_added: Callable[[Request], None]):
    self.on_row_added = on_row_added

  def set_on_rows_removed(self, on_rows_removed: Callable[[list[Request]], None]):
    self.on_rows_removed = on_rows_removed

class CollectionEditArea(tk.Frame):
  def __init__(self, root, collection: Collection, on_row_open: Callable[[Request], None]):
    super().__init__(root)
    self.collection: Collection = collection;

    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)

    self.collection_name_var = tk.StringVar(value=self.collection.name)
    self.collection_name_entry = tk.Entry(self, textvariable=self.collection_name_var)
    self.collection_name_entry.grid(row=0, column=0, sticky=tk.EW)
    self.collection_name_entry.bind('<KeyRelease>', self.on_collection_name_change)

    self.requests_grid = CollectionEditGrid(self, self.collection.requests)
    self.requests_grid.grid(row=1, column=0, sticky=tk.NSEW)
    self.requests_grid.set_on_row_selected(self.on_row_selected)
    self.requests_grid.set_on_row_open(on_row_open)

    self.add_remove_buttons = LeftRightButtons(self, "+ Add Request", "- Remove Request(s)")
    self.add_remove_buttons.grid(row=2, column=0, sticky=tk.EW)
    self.add_remove_buttons.left_button_action = lambda: self.requests_grid.add_row(Request(self.collection))
    self.add_remove_buttons.right_button_action = lambda: self.requests_grid.remove_selected_rows()
    self.add_remove_buttons.set_right_button_clickable(False)

  def on_collection_name_change(self, event: tk.Event):
    self.collection.set_name(self.collection_name_var.get())
    self.collection.refresh()

  def on_row_selected(self, request: Request, selected_request_ids: list[str]):
    self.add_remove_buttons.set_right_button_clickable(len(selected_request_ids) > 0)
