import tkinter as tk
from typing import Callable, Optional

from lilytk.events import ClassListens

from model.collection import Collection
from model.request import Request, RequestMethod
from lilytk.widgets import ScrollableFrame

from ui.dropdown_select import DropDownSelect
from ui.left_right_buttons import LeftRightButtons
from util.getnewname import get_new_name

@ClassListens('Request.NameUpdated', 'pull_name')
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
    self.request.set_name(self.name_var.get())

  def pull_name(self, data):
    self.name_var.set(self.request.name)

  def on_row_open(self):
    if self.on_row_open_action is not None:
      self.on_row_open_action(self.request)

  def __bind_select_change(self) -> Callable[[tk.Event], None]:
    return lambda: None if self.on_row_selected is None else self.on_row_selected(self.request)

class CollectionEditGrid(ScrollableFrame):
  def __init__(self, root, collection: Collection):
    super().__init__(root, orient=tk.VERTICAL)
    self.collection = collection

    self.on_row_open = None
    self.on_row_selected = None
    self.selected_rows: list[str] = []
    self.request_rows: dict[str, CollectionRequestRow] = {}

    for request in collection.requests.items():
      self.request_rows[request.id] = CollectionRequestRow(self, request, on_row_selected=self.row_selected, on_row_open=self.on_row_open)
      self.request_rows[request.id].pack(fill=tk.X)

  def add_row(self):
    new_request = Request(method=self.collection.default_method, 
                          url=self.collection.default_url, 
                          name=get_new_name('Request', [req.name for _, req in self.collection.requests.items()]))
    self.request_rows[new_request.id] = CollectionRequestRow(self, new_request, on_row_selected=self.row_selected, on_row_open=self.on_row_open)
    self.request_rows[new_request.id].pack(fill=tk.X)
    self.collection.add_request(new_request)

  def remove_selected_rows(self):
    removed_requests = []
    for selected in self.selected_rows:
      removed_requests.append(self.request_rows[selected].request)
      self.request_rows[selected].forget()
      self.request_rows.pop(selected)
      self.collection.remove_request(selected)
    self.selected_rows = []

  def row_selected(self, request: Request):
    if request.id in self.selected_rows:
      self.selected_rows.remove(request.id)
    else:
      self.selected_rows.append(request.id)
    if self.on_row_selected is not None:
      self.on_row_selected(request, self.selected_rows)

  def set_on_row_open(self, on_row_open: Callable[[Request], None]):
    self.on_row_open = on_row_open
    for row in self.request_rows.values():
      row.set_on_row_open(on_row_open)

  def set_on_row_selected(self, on_row_selected: Callable[[Request, list[str]], None]):
    self.on_row_selected = on_row_selected

class CollectionDefaultFrame(tk.Frame):
  def __init__(self, root, collection: Collection):
    super().__init__(root)
    self.collection = collection

    self.label = tk.Label(self, text="Default: ")
    self.label.pack(side=tk.LEFT)

    self.request_method = DropDownSelect(self, values=RequestMethod.get_all(),
                                        label_selector=(lambda method: method.name),
                                        on_selection_change=self.on_method_change,
                                        default_selected=RequestMethod.GET, width=10)
    self.request_method.pack(side=tk.LEFT)

    self.default_url_entry_var = tk.StringVar(value=self.collection.default_url)
    self.default_url_entry = tk.Entry(self, textvariable=self.default_url_entry_var)
    self.default_url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    self.default_url_entry.bind('<KeyRelease>', self.on_default_url_update)

  def on_method_change(self, selected_method: Optional[RequestMethod]):
    if selected_method is None:
      self.collection.default_method = RequestMethod.GET
    else:
      self.collection.default_method = selected_method

  def on_default_url_update(self, event):
    self.collection.default_url = self.default_url_entry_var.get()

@ClassListens('Collection.NameUpdated')
class CollectionEditArea(tk.Frame):
  def __init__(self, root, collection: Collection, on_row_open: Callable[[Request], None]):
    super().__init__(root)
    self.collection: Collection = collection;

    self.rowconfigure(2, weight=1)
    self.columnconfigure(0, weight=1)

    self.collection_name_var = tk.StringVar(value=self.collection.name)
    self.collection_name_entry = tk.Entry(self, textvariable=self.collection_name_var)
    self.collection_name_entry.grid(row=0, column=0, sticky=tk.EW)
    self.collection_name_entry.bind('<KeyRelease>', self.on_collection_name_change)

    self.default_frame = CollectionDefaultFrame(self, self.collection)
    self.default_frame.grid(row=1, column=0, sticky=tk.NSEW)

    self.requests_grid = CollectionEditGrid(self, self.collection)
    self.requests_grid.grid(row=2, column=0, sticky=tk.NSEW)
    self.requests_grid.set_on_row_selected(self.on_row_selected)
    self.requests_grid.set_on_row_open(on_row_open)

    self.add_remove_buttons = LeftRightButtons(self, "+ Add Request", "- Remove Request(s)")
    self.add_remove_buttons.grid(row=3, column=0, sticky=tk.EW)
    self.add_remove_buttons.left_button_action = lambda: self.requests_grid.add_row()
    self.add_remove_buttons.right_button_action = lambda: self.requests_grid.remove_selected_rows()
    self.add_remove_buttons.set_right_button_clickable(False)

  def on_collection_name_change(self, event: tk.Event):
    self.collection.set_name(self.collection_name_var.get())

  def on_row_selected(self, request: Request, selected_request_ids: list[str]):
    self.add_remove_buttons.set_right_button_clickable(len(selected_request_ids) > 0)
