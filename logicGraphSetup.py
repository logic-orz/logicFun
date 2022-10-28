'''
Author: Logic
Date: 2022-04-27 08:56:43
LastEditTime: 2022-05-25 14:32:10
FilePath: \pyFuncs\cttqFuncsSetup.py
Description: 
'''

from setuptools import setup

installs = [
 
]

setup(name="logicGraph",
      version="1.0",
      description="能力扩展",
      author="Logic",
      author_email='',
      url='',
      packages=['logicGraph'
                ],
      install_requires=installs
      )
"""
* step1: python logicGraphSetup.py check
* step2: python logicGraphSetup.py build
* step3: python logicGraphSetup.py  bdist_wheel
* 上传: python logicGraphSetup.py sdist bdist_wheel  upload -r cttq 
*       python logicGraphSetup.py sdist bdist_wheel  upload -r local 
* 卸载 : pip uninstall logicGraph -y
* 远程安装:pip  --no-cache-dir install -U logicGraph --trusted-host=172.16.0.224 -i http://172.16.0.224:8180/simple 
*   pip  --no-cache-dir install -U logicGraph --trusted-host=10.81.87.43 -i http://10.81.87.43:8180/simple
*           
"""
 