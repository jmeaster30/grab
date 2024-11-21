import tkinter as tk
from typing import Optional

from model.project_item import ProjectItem

class TreeViewableItem:
  def __init__(self, parent: Optional['TreeViewableItem'], project_hierarchy, object_id: Optional[str] = None, project_item_type: Optional[ProjectItem] = None):
    self.tree_id: Optional[str] = None
    self.project_item_type: Optional[ProjectItem] = project_item_type 
    self.object_id: Optional[str] = object_id
    self.parent = parent
    self.project_hierarchy = project_hierarchy

  def __eq__(self, other):
    if not isinstance(other, TreeViewableItem):
      return False
    return self.tree_id == other.tree_id

  def get_item_options(self) -> tuple[str, tk.Image]:
    pass

  def get_parent_id(self) -> Optional[str]:
    if self.parent is None:
      return None
    return str(self.parent.tree_id)

  def refresh(self, is_open: bool = False):
    is_already_open = is_open
    if self.tree_id is None:
      self.tree_id = str(self.project_hierarchy.add_item(self))
    else:
      is_already_open = self.project_hierarchy.tree.item(self.tree_id, option='open')

    text, img = self.get_item_options()
    self.project_hierarchy.tree.item(self.tree_id, option=None, text=text, open=is_already_open)
