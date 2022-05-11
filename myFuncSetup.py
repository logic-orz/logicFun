'''
Author: Logic
Date: 2022-04-27 08:56:43
LastEditTime: 2022-05-11 10:57:24
FilePath: \pyFuncs\myFuncSetup.py
Description: 
'''

from setuptools import setup

installs = [
    'impyla',
    'pymysql',
    'redis',
    'redis-py-cluster',
    'SQLAlchemy',
    'DBUtils'
]

setup(name="myFunc",
      version="1.0",
      description="能力扩展",
      author="Logic",
      author_email=' ',
      url='https://gitlab.cttq.com/8608858/pyfuncs',
      packages=['myFunc', 'myFunc.conn', 'myFunc.basic', 'myFunc.graph'],
      install_requires=installs
      )
"""
* step1: python myFuncSetup.py check
* step2: python myFuncSetup.py build
* step3: python myFuncSetup.py  bdist_wheel
* all: python myFuncSetup.py sdist bdist_wheel  upload -r local 
* pip install dist\\myFunc-1.0-py3-none-any.whl --force-reinstall
* pip  --no-cache-dir install -U myFunc --trusted-host=10.81.87.43 -i http://10.81.87.43:8180/simple
"""
