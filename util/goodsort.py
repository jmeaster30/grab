import functools


def proper_string_sort(left: str, right: str) -> int:
  fixleft = left.lower()
  fixright = right.lower()
  if len(left) < len(right):
    return -1
  elif len(left) > len(right):
    return 1
  elif fixleft == fixright:
    return 0
  elif fixleft < fixright:
    return -1
  #elif fixleft > fixright:
  return 1  

def proper_string_sort_key():
  return functools.cmp_to_key(proper_string_sort)

