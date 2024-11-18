import tkinter as tk
from tkinter import ttk
from typing import Collection, Optional

from model.environment import Environment, EnvironmentVariable
from model.request import Request
from ui.collection_edit_area import CollectionEditArea
from ui.environment_edit_area import EnvironmentEditArea
from ui.request_edit_area import RequestEditArea

# I got the CustomNotebook from https://stackoverflow.com/a/39459376

class WorkArea(tk.Frame):
  def __init__(self, root):
    super().__init__(root)
    self.notebook = ttk.Notebook(self, style="CustomNotebook")
    self.notebook.pack(expand=True, fill=tk.BOTH)

    self._active = None

    self.notebook.bind("<ButtonPress-1>", self.on_close_press, True)
    self.notebook.bind("<ButtonRelease-1>", self.on_close_release)

    self.collection_id_to_edit_area: dict[int, CollectionEditArea] = {}
    self.environment_id_to_edit_area: dict[int, EnvironmentEditArea] = {}
    self.request_id_to_edit_area: dict[int, RequestEditArea] = {}

  def is_child(self, editArea: EnvironmentEditArea) -> bool:
    return str(editArea) in self.notebook.tabs()

  def open_environment(self, environment: Environment, highlighted_variable: Optional[EnvironmentVariable] = None):
    tab_frame = None
    if environment.tree_id in self.environment_id_to_edit_area and self.is_child(self.environment_id_to_edit_area[environment.tree_id]):
      tab_frame = self.environment_id_to_edit_area[environment.tree_id]
    else:
      tab_frame = EnvironmentEditArea(self.notebook, environment)
      envname, _ = environment.get_item_options()
      self.notebook.add(tab_frame, state=tk.NORMAL, sticky=tk.NSEW, text=envname)
      self.environment_id_to_edit_area[environment.tree_id] = tab_frame
    self.notebook.select(tab_frame)
    # FIXME this is hack and sucks real bad
    self.after(100, self.set_initial_highlight(tab_frame, highlighted_variable))

  def open_collection(self, collection: Collection):
    tab_frame = None
    if collection.tree_id in self.collection_id_to_edit_area and self.is_child(self.collection_id_to_edit_area[collection.tree_id]):
      tab_frame = self.collection_id_to_edit_area[collection.tree_id]
    else:
      tab_frame = CollectionEditArea(self.notebook, collection, self.open_request)
      collection_name, _ = collection.get_item_options()
      self.notebook.add(tab_frame, state=tk.NORMAL, sticky=tk.NSEW, text=collection_name)
      self.collection_id_to_edit_area[collection.tree_id] = tab_frame
    self.notebook.select(tab_frame)

  def open_request(self, request: Request):
    tab_frame = None
    if request.tree_id in self.request_id_to_edit_area and self.is_child(self.request_id_to_edit_area[request.tree_id]):
      tab_frame = self.request_id_to_edit_area[request.tree_id]
    else:
      tab_frame = RequestEditArea(self.notebook, request)
      request_name, _ = request.get_item_options()
      self.notebook.add(tab_frame, state=tk.NORMAL, sticky=tk.NSEW, text=request_name)
      self.request_id_to_edit_area[request.tree_id] = tab_frame
    self.notebook.select(tab_frame)

  def set_initial_highlight(self, tab_frame, highlighted_variable):
    def do_highlight():
      tab_frame.set_highlight_variable(highlighted_variable)
    return do_highlight

  def review_environment_tabs(self, environments: list[Environment]):
    alive_tabs = [env.tree_id for env in environments]
    editarea_ids = [id for id in self.environment_id_to_edit_area.keys()]
    for editarea_id in editarea_ids:
      if editarea_id not in alive_tabs:
        self.notebook.forget(self.environment_id_to_edit_area[editarea_id])
        del self.environment_id_to_edit_area[editarea_id]

  def review_collection_tabs(self, collections: list[Collection]):
    alive_tabs = [env.tree_id for env in collections]
    editarea_ids = [id for id in self.collection_id_to_edit_area.keys()]
    for editarea_id in editarea_ids:
      if editarea_id not in alive_tabs:
        self.notebook.forget(self.collection_id_to_edit_area[editarea_id])
        del self.collection_id_to_edit_area[editarea_id]

  def review_request_tabs(self, requests: list[Request]):
    alive_tabs = [env.tree_id for env in requests]
    editarea_ids = [id for id in self.request_id_to_edit_area.keys()]
    for editarea_id in editarea_ids:
      if editarea_id not in alive_tabs:
        self.notebook.forget(self.request_id_to_edit_area[editarea_id])
        del self.request_id_to_edit_area[editarea_id]

  def update_tab_name(self, tab_id: int, name: str):
    if tab_id in self.environment_id_to_edit_area:
      self.notebook.tab(str(self.environment_id_to_edit_area[tab_id]), text=name)
    if tab_id in self.collection_id_to_edit_area:
      self.notebook.tab(str(self.collection_id_to_edit_area[tab_id]), text=name)
    if tab_id in self.request_id_to_edit_area:
      self.notebook.tab(str(self.request_id_to_edit_area[tab_id]), text=name)

  def update_environment_tabs(self, environments: list[Environment]):
    for environment in environments:
      if environment.tree_id in self.environment_id_to_edit_area:
        self.notebook.tab(str(self.environment_id_to_edit_area[environment.tree_id]), text=environment.name)

  def on_close_press(self, event):
    element = self.notebook.identify(event.x, event.y)

    if "close" in element:
      index = self.notebook.index(f'@{event.x},{event.y}')

      self.notebook.state(['pressed'])
      self._active = index
      return "break"

  def on_close_release(self, event):
    if not self.notebook.instate(['pressed']):
      return

    element = self.notebook.identify(event.x, event.y)
    if "close" not in element:
      return

    index = self.notebook.index(f'@{event.x},{event.y}')

    if self._active == index:
      self.notebook.forget(index)
      self.notebook.event_generate("<<NotebookTabClosed>>")

    self.notebook.state(["!pressed"])
    self._active = None
