import tkinter as tk
from typing import Optional
from uuid import uuid4

from lilytk.events import Notifies

from model.request import Request

class Collection:
  def __init__(self, collection_name: str = "New Collection", collection_id: Optional[str] = None):
    self.id: str = str(uuid4()) if collection_id is None else collection_id
    self.name: str = collection_name
    self.requests: list[Request] = []

  def add_request(self, request: Request):
    self.requests.append(request)

  @Notifies('Collection.NameUpdated')
  def set_name(self, name: str):
    self.name = name
    return self.id, self.name
