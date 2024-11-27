import tkinter as tk
from typing import Callable, Optional

from ui.layout_config import LayoutConfig

class TextArea(tk.Frame):
  def __init__(self, root, *args, initial_value: str = '', debounce_ms: float = 0.0, on_text_updated: Optional[Callable[[tk.Event, str], None]] = None, text_formatter: Optional[Callable[[str], str]] = None, **kwargs):
    super().__init__(root, *args, **kwargs)

    self.debounce_ms = debounce_ms
    self.on_text_updated = on_text_updated
    self.text_formatter = text_formatter
    self._internal_timer = None

    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    self.text = tk.Text(self, tabs=LayoutConfig().text_tab)
    self.text.insert(tk.END, initial_value)
    self.text.bind('<KeyRelease>', self._internal_text_update if debounce_ms == 0.0 else self._internal_debounce_text_update)
    self.text.grid(row=0, column=0, sticky=tk.NSEW)

    self.vertical_scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
    self.vertical_scroll.grid(row=0, column=1, sticky=tk.NS)
    self.text.configure(yscrollcommand=self.vertical_scroll.set)

    self.horizontal_scroll = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.text.xview)
    self.horizontal_scroll.grid(row=1, column=0, sticky=tk.EW)
    self.text.configure(xscrollcommand=self.horizontal_scroll.set)

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