import tkinter as tk
from tkinter import ttk
from typing import Optional

from model.environment import Environment, EnvironmentVariable
from ui.entry_table import EntryTable

class EnvironmentEditArea(tk.Frame):
  def __init__(self, root, environment: Environment, highlight_variable: Optional[EnvironmentVariable] = None):
    super().__init__(root)
    self.environment = environment
    self.highlighted_variable = highlight_variable

    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    self.variables_grid = EntryTable(self, columns=("Name", "Value"), initial_data=[(envvar.name, envvar.value) for envvar in self.environment.variables])
    self.variables_grid.grid(row=0, column=0, sticky=tk.NSEW)
    if highlight_variable is not None:
      self.set_highlight_variable(highlight_variable)

  def set_highlight_variable(self, environment_variable: Optional[EnvironmentVariable]):
    if self.highlighted_variable is not None:
      self.variables_grid.unhighlight_row((self.highlighted_variable.name, self.highlighted_variable.value))
    self.highlighted_variable = environment_variable
    if self.highlighted_variable is not None:
      self.variables_grid.highlight_row((environment_variable.name, environment_variable.value))
