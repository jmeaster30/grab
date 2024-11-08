import tkinter as tk
from typing import Optional
from model.collection import Collection
from model.environment import Environment
from ui.tree_viewable_item import TreeViewableItem
from util.singleton import Singleton

@Singleton
class Project:  
  def __init__(self, name="Empty Project"):
    self.name = name
    self.environments: dict[str, Environment] = {}
    self.collections: dict[str, Collection] = {}

    self.environments_section = EnvironmentsSection(None)
    self.collections_section = CollectionsSection(None)

    self.project_hierarchy = None

  def refresh_project(self):
    self.project_hierarchy.project_name_var.set(self.name)
    self.refresh_environments()
    self.refresh_collections()

  def refresh_environments(self):
    self.environments_section.refresh()
    for _, environment in self.environments.items():
      environment.refresh()

    for item in self.project_hierarchy.get_children(self.environments_section.tree_id):
      if item.tree_id not in [env.tree_id for env in self.environments.values()]:
        print(f"deleting {item.tree_id}")
        self.project_hierarchy.tree.delete(item.tree_id)

  def refresh_collections(self):
    self.collections_section.refresh()
    for _, collection in self.collections.items():
      collection.refresh()

  def add_new_environment(self, env_name: Optional[str]):
    env = Environment(self.environments_section, env_name)
    self.environments[env.name] = env
    return self.environments[env.name]

  def remove_environment(self, env_name: str):
    del self.environments[env_name]

  def add_new_collection(self, collection_name: Optional[str]):
    collection = Collection(self.collections_section, collection_name)
    self.collections[collection.name] = collection
    return self.collections[collection.name]
  
  def remove_collection(self, env_name: str):
    del self.collections[env_name]

  def set_hierarchy(self, hierarchy):
    self.project_hierarchy = hierarchy
    self.environments_section.set_hierarchy(hierarchy)
    self.collections_section.set_hierarchy(hierarchy)
    for name, env in self.environments.items():
      env.set_hierarchy(hierarchy)

    for name, collection in self.collections.items():
      collection.set_hierarchy(hierarchy)

class CollectionsSection(TreeViewableItem):
  def get_item_options(self) -> tuple[str, Optional[tk.Image]]:
    return "Collections", None


class EnvironmentsSection(TreeViewableItem):
  def get_item_options(self) -> tuple[str, Optional[tk.Image]]:
    return "Environments", None
