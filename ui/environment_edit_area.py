import tkinter as tk
from typing import Optional

from lilytk.events import ClassListens

from model.environment import Environment, EnvironmentVariable
from ui.entry_table import EntryTable
from ui.left_right_buttons import LeftRightButtons
from util.getnewname import get_new_name
@ClassListens('Environment.NameUpdated', 'pull_name')
class EnvironmentEditArea(tk.Frame):
  def __init__(self, root, environment: Environment):
    super().__init__(root)
    self.environment = environment
    self.highlighted_variable = None
    self.selected_rows: list[int] = []

    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)

    self.environment_name_var = tk.StringVar(value=self.environment.name)
    self.environment_name_entry = tk.Entry(self, textvariable=self.environment_name_var)
    self.environment_name_entry.grid(row=0, column=0, sticky=tk.EW)
    self.environment_name_entry.bind('<KeyRelease>', self.on_name_change)

    self.variables_grid = EntryTable(self, columns=("Name", "Value"), initial_data=[(envvar.name, envvar.value) for envvar in self.environment.variables])
    self.variables_grid.grid(row=1, column=0, sticky=tk.NSEW)

    self.variables_grid.set_select_change_action(self.on_row_select)
    self.variables_grid.set_row_change_action(self.on_row_change)
    self.variables_grid.set_row_add_action(self.on_row_add)
    self.variables_grid.set_row_remove_action(self.on_row_remove)

    self.buttons = LeftRightButtons(self, "+ Add", "- Remove")
    self.buttons.grid(row=2, column=0, sticky=tk.EW)
    self.buttons.set_right_button_clickable(False)
    self.buttons.left_button_action = self.add_env_variable
    self.buttons.right_button_action = self.remove_env_variable

  def on_row_select(self, rowid: int, values: list[str]):
    if rowid in self.selected_rows:
      self.selected_rows.pop(self.selected_rows.index(rowid))
    else:
      self.selected_rows.append(rowid)
    self.buttons.set_right_button_clickable(len(self.selected_rows) != 0)

  def on_row_add(self, idx: int, values: list[str]):
    self.environment.add_or_update_environment_variable(None, values)
    self.environment.refresh()

  def on_row_remove(self, idx: int, values: list[str]):
    self.environment.remove_environment_variable(idx)
    self.environment.refresh()

  def on_row_change(self, rowidx: int, colidx: int, values: list[str]):
    self.environment.add_or_update_environment_variable(rowidx, values)

  def on_name_change(self, event: tk.Event):
    self.environment.set_name(self.environment_name_var.get())

  def pull_name(self, data):
    self.environment_name_var.set(self.environment.name)

  def add_env_variable(self):
    new_name = get_new_name('New Env Var', [env_var.name for env_var in self.environment.variables])
    self.variables_grid.append_row((new_name, ""))

  def remove_env_variable(self):
    self.variables_grid.remove_rows(self.selected_rows)
    self.selected_rows = []
    self.buttons.set_right_button_clickable(False)

  def set_highlight_variable(self, environment_variable: Optional[EnvironmentVariable]):
    if self.highlighted_variable is not None:
      self.variables_grid.unhighlight_row((self.highlighted_variable.name, self.highlighted_variable.value))
    self.highlighted_variable = environment_variable
    if self.highlighted_variable is not None:
      self.variables_grid.highlight_row((environment_variable.name, environment_variable.value))
