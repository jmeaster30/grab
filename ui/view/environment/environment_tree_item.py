import tkinter as tk
from typing import Optional

from model.project_item import ProjectItem
from ui.tree_viewable_item import TreeViewableItem
from ui.view.environment.environment_variable_tree_item import EnvironmentVariableTreeItem

from lilytk.events import ClassListens

@ClassListens('Environment.NameUpdated', 'update_name')
@ClassListens('Environment.VariableAddUpdate', 'add_variable')
@ClassListens('Environment.VariableRemove', 'remove_variable')
class EnvironmentTreeItem(TreeViewableItem):
  def __init__(self, parent: TreeViewableItem, project_hierarchy, environment_name: str, environment_id: str):
    super().__init__(parent, project_hierarchy, environment_id, ProjectItem.Environment)
    self.environment_id: str = environment_id
    self.environment_name: str = environment_name
    self.variables: dict[str, EnvironmentVariableTreeItem] = {}

  def update_name(self, data):
    (env_id, name) = data
    if env_id == self.environment_id:
      self.environment_name = name
      self.refresh()

  def get_item_options(self) -> tuple[str, Optional[tk.Image]]:
    return self.environment_name, None

  def add_variable(self, data):
    (env_id, added, variable) = data
    if env_id == self.environment_id and added:
      tree_item = EnvironmentVariableTreeItem(self, self.project_hierarchy, variable.name, variable.id)
      tree_item.tree_id = self.project_hierarchy.add_item(tree_item)
      self.variables[tree_item.object_id] = tree_item
      self.refresh()

  def remove_variable(self, data):
    if data.id in self.variables:
      self.variables.pop(data.id)
      self.refresh()

  def refresh(self):
    super().refresh()
    for _, variable in self.variables.items():
      variable.refresh()
    # need to go through and remove the rows from the treeview that are not there any more
    remaining_tree_ids = [str(var.tree_id) for _, var in self.variables.items()]
    for child_id in self.project_hierarchy.tree.get_children(self.tree_id):
      if str(child_id) not in remaining_tree_ids:
        self.project_hierarchy.tree.delete(child_id)