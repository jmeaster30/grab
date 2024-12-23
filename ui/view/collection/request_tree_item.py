import tkinter as tk
from typing import Optional
from model.project_item import ProjectItem
from ui.tree_viewable_item import TreeViewableItem

from lilytk.events import ClassListens

@ClassListens('Request.NameUpdated', 'update_name')
class RequestTreeItem(TreeViewableItem):
  def __init__(self, parent: TreeViewableItem, project_hierarchy, request_name: str, request_id: str):
    super().__init__(parent, project_hierarchy, request_id, ProjectItem.Request)
    self.request_id = request_id
    self.request_name = request_name

  def update_name(self, data):
    (request_id, name) = data
    if request_id == self.request_id:
      self.request_name = name
      self.refresh()

  def get_item_options(self) -> tuple[str, Optional[tk.Image]]:
    return self.request_name, None