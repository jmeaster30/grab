import tkinter as tk
from tkinter import ttk
from typing import Optional

from model.environment import Environment, EnvironmentVariable

class EnvironmentEditArea(tk.Frame):
  def __init__(self, root, environment: Environment, highlight_variable: Optional[EnvironmentVariable] = None):
    super().__init__(root)
    self.environment = environment
    self.highlight_variable = highlight_variable

    print("areas :3")
    print(environment)
    print(highlight_variable)

    self.label = ttk.Label(self, text=f'ENV: {environment.name}, HIGHLIGHT: {"NONE" if highlight_variable is None else highlight_variable.name}')
    self.label.pack()

  def set_highlight_variable(self, environment_variable: Optional[EnvironmentVariable]):
    self.highlight_variable = environment_variable
    self.label.config(text=f'ENV: {self.environment.name}, HIGHLIGHT: {"NONE" if self.highlight_variable is None else self.highlight_variable.name}')
