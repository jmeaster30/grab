import tkinter as tk

from model.project import Project
from model.request import Request
from ui.layout_config import LayoutConfig
from ui.project_hierarchy import ProjectHierarchy
from ui.workarea import WorkArea

project = Project()
env1 = project.add_new_environment("My Sweet Environment")
env1["WOW"] = "heck yeah"
env1["dang"] = "uwu"
env2 = project.add_new_environment("Radical")
env2["aaaa"] = "1234"
env2["oooo"] = "87563"
collection = project.add_new_collection("Many REquests")
collection.add_request(Request("Get Token"))
collection.add_request(Request("Post Man"))

test_project = Project("AAAAA")
print(test_project.name)

class Grab(tk.Tk):
  def __init__(self):
    super().__init__()

    self.layout_config = LayoutConfig()

    self.title(self.layout_config.title)
    self.geometry(f'{self.layout_config.width}x{self.layout_config.height}')
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=2)

    self.project_hierarchy = ProjectHierarchy(self)
    self.project_hierarchy.grid(row=0, column=0, sticky=tk.NSEW)

    self.workarea = WorkArea(self)
    self.workarea.grid(row=0, column=1, sticky=tk.NSEW)

    self.project_hierarchy.on_environment_variable_click_action = self.workarea.open_environment
    project.refresh_project(self.project_hierarchy)
    
if __name__ == "__main__":
  app = Grab()
  app.mainloop()