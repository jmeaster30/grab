import tkinter as tk
from typing import Optional
from model.request import Request
from ui.tree_viewable_item import TreeViewableItem

class Collection(TreeViewableItem):
  def __init__(self, collection_name: str = "New Collection"):
    super().__init__()
    self.name = collection_name
    self.requests = []

  def add_request(self, request: Request):
    self.requests.append(request)
  
  def get_item_options(self) -> tuple[str, Optional[tk.Image], bool]:
    return self.name, None, False

  def refresh(self, hierarchy, parent_id: Optional[int]):
    super().refresh(hierarchy, parent_id)
    for request in self.requests:
      request.refresh(hierarchy, self.tree_id)

