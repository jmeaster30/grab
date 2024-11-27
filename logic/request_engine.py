import re
from typing import Optional
import requests

from lilytk.events import ClassListens
from lilytk.utils import Singleton

from model.environment import Environment
from model.request import Request

@Singleton
@ClassListens('ControlBar.ActiveEnvironmentSet', 'set_active_environment')
class RequestEngine:
  def __init__(self):
    self.active_environment: Optional[Environment] = None
  
  def set_active_environment(self, data):
    self.active_environment = data

  def send_request(self, request: Request):
    url: str = self.resolve_environment_variable(request.url)
    
    headers: dict[str, str] = {}
    for header in request.headers:
      header_name = self.resolve_environment_variable(header[0])
      header_value = self.resolve_environment_variable(header[1])
      headers[header_name] = header_value
    if len(headers) == 0:
      headers = None
    
    parameters: dict[str, str] = {}
    for param in request.parameters:
      param_name = self.resolve_environment_variable(param[0])
      param_value = self.resolve_environment_variable(param[1])
      parameters[param_name] = param_value
    if len(parameters) == 0:
      parameters = None

    body: str = self.resolve_environment_variable(request.body)
    if len(body) == 0:
      body = None

    try:
      response = requests.request(method=request.method.name, 
                                  url=url, 
                                  headers=headers,
                                  params=parameters,
                                  json=body)
      print('= REQUEST ==========================')
      print(response.request)
      print('= RESPONSE =========================')
      print('URL:', response.url)
      print('STATUS:', response.status_code)
      print('ELAPSED:', response.elapsed)
      print('BODY:\n', response.text)
      print('====================================')
    except Exception as ex:
      print(ex)



  def resolve_environment_variable(self, value: str) -> str:
    splits = re.split(r'(\{\{(?:[^\}]|\}+[^\}])*?\}+\})', value)
    fixed_parts = []
    for part in splits:
      if part.startswith('{{') and part.endswith('}}'):
        if self.active_environment is None:
          fixed_parts.append('')
          continue
        value = self.active_environment.get_variable(part[2:-2])
        if value is None:
          fixed_parts.append('')
        else:
          fixed_parts.append(value)
      else:
        fixed_parts.append(part)
    return ''.join(fixed_parts)