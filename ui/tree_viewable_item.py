import tkinter as tk
from typing import Optional

class TreeViewableItem:
  def __init__(self, parent: Optional['TreeViewableItem']):
    self.tree_id = None
    self.parent = parent
    self.project_hierarchy = None

  def get_item_options(self) -> tuple[str, tk.Image]:
    pass

  def get_parent_id(self) -> Optional[str]:
    if self.parent is None:
      return None
    print(self.parent)
    return str(self.parent.tree_id)

  def set_hierarchy(self, hierarchy):
    self.project_hierarchy = hierarchy

  # Purposefully doesn't have type annotation for 'tree'
  def refresh(self, is_open: bool = False):
    if self.tree_id is None:
      self.tree_id = self.project_hierarchy.add_item(self)

    text, img = self.get_item_options()
    self.project_hierarchy.tree.item(self.tree_id, option=None, text=text, open=is_open)
