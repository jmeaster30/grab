import tkinter as tk
from tkinter import ttk
from typing import Callable

from lilytk.events import ClassListens
from lilytk.widgets import ScrollableFrame

from logic.request_engine import RequestEngine
from logic.response import Response
from model.request import Request, RequestMethod
from ui.dropdown_select import DropDownSelect
from ui.layout_config import Colors
from ui.text_area import CONTENT_TYPE_TO_FORMATTER, JSON_FORMATTER, TextArea

@ClassListens('Request.NameUpdated', 'pull_name')
class RequestEditArea(tk.Frame):
  def __init__(self, root: tk.Misc, request: Request):
    super().__init__(root)
    self.request: Request = request

    self.columnconfigure(1, weight=1)
    self.rowconfigure(3, weight=1)

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

    self.control_bar = tk.Frame(self)
    self.control_bar.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW)
    
    self.send_button = tk.Button(self.control_bar, text='Send!!', command=self.send_command)
    self.send_button.pack(fill=tk.X, side=tk.RIGHT)

    self.details = RequestDetails(self, self.request)
    self.details.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW)

  def send_command(self):
    RequestEngine().send_request(self.request)

  def on_request_name_change(self, event):
    self.request.set_name(self.request_name_var.get())

  def pull_name(self, data):
    self.request_name_var.set(self.request.name)

  def on_method_change(self, event):
    self.request.method = self.request_method.selected()

  def on_url_change(self, event):
    self.request.url = self.url_var.get()

class RequestDetails(tk.Frame):
  def __init__(self, root: tk.Misc, request: Request):
    super().__init__(root)
    self.notebook = ttk.Notebook(self)
    self.notebook.pack(expand=True, fill=tk.BOTH)

    self.header_frame = RequestHeaders(self.notebook, request)
    self.notebook.add(self.header_frame, state=tk.NORMAL, sticky=tk.NSEW, text='Headers')

    self.cookie_frame = RequestCookies(self.notebook, request)
    self.notebook.add(self.cookie_frame, state=tk.NORMAL, sticky=tk.NSEW, text='Cookies')

    self.parameter_frame = RequestParameters(self.notebook, request)
    self.notebook.add(self.parameter_frame, state=tk.NORMAL, sticky=tk.NSEW, text='Parameters')

    self.body_frame = RequestBody(self.notebook, request)
    self.notebook.add(self.body_frame, state=tk.NORMAL, sticky=tk.NSEW, text='Body')

    self.response_frame = RequestResponseView(self.notebook, request.id)
    self.notebook.add(self.response_frame, state=tk.NORMAL, sticky=tk.NSEW, text='Response')

class RequestHeaders(tk.Frame):
  def __init__(self, root: tk.Misc, request: Request):
    super().__init__(root)
    self.request = request
    self.selected_idxs: list[int] = []
    self.header_entry_rows: list[RequestDetailRow] = []

    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    self.table = ScrollableFrame(self, orient=tk.VERTICAL)
    self.table.grid(row=0, column=0, sticky=tk.NSEW)

    self.build_headers()

    for i in range(0, len(self.request.headers)):
      row = RequestDetailRow(self.table, self.request, i,
                            name_getter=(lambda req, idx: req.headers[idx][0]), name_setter=self.set_header_name,
                            value_getter=(lambda req, idx: req.headers[idx][1]), value_setter=self.set_header_value,
                            on_selected=self.on_selection)
      row.pack(fill=tk.X, expand=True)
      self.header_entry_rows.append(row)

    self.build_footer()

  def build_headers(self):
    headers_row = tk.Frame(self.table)
    headers_row.columnconfigure(1, weight=1)
    headers_row.columnconfigure(2, weight=1)
    selected = tk.BooleanVar(value=False)
    check_box = tk.Checkbutton(headers_row, variable=selected, offvalue=False, onvalue=True, command=lambda: None)
    check_box.grid(row=0, column=0, sticky=tk.EW)
    name_static_var = tk.StringVar(value='Name')
    name_static_entry = tk.Entry(headers_row, textvariable=name_static_var, state='readonly', relief='raised')
    name_static_entry.grid(row=0, column=1, sticky=tk.EW)
    value_static_var = tk.StringVar(value='Value')
    value_static_entry = tk.Entry(headers_row, textvariable=value_static_var, state='readonly', relief='raised')
    value_static_entry.grid(row=0, column=2, sticky=tk.EW)
    headers_row.pack(fill=tk.X, expand=True)

  def build_footer(self):
    self.footer = tk.Frame(self)
    self.footer.grid(row=1, column=0, sticky=tk.EW)
    self.footer.columnconfigure(0, weight=1)
    self.footer.columnconfigure(1, weight=1)

    self.add_header_button = tk.Button(self.footer, text='Add Header', command=self.add_header)
    self.add_header_button.grid(row=0, column=0, sticky=tk.EW)
    self.remove_header_button = tk.Button(self.footer, text='Remove Header(s)', command=self.remove_selected_headers)
    self.remove_header_button.grid(row=0, column=1, sticky=tk.EW)

  def add_header(self):
    idx = len(self.header_entry_rows)
    self.request.add_update_header(idx, '', '')
    header_row = RequestDetailRow(self.table, self.request, idx, 
                                  name_getter=(lambda req, idx: req.headers[idx][0]), name_setter=self.set_header_name,
                                  value_getter=(lambda req, idx: req.headers[idx][1]), value_setter=self.set_header_value,
                                  on_selected=self.on_selection)
    header_row.pack(fill=tk.X, expand=True)
    self.header_entry_rows.append(header_row)

  def on_selection(self, idx: int, header: tuple[str, str]):
    if idx in self.selected_idxs:
      self.selected_idxs.remove(idx)
    else:
      self.selected_idxs.append(idx)

  def set_header_name(self, req, idx, name):
    (_, value) = req.headers[idx]
    req.add_update_header(idx, name, value)

  def set_header_value(self, req, idx, value):
    (name, _) = req.headers[idx]
    req.add_update_header(idx, name, value)

  def remove_selected_headers(self):
    to_not_delete = []
    to_delete = []
    for idx in range(0, len(self.request.headers)):
      if idx in self.selected_idxs:
        to_delete.append(self.header_entry_rows[idx])
      else:
        to_not_delete.append(self.request.headers[idx])

    self.request.set_headers(to_not_delete)

    for row in to_delete:
      self.header_entry_rows.remove(row)
      row.forget()

    for idx in range(0, len(self.header_entry_rows)):
      self.header_entry_rows[idx].idx = idx
    
    self.selected_idxs = []

class RequestCookies(tk.Frame):
  def __init__(self, root: tk.Misc, request: Request):
    super().__init__(root)
    self.request = request
    self.selected_idxs: list[int] = []
    self.cookie_entry_rows: list[RequestDetailRow] = []

    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    self.table = ScrollableFrame(self, orient=tk.VERTICAL)
    self.table.grid(row=0, column=0, sticky=tk.NSEW)

    self.build_headers()

    for i in range(0, len(self.request.cookies)):
      row = RequestDetailRow(self.table, self.request, i,
                            name_getter=(lambda req, idx: req.cookies[idx][0]), name_setter=self.set_cookie_name,
                            value_getter=(lambda req, idx: req.cookies[idx][1]), value_setter=self.set_cookie_value,
                            on_selected=self.on_selection)
      row.pack(fill=tk.X, expand=True)
      self.cookie_entry_rows.append(row)

    self.build_footer()

  def build_headers(self):
    headers_row = tk.Frame(self.table)
    headers_row.columnconfigure(1, weight=1)
    headers_row.columnconfigure(2, weight=1)
    selected = tk.BooleanVar(value=False)
    check_box = tk.Checkbutton(headers_row, variable=selected, offvalue=False, onvalue=True, command=lambda: None)
    check_box.grid(row=0, column=0, sticky=tk.EW)
    name_static_var = tk.StringVar(value='Name')
    name_static_entry = tk.Entry(headers_row, textvariable=name_static_var, state='readonly', relief='raised')
    name_static_entry.grid(row=0, column=1, sticky=tk.EW)
    value_static_var = tk.StringVar(value='Value')
    value_static_entry = tk.Entry(headers_row, textvariable=value_static_var, state='readonly', relief='raised')
    value_static_entry.grid(row=0, column=2, sticky=tk.EW)
    headers_row.pack(fill=tk.X, expand=True)

  def build_footer(self):
    self.footer = tk.Frame(self)
    self.footer.grid(row=1, column=0, sticky=tk.EW)
    self.footer.columnconfigure(0, weight=1)
    self.footer.columnconfigure(1, weight=1)

    self.add_cookie_button = tk.Button(self.footer, text='Add Cookie', command=self.add_cookie)
    self.add_cookie_button.grid(row=0, column=0, sticky=tk.EW)
    self.remove_cookie_button = tk.Button(self.footer, text='Remove Cookie(s)', command=self.remove_selected_cookies)
    self.remove_cookie_button.grid(row=0, column=1, sticky=tk.EW)

  def add_cookie(self):
    idx = len(self.cookie_entry_rows)
    self.request.add_update_cookies(idx, '', '')
    cookie_row = RequestDetailRow(self.table, self.request, idx, 
                                  name_getter=(lambda req, idx: req.cookies[idx][0]), name_setter=self.set_cookie_name,
                                  value_getter=(lambda req, idx: req.cookies[idx][1]), value_setter=self.set_cookie_value,
                                  on_selected=self.on_selection)
    cookie_row.pack(fill=tk.X, expand=True)
    self.cookie_entry_rows.append(cookie_row)

  def on_selection(self, idx: int, cookie: tuple[str, str]):
    if idx in self.selected_idxs:
      self.selected_idxs.remove(idx)
    else:
      self.selected_idxs.append(idx)

  def set_cookie_name(self, req, idx, name):
    (_, value) = req.cookies[idx]
    req.add_update_cookies(idx, name, value)

  def set_cookie_value(self, req, idx, value):
    (name, _) = req.cookies[idx]
    req.add_update_cookies(idx, name, value)

  def remove_selected_cookies(self):
    to_not_delete = []
    to_delete = []
    for idx in range(0, len(self.request.cookies)):
      if idx in self.selected_idxs:
        to_delete.append(self.cookie_entry_rows[idx])
      else:
        to_not_delete.append(self.request.cookies[idx])

    self.request.set_cookies(to_not_delete)

    for row in to_delete:
      self.cookie_entry_rows.remove(row)
      row.forget()

    for idx in range(0, len(self.cookie_entry_rows)):
      self.cookie_entry_rows[idx].idx = idx
    
    self.selected_idxs = []

class RequestDetailRow(tk.Frame):
  def __init__(self, root: tk.Misc, request: Request, idx: int, 
              name_getter: Callable[[Request, int], str], name_setter: Callable[[Request, int, str], None],
              value_getter: Callable[[Request, int], str], value_setter: Callable[[Request, int, str], None],
              on_selected: Callable[[int, tuple[str, str]], None]):
    super().__init__(root)
    self.request = request
    self.idx = idx
    self.name_getter = name_getter
    self.name_setter = name_setter
    self.value_getter = value_getter
    self.value_setter = value_setter
    self.on_selected = on_selected

    self.columnconfigure(1, weight=1)
    self.columnconfigure(2, weight=1)

    self.selected = tk.BooleanVar(value=False)
    self.check_box = tk.Checkbutton(self, variable=self.selected, offvalue=False, onvalue=True, command=self.on_select_change)
    self.check_box.grid(row=0, column=0, sticky=tk.EW)

    self.name_var = tk.StringVar(value = self.name_getter(self.request, self.idx))
    self.name_entry = tk.Entry(self, textvariable=self.name_var)
    self.name_entry.grid(row=0, column=1, sticky=tk.EW)
    self.name_entry.bind('<KeyRelease>', self.set_name)

    self.value_var = tk.StringVar(value = self.value_getter(self.request, self.idx))
    self.value_entry = tk.Entry(self, textvariable=self.value_var)
    self.value_entry.grid(row=0, column=2, sticky=tk.EW)
    self.value_entry.bind('<KeyRelease>', self.set_value)

  def set_name(self, event):
    self.name_setter(self.request, self.idx, self.name_var.get())

  def set_value(self, event):
    self.value_setter(self.request, self.idx, self.value_var.get())

  def on_select_change(self):
    self.on_selected(self.idx, (self.name_getter(self.request, self.idx), self.value_getter(self.request, self.idx)))

class RequestParameters(tk.Frame):
  def __init__(self, root: tk.Misc, request: Request):
    super().__init__(root)
    self.request = request
    self.selected_idxs: list[int] = []
    self.parameter_entry_rows: list[RequestDetailRow] = []

    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    self.table = ScrollableFrame(self, orient=tk.VERTICAL)
    self.table.grid(row=0, column=0, sticky=tk.NSEW)

    self.build_headers()

    for i in range(0, len(self.request.parameters)):
      row = RequestDetailRow(self.table, self.request, i, 
                            name_getter=(lambda req, idx: req.parameters[idx][0]), name_setter=self.set_parameter_name,
                            value_getter=(lambda req, idx: req.parameters[idx][1]), value_setter=self.set_parameter_value,
                            on_selected=self.on_selection)
      row.pack(fill=tk.X, expand=True)
      self.parameter_entry_rows.append(row)

    self.build_footer()

  def build_headers(self):
    headers_row = tk.Frame(self.table)
    headers_row.columnconfigure(1, weight=1)
    headers_row.columnconfigure(2, weight=1)
    selected = tk.BooleanVar(value=False)
    check_box = tk.Checkbutton(headers_row, variable=selected, offvalue=False, onvalue=True, command=lambda: None)
    check_box.grid(row=0, column=0, sticky=tk.EW)
    name_static_var = tk.StringVar(value='Name')
    name_static_entry = tk.Entry(headers_row, textvariable=name_static_var, state='readonly', relief='raised')
    name_static_entry.grid(row=0, column=1, sticky=tk.EW)
    value_static_var = tk.StringVar(value='Value')
    value_static_entry = tk.Entry(headers_row, textvariable=value_static_var, state='readonly', relief='raised')
    value_static_entry.grid(row=0, column=2, sticky=tk.EW)
    headers_row.pack(fill=tk.X, expand=True)

  def build_footer(self):
    self.footer = tk.Frame(self)
    self.footer.grid(row=1, column=0, sticky=tk.EW)
    self.footer.columnconfigure(0, weight=1)
    self.footer.columnconfigure(1, weight=1)

    self.add_parameter_button = tk.Button(self.footer, text='Add Parameter', command=self.add_parameter)
    self.add_parameter_button.grid(row=0, column=0, sticky=tk.EW)
    self.remove_parameter_button = tk.Button(self.footer, text='Remove Parameter(s)', command=self.remove_selected_parameters)
    self.remove_parameter_button.grid(row=0, column=1, sticky=tk.EW)

  def add_parameter(self):
    idx = len(self.parameter_entry_rows)
    self.request.add_update_parameters(idx, '', '')
    parameter_row = RequestDetailRow(self.table, self.request, idx, 
                                  name_getter=(lambda req, idx: req.parameters[idx][0]), name_setter=self.set_parameter_name,
                                  value_getter=(lambda req, idx: req.parameters[idx][1]), value_setter=self.set_parameter_value,
                                  on_selected=self.on_selection)
    parameter_row.pack(fill=tk.X, expand=True)
    self.parameter_entry_rows.append(parameter_row)

  def on_selection(self, idx: int, parameter: tuple[str, str]):
    if idx in self.selected_idxs:
      self.selected_idxs.remove(idx)
    else:
      self.selected_idxs.append(idx)

  def set_parameter_name(self, req, idx, name):
    (_, value) = req.parameters[idx]
    req.add_update_parameters(idx, name, value)

  def set_parameter_value(self, req, idx, value):
    (name, _) = req.parameters[idx]
    req.add_update_parameters(idx, name, value)

  def remove_selected_parameters(self):
    to_not_delete = []
    to_delete = []
    for idx in range(0, len(self.request.parameters)):
      if idx in self.selected_idxs:
        to_delete.append(self.parameter_entry_rows[idx])
      else:
        to_not_delete.append(self.request.parameters[idx])

    self.request.set_parameters(to_not_delete)

    for row in to_delete:
      self.parameter_entry_rows.remove(row)
      row.forget()

    for idx in range(0, len(self.parameter_entry_rows)):
      self.parameter_entry_rows[idx].idx = idx
    
    self.selected_idxs = []


class RequestBody(tk.Frame):
  def __init__(self, root: tk.Misc, request: Request):
    super().__init__(root)
    self.request = request

    # TODO this should allow sending json, raw bytes, and files at least

    self.textarea = TextArea(self, initial_value=request.body, 
                              debounce_ms=300, 
                              on_text_updated=self.text_area_update,
                              text_formatter=JSON_FORMATTER(indent=2))
    self.textarea.pack(fill=tk.BOTH, expand=True)

  def text_area_update(self, event, text):
    print(f"[{text}]")
    self.request.set_body(text)


class StatusCodeLabel(tk.Frame):
  def __init__(self, root: tk.Misc, initial_code: int = 0, initial_reason: str = ""):
    super().__init__(root)

    self.label_var = tk.StringVar(value=f"Status: {initial_code} ({initial_reason})")
    self.label = tk.Label(self, textvariable=self.label_var)
    self.label.pack(fill=tk.BOTH, expand=True)
  
  def set_status(self, code: int, reason: str = ""):
    if reason == "":
      self.label_var.set(f"Status: {code}")
    else:
      self.label_var.set(f"Status: {code} ({reason})")


class ReadonlyNameValueRow(tk.Frame):
  def __init__(self, root: tk.Misc, name: str, value: str, header: bool = False):
    super().__init__(root)

    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)

    self.name_var = tk.StringVar(value=name)
    self.name = tk.Entry(self, textvariable=self.name_var)
    self.name.configure(state='readonly')
    if header:
      self.name.configure(relief='raised')
    else:
      self.name.configure(relief='sunken', background=Colors.WHITE) # TODO background doesn't work
    self.name.grid(row=0, column=0, sticky=tk.EW)

    self.value_var = tk.StringVar(value=value)
    self.value = tk.Entry(self, textvariable=self.value_var)
    self.value.configure(state='readonly')
    if header:
      self.value.configure(relief='raised')
    else:
      self.value.configure(relief='sunken', background=Colors.WHITE) # TODO background doesn't work
    self.value.grid(row=0, column=1, sticky=tk.EW)

class ReadonlyNameValueGrid(ScrollableFrame):
  def __init__(self, root: tk.Misc):
    super().__init__(root, orient=tk.VERTICAL)
    self.header = ReadonlyNameValueRow(self, name="Name", value="Value", header=True)
    self.header.pack(fill=tk.X, expand=True)
  
  def add_entry(self, name: str, value: str):
    entry = ReadonlyNameValueRow(self, name=name, value=value)
    entry.pack(fill=tk.X, expand=True)

  def clear(self):
    for child in self.winfo_children():
      if child != self.header:
        child.destroy()

@ClassListens('Response.Received', 'set_response')
class RequestResponseView(tk.Frame):
  def __init__(self, root: tk.Misc, request_id: str):
    super().__init__(root)
    self.request_id = request_id

    self.rowconfigure(2, weight=1)
    self.columnconfigure(1, weight=1)

    self.status_code = StatusCodeLabel(self)
    self.status_code.grid(row=0, column=0, sticky=tk.EW)

    self.elapsed_label_var = tk.StringVar(value="Elapsed: ")
    self.elapsed_label = tk.Label(self, textvariable=self.elapsed_label_var)
    self.elapsed_label.grid(row=0, column=1, sticky=tk.EW)

    self.url_var = tk.StringVar(value="URL: ")
    self.url = tk.Label(self, justify=tk.CENTER, textvariable=self.url_var)
    self.url.grid(row=1, column=0, columnspan=2, sticky=tk.EW)

    self.notebook = ttk.Notebook(self)
    self.notebook.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW)

    self.headers = ReadonlyNameValueGrid(self)
    # TODO add getter to the full container on ScrollableFrame
    self.notebook.add(self.headers.full_container, state=tk.NORMAL, text="Headers", sticky=tk.NSEW)

    self.cookies = ReadonlyNameValueGrid(self)
    self.notebook.add(self.cookies.full_container, state=tk.NORMAL, text="Cookies", sticky=tk.NSEW)

    self.body = TextArea(self, readonly=True)
    self.notebook.add(self.body, state=tk.NORMAL, text="Body", sticky=tk.NSEW)

  def set_response(self, data: tuple[str, Response]):
    (request_id, response) = data
    if self.request_id != request_id:
      return
    self.status_code.set_status(response.status_code, response.reason)
    self.url_var.set(f"URL: {response.url}")
    self.elapsed_label_var.set(f"Elapsed: {response.elapsed.total_seconds() * 1000} ms")

    content_type = response.headers['Content-Type'].split(';')[0] if 'Content-Type' in response.headers else 'text/plain' 
    self.body.set_formatter(CONTENT_TYPE_TO_FORMATTER[content_type])
    self.body.set_text(response.body)

    self.headers.clear()
    for name, value in response.headers.items():
      self.headers.add_entry(name, value)

    self.cookies.clear()
    for name, value in response.cookies.items():
      self.cookies.add_entry(name, value)

