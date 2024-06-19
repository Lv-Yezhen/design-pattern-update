"""
用于封装JSON数据结构的节点类
功能：
1. 从文件中获得JSON数据并解析为JSONNode对象
2. 对 Style 类提供接口，用于获取节点的信息
3. 实现遍历节点的功能
设计模式：
1. 组合模式：JSONNode 类是 JSONComposite 和 JSONLeaf 类是 JSONNode 类的子类，实现了组合模式。
2. 简单工厂模式：JSONNodeFactory 类是 JSONNode 的简单工厂类，用于从文件中读取JSON数据并解析为JSONNode对象。
"""
from abc import ABC, abstractmethod
from typing import List, Callable, Union
import json
import os
from .exception import FJEException

id = 0

class JSONNode(ABC):
    def __init__(self, name: str, level: int):
        global id 
        self._name = name
        self._level = level
        self._id = id
        id += 1

    @abstractmethod
    def accept(self, visitor):
        pass

    def is_root(self) -> bool:
        return self._level == 0

    def get_name(self) -> str:
        return self._name
    
    def get_id(self) -> int:
        return self._id
    
    def get_level(self) -> int:
        return self._level
    
class JSONComposite(JSONNode):
    def __init__(self, name: str, level: int):
        super().__init__(name, level)
        self._children: List[JSONNode] = []

    def accept(self, visitor):
        visitor.visit_composite(self)
        for child in self._children:
            child.accept(visitor)

    def add_child(self, child: JSONNode):
        self._children.append(child)
    
    def get_children(self) -> List[JSONNode]:
        return self._children

    def is_leaf(self) -> bool:
        return False
    
    def __iter__(self):
        return iter(self._children)
    
class JSONLeaf(JSONNode):
    def __init__(self, name: str, level: int, value: Union[str, None]):
        super().__init__(name, level)
        self._value = value

    def accept(self, visitor):
        visitor.visit_leaf(self)

    def is_leaf(self) -> bool:
        return True
    
    def get_value(self) -> Union[str, None]:
        return self._value

class JSONNodeFactory:
    def __init__(self, filepath: str):
        if not os.path.isfile(filepath):
            raise FJEException(f'文件{filepath}不存在')
        with open(filepath, 'r', encoding='utf-8') as f:
            self.json_data = json.load(f)
        if not isinstance(self.json_data, (dict, list)):
            raise FJEException(f'JSON根节点必须是字典或列表')
    
    def create(self) -> JSONNode:
        return self._create('', 0, self.json_data)

    def _create(self, name: str, level: int, obj) -> JSONNode:
        if isinstance(obj, list):
            return self._create_composite_from_list(name, level, obj)
        elif isinstance(obj, dict):
            return self._create_composite_from_dict(name, level, obj)
        else:
            return self._create_leaf(name, level, obj)

    def _create_composite_from_list(self, name: str, level: int, obj) -> JSONComposite:
        composite = JSONComposite(name, level)
        for idx, item in enumerate(obj):
            child = self._create(f'Array[{idx}]', level + 1, item)
            composite.add_child(child)
        return composite

    def _create_composite_from_dict(self, name: str, level: int, obj) -> JSONComposite:
        composite = JSONComposite(name, level)
        for key, value in obj.items():
            child = self._create(key, level + 1, value)
            composite.add_child(child)
        return composite
    
    def _create_leaf(self, name: str, level: int, obj) -> JSONLeaf:
        if obj is None:
            return JSONLeaf(name, level, None)
        else:
            return JSONLeaf(name, level, str(obj))


# == 访问 ==
class JSONVisitor(ABC):
    @abstractmethod
    def visit_composite(self, composite: JSONComposite):
        pass

    @abstractmethod
    def visit_leaf(self, leaf: JSONLeaf):
        pass

class JSONPrinterVisitor(JSONVisitor):
    def visit_composite(self, composite: JSONComposite):
        print(f'Composite: {composite.get_name()} Level: {composite.get_level()}')
    
    def visit_leaf(self, leaf: JSONLeaf):
        print(f'Leaf: {leaf.get_name()} Level: {leaf.get_level()} Value: {leaf.get_value()}')


class GridWidthVisitor(JSONVisitor):
    def __init__(self):
        self.grid_width = 16  # 初始宽度

    def visit_composite(self, composite: JSONComposite):
        self.update_grid_width(composite)

    def visit_leaf(self, leaf: JSONLeaf):
        self.update_grid_width(leaf)

    def update_grid_width(self, node: JSONNode):
        prefix_length = max((node.get_level() - 1) * 3 + 2, 0)
        name_length = len(node.get_name()) + 2
        if node.is_leaf() and node.get_value() is not None:
            name_length += len(node.get_value()) + 2
        name_length += 4  # Additional space for stars
        self.grid_width = max(self.grid_width, prefix_length + name_length + 2)

class FirstLastVisitor(JSONVisitor):
    def __init__(self):
        self.first_visited = False
        self.first_id = None
        self.last_id = None

    def visit_composite(self, composite: JSONComposite):
        if not self.first_visited:
            self.first_visited = True
            self.first_id = composite.get_id()
        self.last_id = composite.get_id()

    def visit_leaf(self, leaf: JSONLeaf):
        if not self.first_visited:
            self.first_visited = True
            self.first_id = leaf.get_id()
        self.last_id = leaf.get_id()

    def is_first(self, node: JSONNode) -> bool:
        return node.get_id() == self.first_id

    def is_last(self, node: JSONNode) -> bool:
        return node.get_id() == self.last_id

