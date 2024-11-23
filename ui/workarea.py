import tkinter as tk
from tkinter import ttk
from typing import Collection, Optional

from lilytk.events import ClassListens

from model.environment import Environment, EnvironmentVariable
from model.project import Project
from model.project_item import ProjectItem
from model.request import Request
from ui.collection_edit_area import CollectionEditArea
from ui.environment_edit_area import EnvironmentEditArea
from ui.request_edit_area import RequestEditArea
from util.ui_error_handler import UIErrorHandler

# I got the CustomNotebook from https://stackoverflow.com/a/39459376

@ClassListens('Collection.NameUpdated', 'update_collection_tabs')
@ClassListens('Environment.NameUpdated', 'update_environment_tabs')
@ClassListens('Request.NameUpdated', 'update_request_tabs')
@ClassListens('Environment.Add', 'review_environment_tabs')
@ClassListens('Environment.Remove', 'review_environment_tabs')
@ClassListens('ProjectHierarchy.ItemClicked', 'open_item')
class WorkArea(tk.Frame):
  def __init__(self, root):
    super().__init__(root)
    self.notebook = ttk.Notebook(self, style="CustomNotebook")
    self.notebook.pack(expand=True, fill=tk.BOTH)

    self._active = None

    self.notebook.bind("<ButtonPress-1>", self.on_close_press, True)
    self.notebook.bind("<ButtonRelease-1>", self.on_close_release)

    self.collection_id_to_edit_area: dict[str, CollectionEditArea] = {}
    self.environment_id_to_edit_area: dict[str, EnvironmentEditArea] = {}
    self.request_id_to_edit_area: dict[str, RequestEditArea] = {}

  def is_child(self, editArea: EnvironmentEditArea) -> bool:
    return str(editArea) in self.notebook.tabs()

  @UIErrorHandler("Edit area error", "There was an error trying to open an edit area!\nCheck the console for exceptions.")
  def open_item(self, data):
    # TODO this could use some better error handling
    (project_item_type, object_id, parent_id) = data
    match project_item_type:
      case ProjectItem.Environment:
        self.open_environment(Project().environments[object_id])
      case ProjectItem.EnvironmentVariable:
        env = Project().environments[parent_id.object_id]
        variables = [envvar for envvar in env.variables if envvar.id == object_id]
        if len(variables) != 1:
          raise ValueError(f"Couldn't find environment variable with id '{object_id}' in environment '{env.name}'")
        self.open_environment(env, variables[0])
      case ProjectItem.Collection:
        self.open_collection(Project().collections[object_id])
      case ProjectItem.Request:
        col = Project().collections[parent_id.object_id]
        request = col.requests[object_id]
        self.open_request(request)

  def open_environment(self, environment: Environment, highlighted_variable: Optional[EnvironmentVariable] = None):
    tab_frame = None
    if environment.id in self.environment_id_to_edit_area and self.is_child(self.environment_id_to_edit_area[environment.id]):
      tab_frame = self.environment_id_to_edit_area[environment.id]
    else:
      tab_frame = EnvironmentEditArea(self.notebook, environment)
      self.notebook.add(tab_frame, state=tk.NORMAL, sticky=tk.NSEW, text=environment.name)
      self.environment_id_to_edit_area[environment.id] = tab_frame
    self.notebook.select(tab_frame)
    # FIXME this is hack and sucks real bad
    self.after(100, self.set_initial_highlight(tab_frame, highlighted_variable))

  def open_collection(self, collection: Collection):
    tab_frame = None
    if collection.id in self.collection_id_to_edit_area and self.is_child(self.collection_id_to_edit_area[collection.id]):
      tab_frame = self.collection_id_to_edit_area[collection.id]
    else:
      tab_frame = CollectionEditArea(self.notebook, collection, self.open_request)
      self.notebook.add(tab_frame, state=tk.NORMAL, sticky=tk.NSEW, text=collection.name)
      self.collection_id_to_edit_area[collection.id] = tab_frame
    self.notebook.select(tab_frame)

  def open_request(self, request: Request):
    tab_frame = None
    if request.id in self.request_id_to_edit_area and self.is_child(self.request_id_to_edit_area[request.id]):
      tab_frame = self.request_id_to_edit_area[request.id]
    else:
      tab_frame = RequestEditArea(self.notebook, request)
      self.notebook.add(tab_frame, state=tk.NORMAL, sticky=tk.NSEW, text=request.name)
      self.request_id_to_edit_area[request.id] = tab_frame
    self.notebook.select(tab_frame)

  def set_initial_highlight(self, tab_frame, highlighted_variable):
    def do_highlight():
      tab_frame.set_highlight_variable(highlighted_variable)
    return do_highlight

  # FIXME weird that this is different
  def review_environment_tabs(self, data):
    alive_tabs = [env.id for env in Project().environments.values()]
    editarea_ids = [id for id in self.environment_id_to_edit_area.keys()]
    for editarea_id in editarea_ids:
      if editarea_id not in alive_tabs:
        self.notebook.forget(self.environment_id_to_edit_area[editarea_id])
        del self.environment_id_to_edit_area[editarea_id]

  def review_collection_tabs(self, collections: list[Collection]):
    alive_tabs = [col.id for col in collections]
    editarea_ids = [id for id in self.collection_id_to_edit_area.keys()]
    for editarea_id in editarea_ids:
      if editarea_id not in alive_tabs:
        self.notebook.forget(self.collection_id_to_edit_area[editarea_id])
        del self.collection_id_to_edit_area[editarea_id]

  def review_request_tabs(self, requests: list[Request]):
    alive_tabs = [env.id for env in requests]
    editarea_ids = [id for id in self.request_id_to_edit_area.keys()]
    for editarea_id in editarea_ids:
      if editarea_id not in alive_tabs:
        self.notebook.forget(self.request_id_to_edit_area[editarea_id])
        del self.request_id_to_edit_area[editarea_id]

  def update_environment_tabs(self, data):
    for environment in Project().environments.values():
      if environment.id in self.environment_id_to_edit_area:
        self.notebook.tab(str(self.environment_id_to_edit_area[environment.id]), text=environment.name)

  def update_collection_tabs(self, data):
    for collection in Project().collections.values():
      if collection.id in self.collection_id_to_edit_area:
        self.notebook.tab(str(self.collection_id_to_edit_area[collection.id]), text=collection.name)

  def update_request_tabs(self, data):
    request_id, name = data
    if request_id in self.request_id_to_edit_area:
        self.notebook.tab(str(self.request_id_to_edit_area[request_id]), text=name)

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
