from datetime import timedelta


class Response:
  def __init__(self, status_code: int = 0, reason: str = '',
              url: str = '', 
              elapsed: timedelta = timedelta(),
              headers: dict[str, str] = {},
              body: str = ""):
    self.status_code = status_code
    self.reason = reason
    self.url = url
    self.elapsed = elapsed
    self.headers = headers
    self.body = body