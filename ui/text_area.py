import json
import tkinter as tk
import traceback
from typing import Callable, Optional

from bs4 import BeautifulSoup

from ui.layout_config import LayoutConfig

def JSON_FORMATTER(**kwargs):
  def formatter(text):
    try:
      return json.dumps(json.loads(text), **kwargs)
    except:
      traceback.print_exc()
      return text
  return formatter

def HTML_FORMATTER(**kwargs):
  def formatter(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.prettify(**kwargs)
  return formatter

CONTENT_TYPE_TO_FORMATTER = {
  "application/json": JSON_FORMATTER(indent=2),
  "text/html": HTML_FORMATTER(),
  "text/plain": lambda x: x
}

class TextArea(tk.Frame):
  def __init__(self, root, *args, initial_value: str = '', debounce_ms: float = 0.0, on_text_updated: Optional[Callable[[tk.Event, str], None]] = None, text_formatter: Callable[[str], str] = lambda x: x, readonly: Optional[bool] = None, **kwargs):
    super().__init__(root, *args, **kwargs)

    self.debounce_ms = debounce_ms
    self.on_text_updated = on_text_updated
    self.text_formatter = text_formatter
    self._internal_timer = None

    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    self.text = tk.Text(self, tabs=LayoutConfig().text_tab)
    self.text.insert(tk.END, initial_value)
    if readonly is None or not readonly:
      self.text.bind('<KeyRelease>', self._internal_text_update if debounce_ms == 0.0 else self._internal_debounce_text_update)
    self.text.grid(row=0, column=0, sticky=tk.NSEW)

    self.vertical_scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
    self.vertical_scroll.grid(row=0, column=1, sticky=tk.NS)
    self.text.configure(yscrollcommand=self.vertical_scroll.set)

    self.horizontal_scroll = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.text.xview)
    self.horizontal_scroll.grid(row=1, column=0, sticky=tk.EW)
    self.text.configure(xscrollcommand=self.horizontal_scroll.set)

  def set_text(self, text: str):
    self.text.delete('1.0', tk.END)
    formatted = text
    if self.text_formatter is not None:
      formatted = self.text_formatter(text)
    self.text.insert('1.0', formatted)

  def set_formatter(self, formatter: Callable[[str], str]):
    self.text_formatter = formatter

  def _internal_debounce_text_update(self, event):
    if self._internal_timer is not None:
      self.after_cancel(self._internal_timer)
      self._internal_timer = None
    
    self._internal_timer = self.after(self.debounce_ms, self._internal_text_update, event)

  def _internal_text_update(self, event):
    if self._internal_timer is not None:
      self._internal_timer = None
    current_text = self.text.get("1.0", tk.END)
    if self.text_formatter is not None:
      formatted = self.text_formatter(current_text)
      if current_text == formatted:
        return
      if self.on_text_updated is not None:
        self.on_text_updated(event, formatted)
      self.text.replace("1.0", tk.END, formatted)
    elif self.on_text_updated is not None:
      self.on_text_updated(event, current_text)