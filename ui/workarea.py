import tkinter as tk
from tkinter import ttk
from typing import Optional

from model.environment import Environment, EnvironmentVariable
from model.request import Request
from ui.environment_edit_area import EnvironmentEditArea

# I got the CustomNotebook from https://stackoverflow.com/a/39459376

class WorkArea(tk.Frame):
  def __init__(self, root):
    super().__init__(root)
    self.notebook = ttk.Notebook(self, style="CustomNotebook")
    self.notebook.pack(expand=True, fill=tk.BOTH)

    self._active = None

    self.notebook.bind("<ButtonPress-1>", self.on_close_press, True)
    self.notebook.bind("<ButtonRelease-1>", self.on_close_release)

    self.environment_id_to_edit_area: dict[int, EnvironmentEditArea] = {}

  def is_child(self, editArea: EnvironmentEditArea) -> bool:
    return str(editArea) in self.notebook.tabs()

  def open_environment(self, environment: Environment, highlighted_variable: Optional[EnvironmentVariable] = None):
    tab_frame = None
    if environment.tree_id in self.environment_id_to_edit_area and self.is_child(self.environment_id_to_edit_area[environment.tree_id]):
      tab_frame = self.environment_id_to_edit_area[environment.tree_id]
    else:
      tab_frame = EnvironmentEditArea(self.notebook, environment)
      envname, _ = environment.get_item_options()
      self.notebook.add(tab_frame, state=tk.NORMAL, sticky=tk.NSEW, text=envname)
      self.environment_id_to_edit_area[environment.tree_id] = tab_frame
    self.notebook.select(tab_frame)
    # FIXME this is hack and sucks real bad
    self.after(100, self.set_initial_highlight(tab_frame, highlighted_variable))

  def set_initial_highlight(self, tab_frame, highlighted_variable):
    print("setting click highlight")
    def do_highlight():
      print(f"highlighed: {highlighted_variable}")
      tab_frame.set_highlight_variable(highlighted_variable)
    return do_highlight

  def review_environment_tabs(self, environments: list[Environment]):
    alive_tabs = [env.tree_id for env in environments]
    for editarea_id in self.environment_id_to_edit_area.keys():
      if editarea_id not in alive_tabs:
        self.notebook.forget(self.environment_id_to_edit_area[editarea_id])
        del self.environment_id_to_edit_area[editarea_id]

  def on_close_press(self, event):
    element = self.notebook.identify(event.x, event.y)

    if "close" in element:
      index = self.notebook.index(f'@{event.x},{event.y}')

      self.notebook.state(['pressed'])
      self._active = index
      return "break"

  def on_close_release(self, event):
    if not self.notebook.instate(['pressed']):
      return

    element = self.notebook.identify(event.x, event.y)
    if "close" not in element:
      return

    index = self.notebook.index(f'@{event.x},{event.y}')

    if self._active == index:
      self.notebook.forget(index)
      self.notebook.event_generate("<<NotebookTabClosed>>")

    self.notebook.state(["!pressed"])
    self._active = None
