import tkinter as tk
from typing import Optional
from model.collection import Collection
from model.environment import Environment
from ui.grab_tree_viewer import GrabTreeViewer
from ui.tree_viewable_item import TreeViewableItem

class Project:
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(Project, cls).__new__(cls)
    return cls.instance

  def __init__(self):
    self.name = "New Project"
    self.environments: dict[str, Environment] = {}
    self.collections: dict[str, Collection] = {}

    self.environments_section: Optional[EnvironmentsSection] = None
    self.collections_section: Optional[CollectionsSection] = None

  def refresh_project(self, tree: GrabTreeViewer):
    tree.heading('#0', text=self.name, anchor=tk.W)
    self.refresh_environments(tree)
    self.refresh_collections(tree)

  def refresh_environments(self, tree: GrabTreeViewer):
    if self.environments_section is None:
      self.environments_section = EnvironmentsSection(tree)
    else:
      self.environments_section.refresh(tree)
    
    for _, environment in self.environments.items():
      environment.refresh(tree, self.environments_section.id)

  def refresh_collections(self, tree: GrabTreeViewer):
    if self.collections_section is None:
      self.collections_section = CollectionsSection(tree)
    else:
      self.collections_section.refresh(tree)
    
    for _, collection in self.collections.items():
      collection.refresh(tree, self.collections_section.id)

  def add_new_environment(self, env_name: str):
    self.environments[env_name] = Environment(env_name)
    return self.environments[env_name]

  def remove_environment(self, env_name: str):
    del self.environments[env_name]


class CollectionsSection(TreeViewableItem):
  def __init__(self, tree: GrabTreeViewer):
    self.id = tree.add_item(None, self)

  def get_item_options(self) -> tuple[str, Optional[tk.Image], bool]:
    return "Collections", None, True


class EnvironmentsSection(TreeViewableItem):
  def __init__(self, tree: GrabTreeViewer):
    self.id = tree.add_item(None, self)

  def get_item_options(self) -> tuple[str, Optional[tk.Image], bool]:
    return "Environments", None, True
