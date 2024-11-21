import tkinter as tk
from typing import Optional

from model.project_item import ProjectItem
from ui.tree_viewable_item import TreeViewableItem
from ui.view.environment.environment_variable_tree_item import EnvironmentVariableTreeItem

from lilytk.events import ClassListens

@ClassListens('Environment.NameUpdated', 'update_name')
class EnvironmentTreeItem(TreeViewableItem):
  def __init__(self, parent: TreeViewableItem, project_hierarchy, environment_name: str, environment_id: str):
    super().__init__(parent, project_hierarchy, environment_id, ProjectItem.Environment)
    self.environment_id: str = environment_id
    self.environment_name: str = environment_name
    self.variables: list[EnvironmentVariableTreeItem] = []

  def update_name(self, data):
    (env_id, name) = data
    if env_id == self.environment_id:
      self.environment_name = name
      self.refresh()

  def get_item_options(self) -> tuple[str, Optional[tk.Image]]:
    return self.environment_name, None

  def refresh(self):
    super().refresh()
    for variable in self.variables:
      variable.refresh()
    # need to go through and remove the rows from the treeview that are not there any more
    remaining_tree_ids = [str(var.tree_id) for var in self.variables]
    for child_id in self.project_hierarchy.tree.get_children(self.tree_id):
      if str(child_id) not in remaining_tree_ids:
        self.project_hierarchy.tree.delete(child_id)