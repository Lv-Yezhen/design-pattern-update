"""
设计模式：
1. 抽象工厂模式：创建多个不同风格的JSON展示器
2. 建造者模式：创建JSON展示器的各个部件
"""
from ..exception import FJEException
from ..icon import IconFamily
from ..node import JSONNodeFactory
from .tree_style import TreeStyledJSONNodeFactory
from .rectangle_style import RectangleStyledJSONNodeFactory
from .star_style import StarStyledJSONNodeFactory
import os
import json
from ..node import JSONNodeFactory

class StyledJSONBuilder:

    def __init__(self):
        self._icon_families = {
            'default': IconFamily(' ', ' '),
            'poker-face-icon-family': IconFamily('\u2666', '\u2660'),
            'emoji-icon-family': IconFamily('📦', '🧸')
        }
        self._styles_factory = {
            'tree': TreeStyledJSONNodeFactory(),
            'rect': RectangleStyledJSONNodeFactory(),
            'star': StarStyledJSONNodeFactory()
        }

    def create_styled_json(self, filepath: str, icon_family: str, style: str):
        try:
            icon_family = self._icon_families[icon_family]
        except KeyError:
            raise FJEException(f'找不到图标集：{icon_family}')
        try:
            style_factory = self._styles_factory[style]
        except KeyError:
            raise FJEException(f'找不到样式：{style}')
        json_node = JSONNodeFactory(filepath).create()
        return style_factory.create(json_node, icon_family)
    
    def load_icon_family(self, filepath):
        if os.path.isfile(filepath) == False:
            raise FJEException(f'找不到图标集文件：{filepath}')
        with open(filepath, 'r', encoding='utf-8') as f:
            icon_family_dict = json.load(f)
        try:
            for name, icon_family in icon_family_dict.items():
                self._icon_families[name] = IconFamily(icon_family['composite'], icon_family['leaf'])
        except KeyError:
            raise FJEException(f'图标集文件格式错误：{filepath}')

    def get_available_styles(self):
        return list(self._styles_factory.keys())
    
    def get_available_icon_families(self):
        return list(self._icon_families.keys())