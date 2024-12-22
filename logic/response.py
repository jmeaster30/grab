from datetime import timedelta


class Response:
  def __init__(self, status_code: int, url: str, elapsed: timedelta, body: str):
    self.status_code = status_code
    self.url = url
    self.elapsed = elapsed
    self.body = body