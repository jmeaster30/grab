from util.goodsort import proper_string_sort_key

def get_new_name(type: str, existing_names: list[str]) -> str:
  base_name = f'New {type}'
  existing_new_type_names = [val for val in existing_names if val.startswith(base_name)]
  if len(existing_new_type_names) == 0:
    return base_name
  existing_new_type_names.sort(key=proper_string_sort_key(), reverse=True)
  suffix = existing_new_type_names[0].removeprefix(base_name).strip()
  if len(suffix) == 0:
    return f'{base_name} 1'
  return f'{base_name} {int(float(suffix)) + 1}'
