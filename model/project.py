import tkinter as tk
from typing import Optional
from model.collection import Collection
from model.environment import Environment
from ui.project_hierarchy import ProjectHierarchy
from ui.tree_viewable_item import TreeViewableItem
from util.singleton import Singleton

@Singleton
class Project:  
  def __init__(self, name="Empty Project"):
    self.name = name
    self.environments: dict[str, Environment] = {}
    self.collections: dict[str, Collection] = {}

    self.environments_section = EnvironmentsSection()
    self.collections_section = CollectionsSection()

  def refresh_project(self, hierarchy: ProjectHierarchy):
    hierarchy.project_name_var.set(self.name)
    self.refresh_environments(hierarchy)
    self.refresh_collections(hierarchy)

  def refresh_environments(self, hierarchy: ProjectHierarchy):
    self.environments_section.refresh(hierarchy)
    for _, environment in self.environments.items():
      environment.refresh(hierarchy, self.environments_section.tree_id)

  def refresh_collections(self, hierarchy: ProjectHierarchy):
    self.collections_section.refresh(hierarchy)
    for _, collection in self.collections.items():
      collection.refresh(hierarchy, self.collections_section.tree_id)

  def add_new_environment(self, env_name: str):
    self.environments[env_name] = Environment(env_name)
    return self.environments[env_name]

  def remove_environment(self, env_name: str):
    del self.environments[env_name]

  def add_new_collection(self, collection_name: str):
    self.collections[collection_name] = Collection(collection_name)
    return self.collections[collection_name]


class CollectionsSection(TreeViewableItem):
  def get_item_options(self) -> tuple[str, Optional[tk.Image], bool]:
    return "Collections", None, True


class EnvironmentsSection(TreeViewableItem):
  def get_item_options(self) -> tuple[str, Optional[tk.Image], bool]:
    return "Environments", None, True
