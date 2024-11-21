import tkinter as tk
from typing import Optional
from model.project_item import ProjectItem
from ui.tree_viewable_item import TreeViewableItem
from ui.view.collection.request_tree_item import RequestTreeItem

from lilytk.events import ClassListens

@ClassListens('Collection.NameUpdated', 'update_name')
class CollectionTreeItem(TreeViewableItem):
  def __init__(self, parent: TreeViewableItem, project_hierarchy, collection_name: str, collection_id: str):
    super().__init__(parent, project_hierarchy, collection_id, ProjectItem.Collection)
    self.collection_id = collection_id
    self.collection_name = collection_name
    self.requests: list[RequestTreeItem] = []

  def update_name(self, data):
    (col_id, name) = data
    if col_id == self.collection_id:
      self.collection_name = name
      self.refresh()

  def get_item_options(self) -> tuple[str, Optional[tk.Image]]:
    return self.name, None

  def refresh(self):
    super().refresh()
    for request in self.requests:
      request.refresh()
    # need to go through and remove the rows from the treeview that are not there any more
    remaining_tree_ids = [str(var.tree_id) for var in self.variables]
    for child_id in self.project_hierarchy.tree.get_children(self.tree_id):
      if str(child_id) not in remaining_tree_ids:
        self.project_hierarchy.tree.delete(child_id)