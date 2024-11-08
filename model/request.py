from ui.tree_viewable_item import TreeViewableItem

class Request(TreeViewableItem):
  def __init__(self, parent: TreeViewableItem, name=""):
    super().__init__(parent)
    self.name = name

  def get_item_options(self):
    return self.name, None