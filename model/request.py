import tkinter as tk
from enum import Enum
from ui.tree_viewable_item import TreeViewableItem

class RequestMethod(Enum):
  GET = 1
  HEAD = 2
  POST = 3
  PUT = 4
  DELETE = 5
  CONNECT = 6
  OPTIONS = 7
  TRACE = 8
  PATCH = 9

  @classmethod
  def get_all(cls) -> list['RequestMethod']:
    return [member for member in cls.__members__.values()]

  def get_icon(self: 'RequestMethod') -> tk.Image:
    #return tk.PhotoImage(file=f'ui/{self.__str__().lower()}.png')
    return None

  def get_abbr_name(self: 'RequestMethod') -> str:
    return str(self).upper().removeprefix('REQUESTMETHOD.')[:3]

class Request(TreeViewableItem):
  def __init__(self, parent: TreeViewableItem, method: RequestMethod = RequestMethod.GET, name: str = "", url: str = ""):
    super().__init__(parent)
    self.method: RequestMethod = method
    self.name: str = name
    self.url: str = url

  def get_item_options(self) -> tuple[str, tk.Image]:
    return self.name, self.method.get_icon()