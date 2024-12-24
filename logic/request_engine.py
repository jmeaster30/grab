from datetime import timedelta
from http.cookiejar import Cookie, CookieJar
import re
from typing import Optional
from urllib.parse import urlparse
import requests

from lilytk.events import ClassListens, Notifies
from lilytk.utils import Singleton

from logic.response import Response
from model.environment import Environment
from model.request import Request

@Singleton
@ClassListens('ControlBar.ActiveEnvironmentSet', 'set_active_environment')
class RequestEngine:
  def __init__(self):
    self.active_environment: Optional[Environment] = None
  
  def set_active_environment(self, data):
    self.active_environment = data

  @Notifies('Response.Received')
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
    print(f'[{body}]')
    if len(body) == 0:
      body = None

    cookies = CookieJar()
    request_domain = urlparse(url).netloc
    for cookie in request.cookies:
      cookie_name = self.resolve_environment_variable(cookie[0])
      cookie_value = self.resolve_environment_variable(cookie[1])
      cookies.set_cookie(Cookie(0, cookie_name, cookie_value, None, False, '', False, False, '', False, False, None, False, None, None, {}))

    try:
      response_data = requests.request(method=request.method.name, 
                                  url=url, 
                                  headers=headers,
                                  cookies=cookies,
                                  params=parameters,
                                  data=body)
      print('= REQUEST ==========================')
      print(vars(response_data.request))
      print('= RESPONSE =========================')
      print(vars(response_data))
      print('====================================')

      response = Response(
        status_code=response_data.status_code,
        reason=response_data.reason,
        url=response_data.url, 
        elapsed=response_data.elapsed,
        headers=response_data.headers,
        cookies=response_data.cookies.get_dict(),
        body=response_data.content)
    except Exception as ex:
      print(ex)
      response = Response(body=ex.__str__())

    return (request.id, response)

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
