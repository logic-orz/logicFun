'''
Author: Logic
Date: 2022-04-27 09:41:14
LastEditTime: 2022-05-12 15:10:23
FilePath: \pyFuncs\myFunc\graph\schema.py
Description: 
'''

from myFunc.basic.myClass import BaseClass, Tree
import myFunc.basic.signFunc
from typing import Dict, Any, List
import abc
from abc import ABCMeta


class Attribute(BaseClass):

    def __init__(self, name: str = None) -> None:
        self.name = name  # * 属性名称
        self.type = None  # * 属性类型
        self.desc = None  # * 属性描述
        self.labels: List[str] = []  # * 属性标签


class Concept(BaseClass):
    def __init__(self, key: str = None, name: str = None) -> None:
        self.key = key
        self.name = name  # * 概念名称
        self.desc = None  # * 概念描述
        self.labels: List[str] = []  # * 概念标签
        self.attributes: List[Attribute] = []  # * 概念属性列表


class Relation(BaseClass):
    def __init__(self) -> None:

        self.fromKey: List[str] = None  # * 关系起点
        self.toKey: List[str] = None  # * 关系终点
        self.key = None
        self.name = None  # * 关系名称
        self.desc = None  # * 关系描述
        self.labels: List[str] = []  # * 关系标签


class Schema(BaseClass):

    relations: List[Relation] = []
    concepts: Tree[Concept] = Tree()
    """
    # * 图谱模式对象
    """

    def __init__(self, name) -> None:
        self.name = name

