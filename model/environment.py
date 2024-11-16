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
    self.active = False
    self.name = 'New Environment' if env_name is None else env_name
    self.variables: list[EnvironmentVariable] = []

  def set_name(self, name: str):
    self.name = name
    if self.project_hierarchy.on_environment_name_change is not None:
      self.project_hierarchy.on_environment_name_change(self.tree_id, self.name)

  def add_or_update_environment_variable(self, idx: Optional[int], values: list[str]):
    if idx is None:
      # adding a new environment variable
      newvar = EnvironmentVariable(self, values[0], values[1])
      newvar.set_hierarchy(self.project_hierarchy)
      self.variables.append(newvar)
      return
    
    if idx < 0 or idx >= len(self.variables):
      raise IndexError
    
    envvar = self.variables[idx]
    envvar.name = values[0]
    envvar.value = values[1]

  def remove_environment_variable(self, idx: int):
    self.variables.pop(idx)

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
    super().refresh()
    for variable in self.variables:
      variable.refresh()
    # need to go through and remove the rows from the treeview that are not there any more
    remaining_tree_ids = [str(var.tree_id) for var in self.variables]
    for child_id in self.project_hierarchy.tree.get_children(self.tree_id):
      if str(child_id) not in remaining_tree_ids:
        self.project_hierarchy.tree.delete(child_id)
