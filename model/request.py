from ui.tree_viewable_item import TreeViewableItem

class Request(TreeViewableItem):
  def __init__(self, name=""):
    super().__init__()
    self.name = name

  def get_item_options(self):
    return self.name, None, False