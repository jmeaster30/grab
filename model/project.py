from typing import Optional
from lxml import etree

from model.collection import Collection
from model.environment import Environment
from lilytk.utils import Singleton
from lilytk.events import Notifies, ClassListens

from model.request import Request, RequestMethod

@Singleton
@ClassListens('Project.HasChanges', 'set_modified')
class Project:  
  def __init__(self, name="Empty Project"):
    self.name = name
    self.environments: dict[str, Environment] = {}
    self.collections: dict[str, Collection] = {}

    self.modified = False
    self.filename: Optional[str] = None

  @Notifies('Project.Modified')
  def set_modified(self, value):
    match value:
      case bool():
        self.modified = value
      case _:
        self.modified = True
    return self.modified

  @Notifies("Project.HasChanges")
  @Notifies('Project.NameUpdated')
  def set_name(self, data: str):
    self.name = data
    return self.name

  @Notifies('Environment.Add')
  def add_new_environment(self, env_name: Optional[str]):
    env = Environment(env_name)
    self.environments[env.id] = env
    return env
  
  @Notifies('Environment.Add')
  def add_environment(self, env_id: str, env_name: str):
    env = Environment(env_name, env_id)
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
  
  @Notifies('Collection.Add')
  def add_collection(self, col_id: str, col_name: str, default_url: str, default_method: RequestMethod):
    col = Collection(col_name, col_id)
    col.default_url = default_url
    col.default_method = default_method
    self.collections[col.id] = col
    return col
  
  @Notifies('Collection.Remove')
  def remove_collection(self, collection_id: str):
    return self.collections.pop(collection_id)

  def clear(self):
    self.modified = False
    self.filename = None
    self.set_name('Empty Project')
    env_keys = [id for id in self.environments.keys()]
    for env_id in env_keys:
      self.remove_environment(env_id)
    col_keys = [id for id in self.collections.keys()]
    for col_id in col_keys:
      self.remove_collection(col_id)

  def save(self, filename: str):    
    self.filename = filename
    self.modified = False

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
        'default_method': str(collection.default_method).encode(),
        'default_url': collection.default_url,
        'id': collection.id
      })
      for request in collection.requests.values():
        request_node = etree.Element('Request', {
          'name': request.name,
          'method': str(request.method).encode(),
          'url': request.url,
          'id': request.id
        })

        for header_name, header_value in request.headers:
          header_node = etree.Element('Header', {
            'name': header_name,
            'value': header_value
          })
          request_node.append(header_node)
        
        for parameter_name, parameter_value in request.parameters:
          parameter_node = etree.Element('Parameter', {
            'name': parameter_name,
            'value': parameter_value
          })
          request_node.append(parameter_node)

        if len(request.body) > 0:
          body_node = etree.Element('Body')
          body_node.text = request.body
          request_node.append(body_node)
        
        col_node.append(request_node)
      collections_section_node.append(col_node)
    doc.append(collections_section_node)
    with open(filename, 'w+') as f:
      f.write(etree.tostring(doc, pretty_print=True, encoding='UTF-8').decode('UTF-8'))
    self.set_modified(False)

  def open(self, filename: str):
    self.filename = filename
    etree.parse(filename, etree.XMLParser(target=XMLProjectBuilder(), encoding='UTF-8'))

class XMLProjectBuilder:
  def __init__(self):
    self.environments: dict[str, Environment] = {}
    self.collections: dict[str, Collection] = {}

    self.builder_id_stack = []
    self.tag_stack: list[str] = []

  def start(self, tag, attrib):
    match (tag, self.tag_stack):
      case 'Project', []:
        name = attrib['name']
        Project().set_name(name)
        self.tag_stack.append(tag)
        self.builder_id_stack.append('')
      case 'Environments', ['Project']:
        self.tag_stack.append(tag)
        self.builder_id_stack.append('')
      case 'Collections', ['Project']:
        self.tag_stack.append(tag)
        self.builder_id_stack.append('')
      case 'Environment', [*head, 'Environments']:
        env_id = attrib['id']
        env_active = bool(attrib['active'])
        env_name = attrib['name']
        env = Project().add_environment(env_id, env_name)
        if env_active:
          env.set_active(env_active)
        self.builder_id_stack.append(env.id)
        self.tag_stack.append(tag)
      case 'EnvironmentVariable', [*head, 'Environment']:
        env_var_id = attrib['id']
        env_var_name = attrib['name']
        env_id = self.builder_id_stack[-1]
        (_, _, env_var) = Project().environments[env_id].add_environment_variable(env_var_name, env_var_id)
        self.builder_id_stack.append(env_var.id)
        self.tag_stack.append(tag)
      case 'Collection', [*head, 'Collections']:
        col_id = attrib['id']
        col_name = attrib['name']
        col_default_url = "" if attrib['default_url'] is None else attrib['default_url']
        col_default_method = RequestMethod.GET if attrib['default_method'] is None else RequestMethod.from_str(attrib['default_method'])
        col = Project().add_collection(col_id, col_name, col_default_url, col_default_method)
        self.builder_id_stack.append(col.id)
        self.tag_stack.append(tag)
      case 'Request', [*head, 'Collection']:
        col_id = self.builder_id_stack[-1]
        req_id = attrib['id']
        req_name = attrib['name']
        req_url = attrib['url']
        req_method = RequestMethod.from_str(attrib['method'])
        req = Request(req_method, req_name, req_url, req_id)
        Project().collections[col_id].add_request(req)
        self.builder_id_stack.append(req.id)
        self.tag_stack.append(tag)
      case 'Header', [*head, 'Request']:
        col_id = self.builder_id_stack[-2]
        req_id = self.builder_id_stack[-1]
        header_name = attrib['name']
        header_value = attrib['value']
        Project().collections[col_id].requests[req_id].add_update_header(None, header_name, header_value)
      case 'Parameter', [*head, 'Request']:
        col_id = self.builder_id_stack[-2]
        req_id = self.builder_id_stack[-1]
        parameter_name = attrib['name']
        parameter_value = attrib['value']
        Project().collections[col_id].requests[req_id].add_update_parameters(None, parameter_name, parameter_value)
      case 'Body', [*head, 'Request']:
        self.tag_stack.append(tag)
      case _:
        raise etree.ParserError(f'Unknown opening tag "{tag}" with top of tag stack "{self.tag_stack[-1] if len(self.tag_stack) > 0 else "EMPTY"}"')

  def end(self, tag):
    match (tag, self.tag_stack):
      case 'Project', ['Project']:
        Project().set_modified(False)
        self.tag_stack.pop()
        self.builder_id_stack.pop()
      case 'Environments', [*head, 'Environments']:
        self.builder_id_stack.pop()
        self.tag_stack.pop()
      case 'Collections', [*head, 'Collections']:
        self.builder_id_stack.pop()
        self.tag_stack.pop()
      case 'Environment', [*head, 'Environment']:
        self.builder_id_stack.pop()
        self.tag_stack.pop()
      case 'EnvironmentVariable', [*head, 'EnvironmentVariable']:
        self.builder_id_stack.pop()
        self.tag_stack.pop()
      case 'Collection', [*head, 'Collection']:
        self.builder_id_stack.pop()
        self.tag_stack.pop()
      case 'Request', [*head, 'Request']:
        self.builder_id_stack.pop()
        self.tag_stack.pop()
      case 'Header', [*head, 'Request']:
        pass
      case 'Parameter', [*head, 'Request']:
        pass
      case 'Body', [*head, 'Body']:
        self.tag_stack.pop()
      case _:
        raise etree.ParserError(f'Unknown ending tag "{tag}" with top of tag stack "{self.tag_stack[-1] if len(self.tag_stack) > 0 else "EMPTY"}"')

  def data(self, data):
    match self.tag_stack:
      case [*head, 'EnvironmentVariable']:
        env_var_id = self.builder_id_stack[-1]
        env_id = self.builder_id_stack[-2]
        env_var = Project().environments[env_id].get_variable_by_id(env_var_id)
        env_var.set_value(data)
      case [*head, 'Body']:
        col_id = self.builder_id_stack[-2]
        req_id = self.builder_id_stack[-1]
        Project().collections[col_id].requests[req_id].set_body(data)
      case [*head, 'Project'] | [*head, 'Collections'] | [*head, 'Environments'] | [*head, 'Collection'] | [*head, 'Environment'] | [*head, 'Request'] | [*head, 'Header'] | [*head, 'Parameter']:
        pass
      case _:
        raise etree.ParserError(f'Unexpected data "{data}" with top of tag stack "{self.tag_stack[-1] if len(self.tag_stack) > 0 else "EMPTY"}"')

  def comment(self, text):
    pass
  
  def close(self):
    pass

