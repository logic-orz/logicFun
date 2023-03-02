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

setup(name="cttqFuncs",
      version="4.2",
      description="能力扩展",
      author="Logic",
      author_email='',
      url='',
      packages=['cttqFuncs',
                'cttqFuncs.conn',
                'cttqFuncs.basic',
                'cttqFuncs.common',
                'cttqFuncs.algorithm'
                ],
      install_requires=installs
      )
"""
* step1: python cttqFuncsSetup.py check
* step2: python cttqFuncsSetup.py build
* step3: python cttqFuncsSetup.py bdist_wheel
* 上传: python cttqFuncsSetup.py sdist bdist_wheel  upload -r cttq 
* 卸载 : pip uninstall cttqFuncs -y
* 远程安装: pip  --no-cache-dir install -U cttqFuncs --trusted-host=172.16.0.224 -i http://172.16.0.224:8180/simple 
*           
"""
 