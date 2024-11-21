import tkinter as tk
from typing import Optional
from uuid import uuid4, UUID

from lilytk.events import Notifies

class EnvironmentVariable:
  def __init__(self, key="New Env Variable", value="", variable_id: Optional[str] = None):
    self.id = str(uuid4()) if variable_id is None else variable_id
    self.name = key
    self.value = value

  @Notifies("EnvironmentVariable.NameUpdated")
  def set_name(self, name: str):
    self.name = name
    return self.id, self.name

  @Notifies("EnvironmentVariable.ValeUpdated")
  def set_value(self, value: str):
    self.value = value
    return self.id, self.value

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id

class Environment:
  def __init__(self, env_name: Optional[str] = None, env_id: Optional[str] = None):
    self.id: str = str(uuid4()) if env_id is None else env_id
    self.active: bool = False
    self.name: str = 'New Environment' if env_name is None else env_name
    self.variables: list[EnvironmentVariable] = []

  @Notifies('Environment.NameUpdated')
  def set_name(self, name: str):
    self.name = name
    return self.id, self.name

  @Notifies('Environment.VariableAddUpdate')
  def add_or_update_environment_variable(self, name: str, value: str, idx: Optional[int] = None):
    if idx is None:
      # adding a new environment variable
      newvar = EnvironmentVariable(self, name, value)
      self.variables.append(newvar)
      return True, newvar
    
    if idx < 0 or idx >= len(self.variables):
      raise IndexError
    
    envvar = self.variables[idx]
    envvar.name = name
    envvar.value = value
    return False, envvar

  @Notifies('Environment.VariableRemove')
  def remove_environment_variable(self, idx: int):
    return self.variables.pop(idx)

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id
