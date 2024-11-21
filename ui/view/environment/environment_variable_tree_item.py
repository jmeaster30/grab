import tkinter as tk
from typing import Optional
from model.project_item import ProjectItem
from ui.tree_viewable_item import TreeViewableItem


class EnvironmentVariableTreeItem(TreeViewableItem):
  def __init__(self, parent: TreeViewableItem, project_hierarchy, environment_variable_name: str, environment_variable_id: str):
    super().__init__(parent, project_hierarchy, environment_variable_id, ProjectItem.EnvironmentVariable)
    self.environment_variable_id = environment_variable_id
    self.environment_variable_name = environment_variable_name

  def get_item_options(self) -> tuple[str, Optional[tk.Image]]:
    return self.name, None