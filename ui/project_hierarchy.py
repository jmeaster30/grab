import tkinter as tk
from tkinter import ttk
from typing import Optional
from ui.tree_viewable_item import TreeViewableItem

class ProjectHierarchy(tk.Frame):
  def __init__(self, root):
    super().__init__(root, highlightbackground="red", highlightthickness=2)
    self.max_id = 0

    self.project_name_var = tk.StringVar()
    self.project_name_entry = ttk.Entry(self, textvariable=self.project_name_var)
    self.tree = ttk.Treeview(self, show='tree')
    self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)

    self.tree.configure(yscrollcommand=self.scrollbar.set)

    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)

    self.project_name_entry.grid(row=0, column=0, sticky=tk.EW)
    self.tree.grid(row=1, column=0, sticky=tk.NSEW)
    self.scrollbar.grid(row=1, column=1, sticky=tk.NS)

    self.tree_viewable_item_map: dict[int, TreeViewableItem] = {}


  def add_item(self, parent_id: Optional[int], tree_item: TreeViewableItem) -> int:
    self.max_id += 1
    text, img, is_open = tree_item.get_item_options()
    print(self.max_id, text, img, is_open)
    self.tree.insert('', tk.END, text=text, iid=self.max_id, open=is_open)
    if parent_id is not None:
      child_num = len(self.tree.get_children(parent_id))
      self.tree.move(self.max_id, parent_id, child_num)
    self.tree_viewable_item_map[self.max_id] = tree_item
    return self.max_id

  def backing_data_changed(self, item: TreeViewableItem):
    item.refresh(self)
