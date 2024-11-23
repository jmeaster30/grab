import tkinter as tk
from tkinter import ttk

from lilytk.events import ClassListens

from model.project import Project
from ui.control_bar import ControlBar
from ui.layout_config import LayoutConfig
from ui.project_hierarchy import ProjectHierarchy
from ui.workarea import WorkArea

@ClassListens('Project.NameUpdated', 'update_title')
@ClassListens('Project.Modified', 'update_title')
class Grab(tk.Tk):
  def __init__(self):
    super().__init__()

    self.update_title(Project().name)
    self.geometry(LayoutConfig().window.size())
    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)

    self.control_bar = ControlBar(self, Project().environments)
    self.control_bar.grid(row=0, column=0, sticky=tk.NSEW)

    self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
    self.paned_window.grid(row=1, column=0, sticky=tk.NSEW)

    self.project_hierarchy = ProjectHierarchy(self.paned_window)
    self.project_hierarchy.pack(expand=True, fill=tk.BOTH)

    self.paned_window.add(self.project_hierarchy)

    self.workarea = WorkArea(self.paned_window)
    self.workarea.pack(expand=True, fill=tk.BOTH)
    self.paned_window.add(self.workarea)

  def update_title(self, data):
    self.title(f"{LayoutConfig().window.title} - {Project().name} {'*' if Project().modified else ''}")

if __name__ == "__main__":
  app = Grab()
  app.mainloop()