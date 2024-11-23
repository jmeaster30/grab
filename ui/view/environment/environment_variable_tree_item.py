import tkinter as tk
from typing import Optional

from lilytk.events import ClassListens

from model.project_item import ProjectItem
from ui.tree_viewable_item import TreeViewableItem

@ClassListens('EnvironmentVariable.NameUpdated', 'update_name')
class EnvironmentVariableTreeItem(TreeViewableItem):
  def __init__(self, parent: TreeViewableItem, project_hierarchy, environment_variable_name: str, environment_variable_id: str):
    super().__init__(parent, project_hierarchy, environment_variable_id, ProjectItem.EnvironmentVariable)
    self.environment_variable_id = environment_variable_id
    self.environment_variable_name = environment_variable_name

  def update_name(self, data):
    (env_var_id, name) = data
    if self.environment_variable_id == env_var_id:
      self.environment_variable_name = name
      self.refresh()

  def get_item_options(self) -> tuple[str, Optional[tk.Image]]:
    return self.environment_variable_name, None