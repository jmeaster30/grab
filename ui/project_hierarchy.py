import tkinter as tk
from tkinter import ttk
from typing import Optional
from model.collection import Collection
from model.environment import Environment, EnvironmentVariable
from model.project import CollectionsSection, EnvironmentsSection, Project
from model.request import Request
from ui.left_right_buttons import LeftRightButtons
from ui.tree_viewable_item import TreeViewableItem
from util.getnewname import get_new_name

class ProjectHierarchy(tk.Frame):
  def __init__(self, root):
    super().__init__(root, highlightbackground="red", highlightthickness=2)
    self.max_id = 0

    self.project_name_var = tk.StringVar()
    self.project_name_entry = ttk.Entry(self, textvariable=self.project_name_var)
    self.tree = ttk.Treeview(self, show='tree', selectmode='browse')
    self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)

    self.tree.configure(yscrollcommand=self.scrollbar.set)
    self.tree.bind('<Double-Button-1>', self.on_double_click)
    self.tree.bind('<<TreeviewSelect>>', self.on_tree_selection)

    self.button_controls = LeftRightButtons(self, '+ Add', '- Remove')

    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)

    self.project_name_entry.grid(row=0, column=0, sticky=tk.EW)
    self.tree.grid(row=1, column=0, sticky=tk.NSEW)
    self.scrollbar.grid(row=1, column=1, sticky=tk.NS)
    self.button_controls.grid(row=2, column=0, sticky=tk.EW)

    self.tree_viewable_item_map: dict[str, TreeViewableItem] = {}
    self.on_environment_variable_click_action = None
    self.on_environment_add_remove_action = None
    self.on_environment_name_change = None
    self.on_collection_click_action = None
    self.on_collection_add_remove_action = None
    self.on_collection_name_change = None

  def on_double_click(self, event: tk.Event):
    tree_id = self.tree.identify_row(event.y)
    item = self.tree_viewable_item_map[tree_id]
    
    match item:
      case Environment():
        print(f"found environment: {item.get_item_options()[0]}")
        if self.on_environment_variable_click_action is not None:
          self.on_environment_variable_click_action(item, None)
      case EnvironmentVariable():
        parent_id = item.get_parent_id()
        print(parent_id)
        parent_item = self.tree_viewable_item_map[parent_id]
        print(f"found environment variable: {parent_item.get_item_options()[0]} -> {item.get_item_options()[0]}")
        if self.on_environment_variable_click_action is not None:
          self.on_environment_variable_click_action(parent_item, item)
      case Collection():
        print(f"found collection {item.name}")
        if self.on_collection_click_action is not None:
          self.on_collection_click_action(item)
      case _:
        print(f"unhandled item :( {item}")

  def on_tree_selection(self, event):
    if len(self.tree.selection()) == 0:
      self.add_button_controls(None, False, None)
      self.remove_button_controls(None, False, None)
      return

    item_id = self.tree.selection()[0]
    item = self.tree_viewable_item_map[item_id]
    match item:
      case CollectionsSection():
        self.add_button_controls("Collection", True, self.add_collection)
        self.remove_button_controls(None, False, None)
      case EnvironmentsSection():
        self.add_button_controls("Environment", True, self.add_environment)
        self.remove_button_controls(None, False, None)
      case Environment():
        self.add_button_controls("Environment", True, self.add_environment)
        self.remove_button_controls("Environment", True, self.remove_environment)
      case EnvironmentVariable():
        self.add_button_controls("Environment", True, self.add_environment)
        self.remove_button_controls(None, False, None)
      case Collection():
        self.add_button_controls("Collection", True, self.add_collection)
        self.remove_button_controls("Collection", True, self.remove_collection)
      case Request():
        self.add_button_controls("Request", True, self.add_request)
        self.remove_button_controls("Request", True, self.remove_request)
      case _:
        self.add_button_controls(None, False, None)
        self.remove_button_controls(None, False, None)

  def get_children(self, parent_id: Optional[int]) -> list[TreeViewableItem]:
    item_ids = self.tree.get_children(parent_id)
    return [self.tree_viewable_item_map[id] for id in item_ids]

  def add_item(self, tree_item: TreeViewableItem, is_open: bool = True) -> int:
    print(f"adding item to hierarchy {tree_item}")
    self.max_id += 1
    text, img = tree_item.get_item_options()
    print(self.max_id, text, img)
    self.tree.insert('', tk.END, text=text, iid=self.max_id, open=is_open)
    print(tree_item.get_parent_id())
    if tree_item.get_parent_id() is not None:
      child_num = len(self.tree.get_children(tree_item.get_parent_id()))
      self.tree.move(self.max_id, tree_item.get_parent_id(), child_num)
    self.tree_viewable_item_map[str(self.max_id)] = tree_item
    tree_item.tree_id = str(self.max_id)
    return self.max_id

  def add_button_controls(self, text: Optional[str], clickable: bool, action: Optional[callable]):
    self.button_controls.update_left_button_text(f'+ {"Add" if text is None else text}')
    self.button_controls.set_left_button_clickable(clickable)
    self.button_controls.left_button_action = action

  def remove_button_controls(self, text: Optional[str], clickable: bool, action: Optional[callable]):
    self.button_controls.update_right_button_text(f'- {"Remove" if text is None else text}')
    self.button_controls.set_right_button_clickable(clickable)
    self.button_controls.right_button_action = action

  def add_environment(self):
    new_env_name = get_new_name('Environment', [env.name for env in Project().environments])
    Project().add_new_environment(new_env_name)
    Project().refresh_environments()
    if self.on_environment_add_remove_action is not None:
        self.on_environment_add_remove_action(Project().environments)

  def remove_environment(self):
    item_id = self.tree.selection()[0]
    item = self.tree_viewable_item_map[item_id]
    match item:
      case Environment():
        Project().remove_environment(item)
        Project().refresh_environments()
        if self.on_environment_add_remove_action is not None:
          self.on_environment_add_remove_action(Project().environments)
      case _:
        print(f"Unexpected item in remove_environment call {item}")

  def add_collection(self):
    new_collection_name = get_new_name('Collection', [coll.name for coll in Project().collections])
    Project().add_new_collection(new_collection_name)
    Project().refresh_collections()
    if self.on_collection_add_remove_action is not None:
        self.on_collection_add_remove_action(Project().collections)

  def remove_collection(self):
    item_id = self.tree.selection()[0]
    item = self.tree_viewable_item_map[item_id]
    match item:
      case Collection():
        Project().remove_collection(item)
        Project().refresh_collections()
        if self.on_collection_add_remove_action is not None:
          self.on_collection_add_remove_action(Project().collections)
      case _:
        print(f"Unexpected item in remove_collection call {item}")

  def add_request(self):
    print("add request")

  def remove_request(self):
    print("remove request")
