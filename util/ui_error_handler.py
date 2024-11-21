import tkinter.messagebox as tkmb
import traceback

def UIErrorHandler(title: str, message: str):
  def UIErrorHandlerDecorator(func):
    def wrapper(*args, **kwargs):
      try:
        return func(*args, *kwargs)
      except Exception:
        traceback.print_exc()
        tkmb.showerror(title=title, message=message)
    return wrapper
  return UIErrorHandlerDecorator
