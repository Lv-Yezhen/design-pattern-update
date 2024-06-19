"""
sample output:

├─+name1
|  ├─*name2
│  └─+name3
│     └─*name4: value4
└─*name5

设计模式：
1. 工厂模式：StyledJSONNodeFactory
"""
from .style import StyledJSONNode, StyledJSONNodeFactory
from ..node import *
from ..icon import IconFamily

class TreeStyledJSONNode(StyledJSONNode):

    def __init__(self, root: JSONNode, icon_family: IconFamily):
        super().__init__(root, icon_family)

    def render(self) -> None:
        self._render_branch('', '', self._root)

    def _render(self, prefix_first: str, prefix_follow: str, node: JSONNode) -> None:
        if node.is_leaf():
            self._render_leaf(prefix_first, node)
        else:
            self._render_branch(prefix_first, prefix_follow, node)
    
    def _render_leaf(self, prefix: str, node: JSONLeaf) -> None:
        value = node.get_value()
        if value is None:
            print(f'{prefix}{self._icon_family.leaf_icon}{node.get_name()}')
        else:
            print(f'{prefix}{self._icon_family.leaf_icon}{node.get_name()}: {value}')

    def _render_branch(self, prefix_first: str, prefix_follow: str, node: JSONComposite) -> None:
        if not node.is_root():
            print(f'{prefix_first}{self._icon_family.composite_icon}{node.get_name()}')
        children = node.get_children()
        if len(children) == 0:
            return
        for child in children[:-1]:
            self._render(f'{prefix_follow}├─', f'{prefix_follow}│  ',child)
        self._render(f'{prefix_follow}└─', f'{prefix_follow}   ', children[-1])

class TreeStyledJSONNodeFactory(StyledJSONNodeFactory):

    def create(self, root: JSONNode, icon_family: IconFamily) -> StyledJSONNode:
        return TreeStyledJSONNode(root, icon_family)