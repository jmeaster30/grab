from enum import Enum
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from lilytk.events import Notifies, ClassListens

from model.collection import Collection
from model.project import Project
from model.project_item import ProjectItem
from ui.left_right_buttons import LeftRightButtons
from ui.tree_viewable_item import TreeViewableItem
from ui.view.collection.collection_tree_item import CollectionTreeItem
from ui.view.collection.collections_section_tree_item import CollectionsSection
from ui.view.collection.request_tree_item import RequestTreeItem
from ui.view.environment.environment_tree_item import EnvironmentTreeItem
from ui.view.environment.environment_variable_tree_item import EnvironmentVariableTreeItem
from ui.view.environment.environments_section_tree_item import EnvironmentsSection
from util.getnewname import get_new_name

@ClassListens('Project.NameUpdated', 'refresh_project')
@ClassListens('Environment.Add', 'create_environment_tree_item')
@ClassListens('Environment.Remove', 'refresh_environments')
@ClassListens('Collection.Add', 'create_collection_tree_item')
@ClassListens('Collection.Remove', 'refresh_collections')
class ProjectHierarchy(tk.Frame):
  def __init__(self, root):
    super().__init__(root)
    self.max_id = 0

    self.project_name_var = tk.StringVar(value=Project().name)
    self.project_name_entry = ttk.Entry(self, textvariable=self.project_name_var)
    self.project_name_entry.bind('<KeyRelease>', self.project_name_changed)

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

    self.environments_section = EnvironmentsSection(None, self)
    self.environments_section.tree_id = self.add_item(self.environments_section, True)
    self.collections_section = CollectionsSection(None, self)
    self.collections_section.tree_id = self.add_item(self.collections_section, True)

  def refresh_project(self, data):
    self.project_name_var.set(data)

  def refresh_environments(self, data):
    self.environments_section.refresh()
    env_uuids = Project().environments.keys()
    for tree_item in self.get_children(self.environments_section.tree_id):
      if tree_item.tree_id not in self.tree_viewable_item_map.keys():
        self.tree.delete(tree_item.tree_id)
      elif tree_item.project_item_type == ProjectItem.Environment:
        if tree_item.environment_id in env_uuids:
          tree_item.refresh()
        else:
          self.tree.delete(tree_item.tree_id)

  def refresh_collections(self, data):
    self.collections_section.refresh()
    col_uuids = Project().collections.keys()
    for tree_item in self.get_children(self.collections_section.tree_id):
      if tree_item.tree_id not in self.tree_viewable_item_map.keys():
        self.tree.delete(tree_item.tree_id)
      elif tree_item.project_item_type == ProjectItem.Collection:
        if tree_item.collection_id in col_uuids:
          tree_item.refresh()
        else:
          self.tree.delete(tree_item.tree_id)

  @Notifies('ProjectHierarchy.ItemClicked')
  def on_double_click(self, event: tk.Event):
    tree_id = self.tree.identify_row(event.y)
    item = self.tree_viewable_item_map[tree_id]
    return item.project_item_type, item.object_id, item.get_parent_id()

  def get_by_tree_id(self, tree_id: str) -> Optional[TreeViewableItem]:
    for item in self.tree_viewable_item_map.values():
      if item.tree_id == tree_id:
        return item
    return None

  def on_tree_selection(self, event):
    if len(self.tree.selection()) == 0:
      self.add_button_controls(None, False, None)
      self.remove_button_controls(None, False, None)
      return

    item_id = self.tree.selection()[0]
    item = self.get_by_tree_id(item_id)
    match item:
      case CollectionsSection():
        self.add_button_controls("Collection", True, self.add_collection)
        self.remove_button_controls(None, False, None)
      case EnvironmentsSection():
        self.add_button_controls("Environment", True, self.add_environment)
        self.remove_button_controls(None, False, None)
      case _:
        match item.project_item_type:
          case ProjectItem.Environment:
            self.add_button_controls("Environment", True, self.add_environment)
            self.remove_button_controls("Environment", True, self.remove_environment)
          case ProjectItem.EnvironmentVariable:
            self.add_button_controls("Environment", True, self.add_environment)
            self.remove_button_controls(None, False, None)
          case ProjectItem.Collection:
            self.add_button_controls("Collection", True, self.add_collection)
            self.remove_button_controls("Collection", True, self.remove_collection)
          case ProjectItem.Request:
            self.add_button_controls("Collection", True, self.add_collection)
            self.remove_button_controls(None, False, None)
          case _:
            self.add_button_controls(None, False, None)
            self.remove_button_controls(None, False, None)

  def get_children(self, parent_id: Optional[str]) -> list[TreeViewableItem]:
    item_ids = self.tree.get_children(parent_id)
    return [self.tree_viewable_item_map[id] for id in item_ids]

  def add_item(self, tree_item: TreeViewableItem, is_open: bool = True) -> str:
    self.max_id += 1
    self.max_id_str = str(self.max_id)
    text, _ = tree_item.get_item_options()
    self.tree.insert('', tk.END, text=text, iid=self.max_id_str, open=is_open)
    if tree_item.get_parent_id() is not None:
      child_num = len(self.get_children(tree_item.get_parent_id().tree_id))
      self.tree.move(self.max_id_str, tree_item.get_parent_id().tree_id, child_num)
    self.tree_viewable_item_map[self.max_id_str] = tree_item
    return self.max_id_str

  def add_button_controls(self, text: Optional[str], clickable: bool, action: Optional[Callable]):
    self.button_controls.update_left_button_text(f'+ {"Add" if text is None else text}')
    self.button_controls.set_left_button_clickable(clickable)
    self.button_controls.left_button_action = action

  def remove_button_controls(self, text: Optional[str], clickable: bool, action: Optional[Callable]):
    self.button_controls.update_right_button_text(f'- {"Remove" if text is None else text}')
    self.button_controls.set_right_button_clickable(clickable)
    self.button_controls.right_button_action = action

  def add_environment(self):
    new_env_name = get_new_name('Environment', [env.name for env in Project().environments.values()])
    Project().add_new_environment(new_env_name)

  def create_environment_tree_item(self, environment):
    tree_item = EnvironmentTreeItem(self.environments_section, self, environment.name, environment.id)
    tree_item.tree_id = self.add_item(tree_item)
    self.refresh_environments(None)

  def remove_environment(self):
    item_id = self.tree.selection()[0]
    item = self.tree_viewable_item_map[item_id]
    match item:
      case EnvironmentTreeItem():
        Project().remove_environment(item.environment_id)
      case _:
        print(f"Unexpected item in remove_environment call {item}")

  def add_collection(self):
    new_collection_name = get_new_name('Collection', [coll.name for coll in Project().collections.values()])
    Project().add_new_collection(new_collection_name)

  def create_collection_tree_item(self, collection):
    tree_item = CollectionTreeItem(self.collections_section, self, collection.name, collection.id)
    tree_item.tree_id = self.add_item(tree_item)
    self.refresh_collections(None)

  def remove_collection(self):
    item_id = self.tree.selection()[0]
    item = self.tree_viewable_item_map[item_id]
    match item:
      case Collection():
        Project().remove_collection(item.collection_id)
      case _:
        print(f"Unexpected item in remove_collection call {item}")

  def project_name_changed(self, event):
    Project().set_name(self.project_name_var.get())
