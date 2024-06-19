from .style import StyledJSONNode, StyledJSONNodeFactory
from ..node import *
from ..icon import IconFamily

class RenderVisitor(JSONVisitor):
    def __init__(self, grid_width, fl_visitor, icon_family):
        self.grid_width = grid_width
        self.fl_visitor = fl_visitor
        self.icon_family = icon_family

    def visit_composite(self, composite: JSONComposite):
        self.render_node(composite)

    def visit_leaf(self, leaf: JSONLeaf):
        self.render_node(leaf)

    def render_node(self, node: JSONNode):
        if node.is_root():
            return
        result = ''
        # first layer
        if self.fl_visitor.is_first(node):
            result += "──"
        elif self.fl_visitor.is_last(node):
            result += "──"
        elif node.get_level() == 1:
            result += "├─"
        else:
            result += "│ "
        # straight lines
        if node.get_level() > 2:
            if self.fl_visitor.is_last(node):
                result += '─┴─' * (node.get_level() - 2)
            else:
                result += ' │ ' * (node.get_level() - 2)
        # header
        if self.fl_visitor.is_last(node):
            result += '─┴─'
        elif node.get_level() > 1:
            result += ' ├─'
        # icon
        if node.is_leaf():
            result += self.icon_family.leaf_icon
        else:
            result += self.icon_family.composite_icon
        # name surrounded by stars
        result += f'* {node.get_name()} *'
        # value
        if node.is_leaf() and node.get_value() is not None:
            result += f': {node.get_value()}'
        # padding
        result = f'{result} '.ljust(self.grid_width - 2, '─')
        # last layer
        if self.fl_visitor.is_first(node):
            result += '──'
        elif self.fl_visitor.is_last(node):
            result += '──'
        else:
            result += '─┤'
        print(result)


class StarStyledJSONNode(StyledJSONNode):
    def __init__(self, root: JSONNode, icon_family: IconFamily):
        super().__init__(root, icon_family)
        # Calculate maximum grid width
        self.grid_width_visitor = GridWidthVisitor()
        root.accept(self.grid_width_visitor)
        # Detect the first and last nodes
        self.fl_visitor = FirstLastVisitor()
        root.accept(self.fl_visitor)
        # Initialize icons
        self.icon_family = icon_family
        self._root = root  # Ensure root is properly assigned and named

    def render(self):
        render_visitor = RenderVisitor(self.grid_width_visitor.grid_width, self.fl_visitor, self.icon_family)
        self._root.accept(render_visitor)  # Use _root here instead of root



class StarStyledJSONNodeFactory(StyledJSONNodeFactory):

    def create(self, root: JSONNode, icon_family: IconFamily) -> StyledJSONNode:
        return StarStyledJSONNode(root, icon_family)
