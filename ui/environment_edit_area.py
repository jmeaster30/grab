import tkinter as tk
from tkinter import ttk
from typing import Optional

from model.environment import Environment, EnvironmentVariable
from ui.entry_table import EntryTable

class EnvironmentEditArea(tk.Frame):
  def __init__(self, root, environment: Environment, highlight_variable: Optional[EnvironmentVariable] = None):
    super().__init__(root)
    self.environment = environment
    self.highlight_variable = highlight_variable

    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    self.variables_grid = EntryTable(self, columns=("Name", "Value"), initial_data=[(envvar.name, envvar.value) for envvar in self.environment.variables])
    self.variables_grid.grid(row=0, column=0, sticky=tk.NSEW)

  def set_highlight_variable(self, environment_variable: Optional[EnvironmentVariable]):
    self.highlight_variable = environment_variable
    #self.label.config(text=f'ENV: {self.environment.name}, HIGHLIGHT: {"NONE" if self.highlight_variable is None else self.highlight_variable.name}')

