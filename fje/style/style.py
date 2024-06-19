from abc import ABC, abstractmethod
from ..node import JSONNode
from ..icon import IconFamily

"""
抽象产品：用于渲染JSON节点的样式
"""
class StyledJSONNode:

    def __init__(self, root: JSONNode, icon_family: IconFamily) -> None:
        self._root = root
        self._icon_family = icon_family

    @abstractmethod
    def render(self) -> None:
        pass

"""
抽象工厂：用于创建StyledJSONNode
"""
class StyledJSONNodeFactory(ABC):

    @abstractmethod
    def create(self, root: JSONNode, icon_family: IconFamily) -> StyledJSONNode:
        pass