import tkinter as tk
from typing import Optional

from ui.tree_viewable_item import TreeViewableItem

class EnvironmentVariable(TreeViewableItem):
  def __init__(self, key="New Env Variable", value=""):
    super().__init__()
    self.name = key
    self.value = value

  def get_item_options(self) -> tuple[str, Optional[tk.Image], bool]:
    return self.name, None, False
  
  # can't use typing info fro hierarchy here :(
  def refresh(self, hierarchy, parent_id: Optional[int]):
    if self.tree_id is None:
      self.tree_id = hierarchy.add_item(parent_id, self)

    text, img, is_open = self.get_item_options()
    hierarchy.tree.item(self.tree_id, option=None, text=text, open=is_open)


class Environment(TreeViewableItem):
  def __init__(self, env_name: str = "New Environment"):
    super().__init__()
    self.name = env_name
    self.variables: dict[str, EnvironmentVariable] = {}

  def __getitem__(self, key: str) -> str:
    envvar = self.variables.get(key)
    if envvar is None:
      raise KeyError
    return envvar.value
  
  def __setitem__(self, key: str, value: str):
    self.variables[key] = EnvironmentVariable(key, value)

  def __delitem__(self, key: str):
    original = self.variables.get(key)
    if original is None:
      raise KeyError
    del self.variables[key]

  def get_item_options(self) -> tuple[str, Optional[tk.Image], bool]:
    return self.name, None, False
  
  # can't use typing info for hierarchy here :(
  def refresh(self, hierarchy, parent_id: Optional[int]):
    super().refresh(hierarchy, parent_id)
    for _, variable in self.variables.items():
      variable.refresh(hierarchy, self.tree_id)
