import tkinter as tk
import tkinter.messagebox as tkmb
import tkinter.filedialog as tkfd
import traceback
from typing import Optional

from lilytk.events import ClassListens

from model.environment import Environment
from model.project import Project
from ui.dropdown_select import DropDownSelect

@ClassListens('Environment.NameUpdated', 'on_environments_change')
@ClassListens('Environment.Add', 'on_environments_change')
@ClassListens('Environment.Remove', 'on_environments_change')
class ControlBar(tk.Frame):
  def __init__(self, root, environments: list[Environment]):
    super().__init__(root)

    self.new_project_button = tk.Button(self, text='New Project', command=self.new_command)
    self.new_project_button.pack(side=tk.LEFT)

    self.open_project_button = tk.Button(self, text='Open Project', command=self.open_command)
    self.open_project_button.pack(side=tk.LEFT)

    self.save_project_button = tk.Button(self, text='Save Project', command=self.save_command)
    self.save_project_button.pack(side=tk.LEFT)

    self.environment_select = DropDownSelect(self, values=environments, 
                                            label_selector=lambda environment: environment.name, 
                                            on_selection_change=self.on_active_environment_change,
                                            placeholder='<No Environment>')
    self.environment_select.pack(side=tk.RIGHT)

  def new_command(self):
    print('new')
    if Project().modified:
      selected_option = tkmb.askyesnocancel('Unsaved Changes', f"Project '{Project().name}' has unsaved changes. Would you like to save before creating a new project?")
      if selected_option is None:
        return
      if selected_option:
        self.save_command()
    Project().clear()

  def open_command(self):
    print('open')
    if Project().modified:
      selected_option = tkmb.askyesnocancel('Unsaved Changes', f"Project '{Project().name}' has unsaved changes. Would you like to save before creating a new project?")
      if selected_option is None:
        return
      if selected_option:
        self.save_command()
    
    selected_filename = tkfd.askopenfilename(initialdir='~', title="Open File")
    if selected_filename is None:
      tkmb.showerror(title='File Open Error', message='No file path to open project from :(')
      return
    
    try:
      Project().clear()
      Project().open(selected_filename)
    except Exception:
      traceback.print_exc()
      tkmb.showerror(title='File Open Error', message='There was an error when opening the project (>⌓<｡)\nCheck console for exception )\':')


  def save_command(self):
    print('save')
    selected_filename = Project().filename
    if selected_filename is None:
      selected_filename = tkfd.asksaveasfilename(confirmoverwrite=True, initialdir='~', initialfile='the_greatest_api_ever.grab', title="Save File")
    
    if selected_filename is None:
      tkmb.showerror(title='File Save Error', message='No file path to save project into :(')
      return
    
    try:
      Project().save(selected_filename)
    except Exception:
      traceback.print_exc()
      tkmb.showerror(title='File Save Error', message='There was an error when saving the project (ￗ﹏ￗ )\nCheck console for errors Dx')

  def on_environments_change(self, data):
    self.environment_select.set_options(Project().environments.values())

  def on_active_environment_change(self, selected_environment: Optional[Environment]):
    pass