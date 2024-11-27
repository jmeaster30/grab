from typing import Optional
from uuid import uuid4

from lilytk.events import Notifies

class EnvironmentVariable:
  def __init__(self, key="New Env Var", value="", variable_id: Optional[str] = None):
    self.id = str(uuid4()) if variable_id is None else variable_id
    self.name = key
    self.value = value

  @Notifies("Project.HasChanges")
  @Notifies("EnvironmentVariable.NameUpdated")
  def set_name(self, name: str):
    self.name = name
    return self.id, self.name

  @Notifies("Project.HasChanges")
  @Notifies("EnvironmentVariable.ValueUpdated")
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

  @Notifies("Project.HasChanges")
  @Notifies('Environment.NameUpdated')
  def set_name(self, name: str):
    self.name = name
    return self.id, self.name
  
  @Notifies("Project.HasChanges")
  @Notifies('Environment.SetActive')
  def set_active(self, active: bool):
    self.active = active
    return self.id, self.active
  
  def get_variable_by_id(self, variable_id: str) -> Optional[EnvironmentVariable]:
    for variable in self.variables:
      if variable.id == variable_id:
        return variable
    return None
  
  @Notifies("Project.HasChanges")
  @Notifies('Environment.VariableAddUpdate')
  def add_environment_variable(self, name: str, variable_id: str):
    env_var = EnvironmentVariable(key=name, variable_id=variable_id)
    self.variables.append(env_var)
    return self.id, True, env_var

  @Notifies("Project.HasChanges")
  @Notifies('Environment.VariableAddUpdate')
  def add_or_update_environment_variable(self, idx: Optional[int], values: tuple[str, str]):
    (name, value) = values
    if idx is None:
      # adding a new environment variable
      newvar = EnvironmentVariable(name, value)
      self.variables.append(newvar)
      return self.id, True, newvar
    
    if idx < 0 or idx >= len(self.variables):
      raise IndexError
    
    envvar = self.variables[idx]
    envvar.set_name(name)
    envvar.set_value(value)
    return self.id, False, envvar

  @Notifies("Project.HasChanges")
  @Notifies('Environment.VariableRemove')
  def remove_environment_variable(self, idx: int):
    return self.variables.pop(idx)
  
  def get_variable(self, key: str) -> Optional[str]:
    for env_var in self.variables:
      if env_var.name == key:
        return env_var.value
    return None


  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id
