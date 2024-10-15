
def Singleton(cls):
  instance = None
  def get_instance(*args, **kwargs):
    nonlocal instance
    if instance is None:
      print("INITIALIZE")
      instance = cls(*args, *kwargs)
    print("RETURN INSTANCE")
    return instance
  return get_instance
