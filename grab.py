#!/usr/bin/env python3

import argparse
import sys
import tkinter as tk
import tkinter.messagebox as tkmb
from tkinter import ttk

from lilytk.events import ClassListens

from logic.request_engine import RequestEngine
from model.project import Project
from ui.control_bar import ControlBar
from ui.layout_config import LayoutConfig
from ui.project_hierarchy import ProjectHierarchy
from ui.workarea import WorkArea
from util.ui_error_handler import UIErrorHandler

@ClassListens('Project.NameUpdated', 'update_title')
@ClassListens('Project.Modified', 'update_title')
class Grab(tk.Tk):
  def __init__(self):
    super().__init__()

    self.update_title(Project().name)
    self.geometry(LayoutConfig().window.size())
    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)

    self.engine = RequestEngine()

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

    self.bind('<Control-s>', lambda event: self.control_bar.save_command())
    self.protocol("WM_DELETE_WINDOW", self.on_close)

  def update_title(self, data):
    self.title(f"{LayoutConfig().window.title} - {Project().name} {'*' if Project().modified else ''}")

  @UIErrorHandler('On Close Error', 'Oof there was an error when closing the window :(')
  def on_close(self):
    if Project().modified:
      selected_option = tkmb.askyesnocancel('You have unsaved changes!', 'Would you like to save before closing?')
      if selected_option is None:
        return
      
      if selected_option:
        self.control_bar.save_command()
    
    self.destroy()

if __name__ == "__main__":
  argparser = argparse.ArgumentParser(prog='grab', description='graphical rest api badgerer')
  argparser.add_argument('project', nargs='?', default='.', help='Project file to open')
  args = argparser.parse_args(sys.argv[1:])

  app = Grab()
  if args.project != '.':
    Project().open(args.project)

  app.mainloop()
