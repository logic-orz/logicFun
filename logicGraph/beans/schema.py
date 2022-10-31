'''
Author: Logic
Date: 2022-04-27 09:41:14
LastEditTime: 2022-05-24 16:20:49
FilePath: \pyFuncs\cttqFuncs\graph\schema.py
Description: 
'''

from cttqFuncs.basic.exClass import BaseClass,  Tree
from cttqFuncs.basic.signClass import build, toDict, toStr
import cttqFuncs.basic.exFunc
from typing import Any, List
import abc
from abc import ABCMeta


class Label:
    """
    @ labels * 属性标签
    """

    def __init__(self) -> None:
        self.labels: List[str] = list()


@build
@toDict
@toStr
class Attribute(Label):
    """
    * 属性定义类
    @ name 属性名称
    @ type 属性类型
    @ desc 属性描述
    @ label 属性标签
    """

    def __init__(self, name: str = None) -> None:
        Label.__init__(self)
        self.name: str = name
        self.type: str = None
        self.desc: str = None


@build
@toDict
@toStr
class Concept(Label):
    """
    * 概念定义类
    @ key 概念唯一标识
    @ name 概念名称
    @ desc 概念描述
    @ attributes 概念属性列表
    """

    def __init__(self, key: str = None, name: str = None) -> None:
        Label.__init__(self)
        self.key = key
        self.name = name
        self.desc = None
        self.attributes: List[Attribute] = list()


@build
@toDict
@toStr
class Relation(Label):

    def __init__(self) -> None:
        Label.__init__(self)
        self.fromKey: List[str] = None  # * 关系起点
        self.toKey: List[str] = None  # * 关系终点
        self.key = None
        self.name = None  # * 关系名称
        self.desc = None  # * 关系描述


@build
@toDict
@toStr
class Schema(BaseClass):

    """
    # * 图谱模式对象
    """

    def __init__(self, name) -> None:
        self.name = name
        self.relations: List[Relation] = []
        self.concepts: Tree[Concept] = Tree()
