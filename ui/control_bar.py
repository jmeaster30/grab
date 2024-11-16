import tkinter as tk
from typing import Callable, Optional

from model.environment import Environment
from ui.dropdown_select import DropDownSelect

class ControlBar(tk.Frame):
  def __init__(self, root, environments: list[Environment], on_environments_change: Optional[Callable[[list[Environment]], None]] = None):
    super().__init__(root)

    self.new_project_button = tk.Button(self, text='New Project')
    self.new_project_button.pack(side=tk.LEFT)

    self.open_project_button = tk.Button(self, text='Open Project')
    self.open_project_button.pack(side=tk.LEFT)

    self.save_project_button = tk.Button(self, text='Save Project')
    self.save_project_button.pack(side=tk.LEFT)

    self.environment_select = DropDownSelect(self, values=environments, 
                                            label_selector=lambda environment: environment.name, 
                                            on_selection_change=self.on_active_environment_change,
                                            placeholder='<No Environment>')
    self.environment_select.pack(side=tk.RIGHT)

  def on_active_environment_change(self, selected_environment):
    selected_environment.active = True