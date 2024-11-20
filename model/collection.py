import tkinter as tk
from typing import Optional

from lilytk.events import Notifies

from model.request import Request
from ui.tree_viewable_item import TreeViewableItem

class Collection(TreeViewableItem):
  def __init__(self, parent: TreeViewableItem, collection_name: str = "New Collection"):
    super().__init__(parent)
    self.name: str = collection_name
    self.requests: list[Request] = []

  def add_request(self, request: Request):
    self.requests.append(request)

  @Notifies('Collection.NameUpdated')
  def set_name(self, name: str):
    self.name = name
    self.refresh()
  
  def get_item_options(self) -> tuple[str, Optional[tk.Image]]:
    return self.name, None

  def set_hierarchy(self, hierarchy):
    super().set_hierarchy(hierarchy)
    for request in self.requests:
      request.set_hierarchy(hierarchy)

  def refresh(self):
    if self.project_hierarchy is None:
      return
    super().refresh()
    for request in self.requests:
      request.refresh()

