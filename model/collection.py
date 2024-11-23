import tkinter as tk
from typing import Optional
from uuid import uuid4

from lilytk.events import Notifies

from model.request import Request, RequestMethod

class Collection:
  def __init__(self, collection_name: str = "New Collection", collection_id: Optional[str] = None):
    self.id: str = str(uuid4()) if collection_id is None else collection_id
    self.name: str = collection_name
    self.default_url: str = ""
    self.default_method: RequestMethod = RequestMethod.GET
    self.requests: dict[str, Request] = {}

  @Notifies('Collection.AddRequest')
  def add_request(self, request: Request):
    self.requests[request.id] = request
    return self.id, request

  @Notifies('Collection.RemoveRequest')
  def remove_request(self, request_id: str):
    return self.id, self.requests.pop(request_id)

  @Notifies('Collection.NameUpdated')
  def set_name(self, name: str):
    self.name = name
    return self.id, self.name
