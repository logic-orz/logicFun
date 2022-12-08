'''
Author: Logic
Date: 2022-04-27 08:56:43
LastEditTime: 2022-05-25 14:32:10
FilePath: \pyFuncs\cttqFuncsSetup.py
Description: 
'''

from setuptools import setup

installs = [
    # 'impyla',
    # 'pymysql',
    # 'DBUtils',
    # 'IPython', 
    # 'prettytable'
]

setup(name="logicFunc",
      version="4.1",
      description="能力扩展",
      author="Logic",
      author_email='',
      url='',
      packages=['logicFunc',
                'logicFunc.conn',
                'logicFunc.basic',
                'logicFunc.common'
                ],
      install_requires=installs
      )
"""
* step1: python logicFuncSetup.py check
* step2: python logicFuncSetup.py build
* step3: python logicFuncSetup.py  bdist_wheel
* 上传: python logicFuncSetup.py sdist bdist_wheel  upload -r logic 
*     
* 卸载 : pip uninstall logicFunc -y
* 远程安装:
*   pip  --no-cache-dir install -U cttqFuncs --trusted-host=www.logic-orz.top -i http://www.logic-orz.top:8180/simple 
*           
"""
 