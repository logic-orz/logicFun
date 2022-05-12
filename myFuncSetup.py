'''
Author: Logic
Date: 2022-04-27 08:56:43
LastEditTime: 2022-05-11 11:15:45
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
* 上传: python myFuncSetup.py sdist bdist_wheel  upload -r local 
* 本地安装: pip install dist\\myFunc-1.0-py3-none-any.whl --force-reinstall
* 远程安装: pip  --no-cache-dir install -U myFunc --trusted-host=10.81.87.43 -i http://10.81.87.43:8180/simple
"""
