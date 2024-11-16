import tkinter as tk
from tkinter import ttk

from model.project import Project
from model.request import Request, RequestMethod
from ui.control_bar import ControlBar
from ui.layout_config import LayoutConfig
from ui.project_hierarchy import ProjectHierarchy
from ui.workarea import WorkArea

project = Project()
env1 = project.add_new_environment("My Sweet Environment")
env1["WOW"] = "heck yeah"
env1["dang"] = "uwu"
env1["dang1"] = "uwu"
env1["dang2"] = "uwu"
env1["dang3"] = "uwu"
env1["dang4"] = "uwu"
env1["dang5"] = "uwu"
env1["dang6"] = "uwu"
env1["dang7"] = "uwu"
env1["dang8"] = "uwu"
env1["dang9"] = "uwu"
env1["dang10"] = "uwu"
env1["dang11"] = "uwu"
env1["dang12"] = "uwu"
env1["dang13"] = "uwu"
env1["dang14"] = "uwu"
env1["dang15"] = "uwu"
env1["dang16"] = "uwu"
env1["dang17"] = "uwu"
env1["dang18"] = "uwu"
env1["dang19"] = "uwu"
env1["dang20"] = "uwu"
env1["dang21"] = "uwu"
env1["dang22"] = "uwu"
env1["dang23"] = "uwu"
env1["dang24"] = "uwu"
env1["dang25"] = "uwu"
env2 = project.add_new_environment("Radical")
env2["aaaa"] = "1234"
env2["oooo"] = "87563"
collection = project.add_new_collection("Many REquests")
collection.add_request(Request(collection, RequestMethod.GET, "Get Token"))
collection.add_request(Request(collection, RequestMethod.POST, "Post Man"))

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

    self.project_hierarchy.on_environment_variable_click_action = self.workarea.open_environment
    self.project_hierarchy.on_collection_click_action = self.workarea.open_collection
    self.project_hierarchy.on_request_click_action = self.workarea.open_request
    self.project_hierarchy.on_environment_add_remove_action = self.workarea.review_environment_tabs
    self.project_hierarchy.on_environment_name_change = self.workarea.update_tab_name
    self.project_hierarchy.on_collection_name_change = self.workarea.update_tab_name
    self.project_hierarchy.on_project_name_change_action = self.update_title
    Project().set_hierarchy(self.project_hierarchy)
    Project().refresh_project()

  def update_title(self, project_name: str):
    self.title(f"{LayoutConfig().window.title} - {project_name}")

if __name__ == "__main__":
  app = Grab()
  app.mainloop()