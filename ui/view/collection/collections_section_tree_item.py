import tkinter as tk
from typing import Optional
from ui.tree_viewable_item import TreeViewableItem


class CollectionsSection(TreeViewableItem):
  def get_item_options(self) -> tuple[str, Optional[tk.Image]]:
    return "Collections", None

