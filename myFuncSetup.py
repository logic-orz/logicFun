'''
Author: Logic
Date: 2022-04-27 08:56:43
LastEditTime: 2022-04-29 11:19:52
FilePath: \pyFuncs\myFuncSetup.py
Description: 
'''
from setuptools import setup 
setup(name="myFunc",
      version="1.0",
      description="能力扩展",
      author="Logic",
      author_email=' ',
      url=' ',
      packages=['myFunc','myFunc.conn','myFunc.basic'])
"""
* step1: python myFuncSetup.py check
* step2: python myFuncSetup.py build
* step3: python myFuncSetup.py  bdist_wheel
* all: python myFuncSetup.py check build  bdist_wheel 
* pip install dist\\myFunc-1.0-py3-none-any.whl --force-reinstall
"""
