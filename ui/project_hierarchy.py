import tkinter as tk
from tkinter import ttk
from typing import Optional
from model.environment import Environment, EnvironmentVariable
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
    self.tree.bind('<Double-Button-1>', func=self.on_double_click)

    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)

    self.project_name_entry.grid(row=0, column=0, sticky=tk.EW)
    self.tree.grid(row=1, column=0, sticky=tk.NSEW)
    self.scrollbar.grid(row=1, column=1, sticky=tk.NS)

    self.tree_viewable_item_map: dict[str, TreeViewableItem] = {}
    self.on_environment_variable_click_action = None

  def on_double_click(self, event: tk.Event):
    tree_id = self.tree.identify_row(event.y)
    item = self.tree_viewable_item_map[tree_id]
    
    # We can't import these types here :(
    match item:
      case Environment():
        print(f"found environment: {item.get_item_options()[0]}")
        if self.on_environment_variable_click_action is not None:
          self.on_environment_variable_click_action(item, None)
      case EnvironmentVariable():
        parent_id = self.tree.parent(tree_id)
        parent_item = self.tree_viewable_item_map[parent_id]
        print(f"found environment variable: {parent_item.get_item_options()[0]} -> {item.get_item_options()[0]}")
        if self.on_environment_variable_click_action is not None:
          self.on_environment_variable_click_action(parent_item, item)
      case _:
        print(f"unhandled item :( {item}")


  def add_item(self, parent_id: Optional[int], tree_item: TreeViewableItem) -> int:
    self.max_id += 1
    text, img, is_open = tree_item.get_item_options()
    print(self.max_id, text, img, is_open)
    self.tree.insert('', tk.END, text=text, iid=self.max_id, open=is_open)
    if parent_id is not None:
      child_num = len(self.tree.get_children(parent_id))
      self.tree.move(self.max_id, parent_id, child_num)
    self.tree_viewable_item_map[str(self.max_id)] = tree_item
    return self.max_id

  def backing_data_changed(self, item: TreeViewableItem):
    item.refresh(self)
