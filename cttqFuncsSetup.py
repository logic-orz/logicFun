'''
Author: Logic
Date: 2022-04-27 08:56:43
LastEditTime: 2022-05-19 15:30:07
FilePath: \pyFuncs\cttqFuncsSetup.py
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

setup(name="cttqFuncs",
      version="2.0",
      description="能力扩展",
      author="Logic",
      author_email=' ',
      url='https://gitlab.cttq.com/8608858/pyfuncs',
      packages=['cttqFuncs', 'cttqFuncs.conn',
                'cttqFuncs.basic', 'cttqFuncs.graph'],
      install_requires=installs
      )
"""
* step1: python cttqFuncsSetup.py check
* step2: python cttqFuncsSetup.py build
* step3: python cttqFuncsSetup.py  bdist_wheel
* 上传: python cttqFuncsSetup.py sdist bdist_wheel  upload -r local 
* 卸载 : pip uninstall cttqFuncs -y
* 远程安装: pip  --no-cache-dir install -U cttqFuncs --trusted-host=10.81.87.43 -i http://10.81.87.43:8180/simple
"""
