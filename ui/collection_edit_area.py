import tkinter as tk
from typing import Callable, Collection, Optional

from model.request import Request, RequestMethod
from lilytk import ScrollableFrame

from ui.dropdown_select import DropDownSelect

class CollectionRequestRow(tk.Frame):
  def __init__(self, root, request: Request, on_row_selected: Optional[Callable[[str, Request], None]] = None):
    super().__init__(root)
    self.request = request
    self.on_row_selected = on_row_selected

    self.rowconfigure(0, weight=1)
    self.columnconfigure(2, weight=1)

    self.selected = tk.BooleanVar(value=False)
    self.check_box = tk.Checkbutton(self, variable=self.selected, offvalue=False, onvalue=True, command=self.__bind_select_change())
    self.check_box.grid(row=0, column=0)

    self.request_method = DropDownSelect(self, values=RequestMethod.get_all(), 
                                        label_selector=(lambda method: method.name),
                                        on_selection_change=self.on_method_change,
                                        default_selected=request.method, width=10)
    self.request_method.grid(row=0, column=1, sticky=tk.EW)

    self.name_var = tk.StringVar(value=self.request.name)
    self.name = tk.Entry(self, textvariable=self.name_var)
    self.name.grid(row=0, column=2, sticky=tk.EW)
    self.name.bind('<KeyRelease>', self.on_name_change)

  def on_method_change(self, new_method: RequestMethod):
    self.request.method = new_method

  def on_name_change(self, event: tk.Event):
    self.request.name = self.name_var.get()
    self.request.refresh()

  def on_url_change(self, event: tk.Event):
    self.request.url = self.url_var.get()

  def __bind_select_change(self) -> Callable[[tk.Event], None]:
    return lambda: None if self.on_row_selected is None else self.on_row_selected(self.row_id, self.request)

class CollectionEditGrid(ScrollableFrame):
  def __init__(self, root, requests: list[Request]):
    super().__init__(root, orient=tk.VERTICAL)

    self.request_rows: dict[str, CollectionRequestRow] = {}

    for request in requests:
      self.request_rows[request.tree_id] = CollectionRequestRow(self, request)
      self.request_rows[request.tree_id].pack(fill=tk.X)

  def add_row(self, request: Request):
    pass

class CollectionEditArea(tk.Frame):
  def __init__(self, root, collection: Collection):
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

  def on_collection_name_change(self, event: tk.Event):
    self.collection.set_name(self.collection_name_var.get())
    self.collection.refresh()
