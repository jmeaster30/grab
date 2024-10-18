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
  def __init__(self, env_name: Optional[str] = None):
    super().__init__()
    self.name = 'New Environment' if env_name is None else env_name
    self.variables: list[EnvironmentVariable] = []

  def __getitem__(self, key: str) -> str:
    for var in self.variables:
      if var.name == key:
        return var.value
    raise KeyError
  
  def __setitem__(self, key: str, value: str):
    for var in self.variables:
      if var.name == key:
        var.value = value
        return
    self.variables.append(EnvironmentVariable(key, value))

  def __delitem__(self, key: str):
    envvar = None
    for var in self.variables:
      if var.name == key:
        envvar = var
        break
    if envvar is None:
      raise KeyError
    self.variables.remove(envvar)

  def get_item_options(self) -> tuple[str, Optional[tk.Image], bool]:
    return self.name, None, False
  
  # can't use typing info for hierarchy here :(
  def refresh(self, hierarchy, parent_id: Optional[int]):
    super().refresh(hierarchy, parent_id)
    for variable in self.variables:
      variable.refresh(hierarchy, self.tree_id)
