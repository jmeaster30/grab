import tkinter as tk

from lilytk.events import ClassListens

from model.request import Request, RequestMethod
from ui.dropdown_select import DropDownSelect

@ClassListens('Request.NameUpdated', 'pull_name')
class RequestEditArea(tk.Frame):
  def __init__(self, root: tk.Misc, request: Request):
    super().__init__(root)
    self.request: Request = request

    self.columnconfigure(1, weight=1)

    self.request_name_var = tk.StringVar(value=self.request.name)
    self.request_name_entry = tk.Entry(self, textvariable=self.request_name_var)
    self.request_name_entry.grid(row=0, column=0, columnspan=2, sticky=tk.EW)
    self.request_name_entry.bind('<KeyRelease>', self.on_request_name_change)

    self.request_method = DropDownSelect(self, values=RequestMethod.get_all(),
                                        label_selector=(lambda method: method.name),
                                        on_selection_change=self.on_method_change,
                                        default_selected=request.method, width=10)
    self.request_method.grid(row=1, column=0, sticky=tk.EW)
    self.request_method.bind('<<ComboboxSelected>>', self.on_method_change)

    self.url_var = tk.StringVar(value=self.request.url)
    self.url_entry = tk.Entry(self, textvariable=self.url_var)
    self.url_entry.grid(row=1, column=1, sticky=tk.EW)
    self.url_entry.bind('<KeyRelease>', self.on_url_change)


  def on_request_name_change(self, event):
    self.request.set_name(self.request_name_var.get())

  def pull_name(self, data):
    self.request_name_var.set(self.request.name)

  def on_method_change(self, event):
    self.request.method = self.request_method.selected()

  def on_url_change(self, event):
    self.request.url = self.url_var.get()


