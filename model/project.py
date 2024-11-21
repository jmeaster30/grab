from typing import Optional
from lxml import etree

from model.collection import Collection
from model.environment import Environment
from lilytk.utils import Singleton
from lilytk.events import Notifies

@Singleton
class Project:  
  def __init__(self, name="Empty Project"):
    self.name = name
    self.environments: dict[str, Environment] = {}
    self.collections: dict[str, Collection] = {}

    self.modified = False
    self.filename: Optional[str] = None

  @Notifies('Project.NameUpdated')
  def set_name(self, data):
    self.name = data
    return self.name

  @Notifies('Environment.Add')
  def add_new_environment(self, env_name: Optional[str]):
    env = Environment(env_name)
    self.environments[env.id] = env
    return env

  @Notifies('Environment.Remove')
  def remove_environment(self, environment_id: str):
    return self.environments.pop(environment_id)

  @Notifies('Collection.Add')
  def add_new_collection(self, collection_name: Optional[str]):
    collection = Collection(collection_name)
    self.collections[collection.id] = collection
    return collection
  
  @Notifies('Collection.Remove')
  def remove_collection(self, collection_id: str):
    return self.collections.pop(collection_id)

  def clear(self):
    self.modified = False
    self.filename = None
    self.set_name('Empty Project')
    for env_id in self.environments.keys():
      self.remove_environment(env_id)
    for col_id in self.collections.keys():
      self.remove_collection(col_id)

  def save(self, filename: str):    
    self.filename = filename

    doc = etree.Element('Project', {'name': self.name})
    environment_section_node = etree.Element('Environments')
    for _, environment in self.environments.items():
      env_node = etree.Element('Environment', {
        'name': environment.name, 
        'id': environment.id,
        'active': str(environment.active).encode()
        })
      for environment_variable in environment.variables:
        env_var_node = etree.Element('EnvironmentVariable', {
          'name': environment_variable.name,
          'id': environment_variable.id
        })
        env_var_node.text = environment_variable.value
        env_node.append(env_var_node)
      environment_section_node.append(env_node)
    doc.append(environment_section_node)
    
    collections_section_node = etree.Element('Collections')
    for _, collection in self.collections.items():
      col_node = etree.Element('Collection', {
        'name': collection.name,
        'id': collection.id
      })
      for request in collection.requests:
        request_node = etree.Element('Request', {
          'name': request.name,
          'method': str(request.method).encode(),
          'url': request.url,
          'id': request.id
        })
        col_node.append(request_node)
      collections_section_node.append(col_node)
    doc.append(collections_section_node)
    with open(filename, 'w+') as f:
      f.write(etree.tostring(doc, pretty_print=True, encoding='UTF-8').decode('UTF-8'))
  
  def open(self, filename: str):
    print(f"selected filename {filename} length {len(filename)}")
    raise NotImplementedError()

