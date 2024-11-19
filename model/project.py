import tkinter as tk
from typing import Optional
from model.collection import Collection
from model.environment import Environment
from ui.tree_viewable_item import TreeViewableItem
from lilytk.utils import Singleton

@Singleton
class Project:  
  def __init__(self, name="Empty Project"):
    self.name = name
    self.environments: list[Environment] = []
    self.collections: list[Collection] = []

    self.environments_section = EnvironmentsSection(None)
    self.collections_section = CollectionsSection(None)

    self.project_hierarchy = None

  def refresh_project(self):
    self.project_hierarchy.project_name_var.set(self.name)
    self.refresh_environments()
    self.refresh_collections()

  def refresh_environments(self):
    self.environments_section.refresh()
    for environment in self.environments:
      environment.refresh()

    self.remove_dead_environment_branches()

  def refresh_collections(self):
    self.collections_section.refresh()
    for collection in self.collections:
      collection.refresh()

    self.remove_dead_collection_branches()

  def remove_dead_environment_branches(self):
    for item in self.project_hierarchy.get_children(self.environments_section.tree_id):
      if item.tree_id not in [env.tree_id for env in self.environments]:
        self.project_hierarchy.tree.delete(item.tree_id)

  def remove_dead_collection_branches(self):
    for item in self.project_hierarchy.get_children(self.collections_section.tree_id):
      if item.tree_id not in [coll.tree_id for coll in self.collections]:
        self.project_hierarchy.tree.delete(item.tree_id)

  def add_new_environment(self, env_name: Optional[str]):
    env = Environment(self.environments_section, env_name)
    env.set_hierarchy(self.project_hierarchy)
    self.environments.append(env)
    return env

  def remove_environment(self, environment: Environment):
    self.environments.remove(environment)

  def add_new_collection(self, collection_name: Optional[str]):
    collection = Collection(self.collections_section, collection_name)
    collection.set_hierarchy(self.project_hierarchy)
    self.collections.append(collection)
    return collection
  
  def remove_collection(self, collection: Collection):
    self.collections.remove(collection)

  def set_hierarchy(self, hierarchy):
    self.project_hierarchy = hierarchy
    self.environments_section.set_hierarchy(hierarchy)
    self.collections_section.set_hierarchy(hierarchy)
    for env in self.environments:
      env.set_hierarchy(hierarchy)

    for collection in self.collections:
      collection.set_hierarchy(hierarchy)

class CollectionsSection(TreeViewableItem):
  def get_item_options(self) -> tuple[str, Optional[tk.Image]]:
    return "Collections", None


class EnvironmentsSection(TreeViewableItem):
  def get_item_options(self) -> tuple[str, Optional[tk.Image]]:
    return "Environments", None
