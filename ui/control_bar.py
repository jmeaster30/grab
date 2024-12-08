import tkinter as tk
import tkinter.messagebox as tkmb
import tkinter.filedialog as tkfd
from typing import Optional

from lilytk.events import ClassListens, Notifies

from model.environment import Environment
from model.project import Project
from ui.dropdown_select import DropDownSelect
from util.ui_error_handler import UIErrorHandler

@ClassListens('Environment.NameUpdated', 'on_environments_change')
@ClassListens('Environment.Add', 'on_environments_change')
@ClassListens('Environment.Remove', 'on_environments_change')
@ClassListens('Environment.SetActive', 'update_environment_active')
@ClassListens('Project.Modified', 'update_buttons')
class ControlBar(tk.Frame):
  def __init__(self, root, environments: list[Environment]):
    super().__init__(root)

    self.new_project_button_text_variable = tk.StringVar(value='New Project')
    self.new_project_button = tk.Button(self, textvariable=self.new_project_button_text_variable, command=self.new_command)
    self.new_project_button.pack(side=tk.LEFT)

    self.open_project_button_text_variable = tk.StringVar(value='Open Project')
    self.open_project_button = tk.Button(self, textvariable=self.open_project_button_text_variable, command=self.open_command)
    self.open_project_button.pack(side=tk.LEFT)

    self.save_project_button_text_variable = tk.StringVar(value='Save Project')
    self.save_project_button = tk.Button(self, textvariable=self.save_project_button_text_variable, command=self.save_command)
    self.save_project_button.pack(side=tk.LEFT)
    self.update_buttons(False)

    self.environment_select = DropDownSelect(self, values=environments, 
                                            label_selector=lambda environment: environment.name, 
                                            on_selection_change=self.on_active_environment_change,
                                            placeholder='<No Environment>')
    self.environment_select.pack(side=tk.RIGHT)

  def update_buttons(self, data):
    self.new_project_button_text_variable.set(f'New Project{" [!]" if data else ""}')
    self.open_project_button_text_variable.set(f'Open Project{" [!]" if data else ""}')
    self.save_project_button.config(state='normal' if data else 'disabled')

  def new_command(self):
    if Project().modified:
      selected_option = tkmb.askyesnocancel('Unsaved Changes', f"Project '{Project().name}' has unsaved changes. Would you like to save before creating a new project?")
      if selected_option is None:
        return
      if selected_option:
        self.save_command()
    Project().clear()

  @UIErrorHandler('File Open Error', 'There was an error when opening the project (>⌓<｡)\nCheck console for exception )\'')
  def open_command(self):
    if Project().modified:
      selected_option = tkmb.askyesnocancel('Unsaved Changes', f"Project '{Project().name}' has unsaved changes. Would you like to save before creating a new project?")
      if selected_option is None:
        return
      if selected_option:
        self.save_command()
    
    selected_filename = tkfd.askopenfilename(initialdir='~', title="Open File")
    if selected_filename is None or selected_filename == ():
      return
    
    Project().clear()
    Project().open(selected_filename)

  @UIErrorHandler('File Save Error', 'There was an error when saving the project (ￗ﹏ￗ )\nCheck console for errors Dx')
  def save_command(self):
    selected_filename = Project().filename
    if selected_filename is None:
      selected_filename = tkfd.asksaveasfilename(confirmoverwrite=True, initialdir='~', initialfile='the_greatest_api_ever.grab', title="Save File")

    if selected_filename is None:
      return

    Project().save(selected_filename)

  def on_environments_change(self, data):
    self.environment_select.set_options(Project().environments.values())

  def update_environment_active(self, data):
    (env_id, is_active) = data
    environment = Project().environments[env_id]
    selected_env = self.environment_select.selected()
    if is_active and (selected_env is None or selected_env.id != env_id):
      self.environment_select.select(environment)
    elif selected_env is not None and selected_env.id == env_id:
      self.environment_select.deselect()

  @Notifies('ControlBar.ActiveEnvironmentSet')
  def on_active_environment_change(self, selected_environment: Optional[Environment]):
    if selected_environment is not None and selected_environment.active:
      return selected_environment
    for environment in Project().environments.values():
      environment.set_active(False)
    if selected_environment is not None:
      selected_environment.set_active(True)
    return selected_environment