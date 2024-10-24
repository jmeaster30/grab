from ui.layout_config import Colors, LayoutConfig


class Highlightable:
  def highlight(self):
    self.configure(background=LayoutConfig().highlight.color, borderwidth=LayoutConfig().highlight.width)

  def unhighlight(self):
    self.configure(background=Colors.BLACK, borderwidth=0)