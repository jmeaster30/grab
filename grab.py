import tkinter as tk

from model.project import Project
from ui.grab_tree_viewer import GrabTreeViewer

project = Project()
env1 = project.add_new_environment("My Sweet Environment")
env1["WOW"] = "heck yeah"
env1["dang"] = "uwu"
env2 = project.add_new_environment("Radical")
env2["aaaa"] = "1234"
env2["oooo"] = "87563"

class Grab(tk.Tk):
  def __init__(self):
    super().__init__()

    self.title('grab')
    self.geometry('400x200')
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    self.my_tree_viewer = GrabTreeViewer(self)
    project.refresh_project(self.my_tree_viewer)


if __name__ == "__main__":
  app = Grab()
  app.mainloop()