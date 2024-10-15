import tkinter as tk
from tkinter import ttk
from typing import Optional
from ui.tree_viewable_item import TreeViewableItem

class GrabTreeViewer(ttk.Treeview):
  def __init__(self, root):
    super().__init__(root)
    self.max_id = 0
    self.scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.yview)
    self.configure(yscrollcommand=self.scrollbar.set)
  
    self.grid(row=0, column=0, sticky=tk.NSEW)
    self.scrollbar.grid(row=0, column=1, sticky='ns')
  
    self.tree_viewable_item_map: dict[int, TreeViewableItem] = {}
  

  def add_item(self, parent_id: Optional[int], tree_item: TreeViewableItem) -> int:
    self.max_id += 1
    text, img, is_open = tree_item.get_item_options()
    print(self.max_id, text, img, is_open)
    self.insert('', tk.END, text=text, iid=self.max_id, open=is_open)
    if parent_id is not None:
      child_num = len(self.get_children(parent_id))
      self.move(self.max_id, parent_id, child_num)
    self.tree_viewable_item_map[self.max_id] = tree_item
    return self.max_id

  def backing_data_changed(self, item: TreeViewableItem):
    item.refresh(self)

  def item_selected(event):
    print(event)