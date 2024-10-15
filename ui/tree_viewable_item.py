import tkinter as tk
from typing import Optional

class TreeViewableItem:
  def get_item_options(self) -> tuple[str, tk.Image, bool]:
    pass

  # Purposefully doesn't have type annotation for 'tree'
  def refresh(self, tree, parent_id: Optional[int] = None):
    text, img, is_open = self.get_item_options()
    tree.item(self.id, None, text=text, image=img, open=is_open)

