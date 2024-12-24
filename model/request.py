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
    return self.name

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
    self.headers: list[tuple[str, str]] = []
    self.parameters: list[tuple[str, str]] = []
    self.cookies: list[tuple[str, str]] = []
    self.body: str = ''

  @Notifies('Project.HasChanges')
  @Notifies('Request.NameUpdated')
  def set_name(self, name: str):
    if self.name == name:
      return False
    self.name = name
    return self.id, self.name
  
  @Notifies('Project.HasChanges')
  def add_update_header(self, idx: Optional[int], name: str, value: str):
    if idx == len(self.headers) or idx is None:
      self.headers.append((name, value))
    else:
      if self.headers[idx] == (name, value):
        return False
      self.headers[idx] = (name, value)
    return True

  @Notifies('Project.HasChanges')
  def set_headers(self, headers: list[tuple[str, str]]):
    if self.headers == headers:
      return False
    self.headers = headers
    return True

  @Notifies('Project.HasChanges')
  def add_update_parameters(self, idx: Optional[int], name: str, value: str):
    if idx == len(self.parameters) or idx is None:
      self.parameters.append((name, value))
    else:
      if self.parameters[idx] == (name, value):
        return False
      self.parameters[idx] = (name, value)
    return True

  @Notifies('Project.HasChanges')
  def set_parameters(self, parameters: list[tuple[str, str]]):
    if self.parameters == parameters:
      return False
    self.parameters = parameters
    return True

  @Notifies('Project.HasChanges')
  def add_update_cookies(self, idx: Optional[int], name: str, value: str):
    if idx == len(self.cookies) or idx is None:
      self.cookies.append((name, value))
    else:
      if self.cookies[idx] == (name, value):
        return False
      self.cookies[idx] = (name, value)
    return True

  @Notifies('Project.HasChanges')
  def set_cookies(self, cookies: list[tuple[str, str]]):
    if self.cookies == cookies:
      return False
    self.cookies = cookies
    return True

  @Notifies('Project.HasChanges')
  def set_body(self, text: str):
    if self.body == text:
      return False
    self.body = text
    return True
