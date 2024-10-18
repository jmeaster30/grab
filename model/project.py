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

    self.environments_section = EnvironmentsSection()
    self.collections_section = CollectionsSection()


  # FIXME: I really dislike having so much UI oriented code in my models here :(
  def refresh_project(self, hierarchy):
    hierarchy.project_name_var.set(self.name)
    self.refresh_environments(hierarchy)
    self.refresh_collections(hierarchy)

  def refresh_environments(self, hierarchy):
    self.environments_section.refresh(hierarchy)
    print(self.environments)
    for _, environment in self.environments.items():
      environment.refresh(hierarchy, self.environments_section.tree_id)

    for item in hierarchy.get_children(self.environments_section.tree_id):
      if item.tree_id not in [env.tree_id for env in self.environments.values()]:
        print(f"deleting {item.tree_id}")
        hierarchy.tree.delete(item.tree_id)

  def refresh_collections(self, hierarchy):
    self.collections_section.refresh(hierarchy)
    for _, collection in self.collections.items():
      collection.refresh(hierarchy, self.collections_section.tree_id)

  def add_new_environment(self, env_name: Optional[str]):
    env = Environment(env_name)
    self.environments[env.name] = env
    return self.environments[env.name]

  def remove_environment(self, env_name: str):
    del self.environments[env_name]

  def add_new_collection(self, collection_name: Optional[str]):
    collection = Collection(collection_name)
    self.collections[collection.name] = collection
    return self.collections[collection.name]
  
  def remove_collection(self, env_name: str):
    del self.collections[env_name]


class CollectionsSection(TreeViewableItem):
  def get_item_options(self) -> tuple[str, Optional[tk.Image], bool]:
    return "Collections", None, True


class EnvironmentsSection(TreeViewableItem):
  def get_item_options(self) -> tuple[str, Optional[tk.Image], bool]:
    return "Environments", None, True
