import tkinter as tk
from tkinter import ttk

class LeftRightButtons(tk.Frame):
  def __init__(self, root, left_text: str, right_text: str):
    super().__init__(root)

    self.left_button_var = tk.StringVar(value=left_text)
    self.right_button_var = tk.StringVar(value=right_text)

    self.left_button = tk.Button(self, textvariable=self.left_button_var, command=self.on_left_button_clicked)
    self.right_button = tk.Button(self, textvariable=self.right_button_var, command=self.on_right_button_clicked)

    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)

    self.left_button.grid(row=0, column=0, sticky=tk.NSEW)
    self.right_button.grid(row=0, column=1, sticky=tk.NSEW)

    self.left_button_action = None
    self.right_button_action = None

  def update_left_button_text(self, left_text: str):
    self.left_button_var.set(left_text)

  def update_right_button_text(self, right_text: str):
    self.right_button_var.set(right_text)

  def set_left_button_clickable(self, is_clickable: bool):
    # TODO need better inclusive language
    self.left_button.config(state='normal' if is_clickable else 'disabled')

  def set_right_button_clickable(self, is_clickable: bool):
    # TODO need better inclusive language
    self.right_button.config(state='normal' if is_clickable else 'disabled')

  def on_left_button_clicked(self):
    print(f"left clicked {self.left_button_action}")
    if self.left_button_action is not None:
      self.left_button_action()

  def on_right_button_clicked(self):
    print(f"right clicked {self.right_button_action}")
    if self.right_button_action is not None:
      self.right_button_action()