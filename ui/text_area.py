import tkinter as tk
from typing import Callable, Optional

class TextArea(tk.Text):
  def __init__(self, root, *args, initial_value: str = '', debounce_ms: float = 0.0, on_text_updated: Optional[Callable[[tk.Event, str], None]] = None,  **kwargs):
    super().__init__(root, *args, **kwargs)
    self.insert(tk.END, initial_value)
    self.debounce_ms = debounce_ms
    self.on_text_updated = on_text_updated
    self.bind('<KeyRelease>', self._internal_text_update if debounce_ms == 0.0 else self._internal_debounce_text_update)
    self._internal_timer = None

  def _internal_debounce_text_update(self, event):
    if self._internal_timer is not None:
      self.after_cancel(self._internal_timer)
      self._internal_timer = None
    
    self._internal_timer = self.after(self.debounce_ms, self._internal_text_update, event)

  def _internal_text_update(self, event):
    if self._internal_timer is not None:
      self._internal_timer = None
    if self.on_text_updated is not None:
      print(f"HERE >>> [{self.get('1.0', tk.END)}]")
      self.on_text_updated(event, self.get("1.0", tk.END))