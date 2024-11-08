import tkinter as tk
from typing import Optional

from ui.tree_viewable_item import TreeViewableItem

class EnvironmentVariable(TreeViewableItem):
  def __init__(self, parent: TreeViewableItem, key="New Env Variable", value=""):
    super().__init__(parent)
    self.name = key
    self.value = value

  def get_item_options(self) -> tuple[str, Optional[tk.Image]]:
    return self.name, None

class Environment(TreeViewableItem):
  def __init__(self, parent: TreeViewableItem, env_name: Optional[str] = None):
    super().__init__(parent)
    self.name = 'New Environment' if env_name is None else env_name
    self.variables: list[EnvironmentVariable] = []

  def add_or_update_environment_variable(self, idx: Optional[int], values: list[str]):
    print(f"add or update environment variable {idx} {values}")

  def remove_environment_variable(self, idx: int):
    print(f"remove environment variable {idx}")

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
    envvar = EnvironmentVariable(self, key, value)
    envvar.project_hierarchy = self.project_hierarchy
    self.variables.append(envvar)

  def __delitem__(self, key: str):
    envvar = None
    for var in self.variables:
      if var.name == key:
        envvar = var
        break
    if envvar is None:
      raise KeyError
    self.variables.remove(envvar)

  def get_item_options(self) -> tuple[str, Optional[tk.Image]]:
    return self.name, None
  
  def set_hierarchy(self, hierarchy):
    super().set_hierarchy(hierarchy)
    for var in self.variables:
      var.set_hierarchy(hierarchy)

  def refresh(self):
    print(self)
    super().refresh(True)
    for variable in self.variables:
      variable.refresh()
