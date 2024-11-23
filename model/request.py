import tkinter as tk
from enum import Enum
from typing import Optional
from uuid import uuid4

from lilytk.events import Notifies

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
  
  @classmethod
  def from_str(cls, method: str) -> 'RequestMethod':
    return cls.__members__[method]

  def __str__(self: 'RequestMethod') -> str:
    self.name

  def get_icon(self: 'RequestMethod') -> tk.Image:
    #return tk.PhotoImage(file=f'ui/{self.__str__().lower()}.png')
    return None

  def get_abbr_name(self: 'RequestMethod') -> str:
    return str(self).upper().removeprefix('REQUESTMETHOD.')[:3]

class Request:
  def __init__(self, method: RequestMethod = RequestMethod.GET, name: str = "", url: str = "", request_id: Optional[str] = None):
    self.id: str = str(uuid4()) if request_id is None else request_id
    self.method: RequestMethod = method
    self.name: str = name
    self.url: str = url

  @Notifies('Request.NameUpdated')
  def set_name(self, name: str):
    self.name = name
    return self.id, self.name
