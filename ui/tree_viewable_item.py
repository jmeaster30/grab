import tkinter as tk
from typing import Optional

class TreeViewableItem:
  def __init__(self):
    self.tree_id = None

  def get_item_options(self) -> tuple[str, tk.Image, bool]:
    pass

  # Purposefully doesn't have type annotation for 'tree'
  def refresh(self, hierarchy, parent_id: Optional[int] = None):
    if self.tree_id is None:
      self.tree_id = hierarchy.add_item(parent_id, self)

    text, img, is_open = self.get_item_options()
    hierarchy.tree.item(self.tree_id, option=None, text=text, open=is_open)
