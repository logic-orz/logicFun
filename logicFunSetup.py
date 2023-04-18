from setuptools import setup

installs = [
    'impyla',
    'pymysql',
    'DBUtils',
    'IPython', 
    'prettytable',
    'redis',
    'redis-py-cluster',
    'cacheout',
    'xlwt',
    'xlrd2',
    'openpyxl',
    'sqlalchemy',
    'python-consul',
    'apscheduler',
    'loguru'
]

setup(name="logicFun",
      version="4.1",
      description="能力扩展",
      author="Logic",
      author_email='',
      url='',
      packages=['logicFun',
                'logicFun.conn',
                'logicFun.basic',
                'logicFun.common',
                'logicFun.algorithm',
                'logicFun.graph',
                'logicFun.graph.extras',
                'logicFun.web'
                ],
      install_requires=installs
      )
"""
* step1: python logicFunSetup.py check
* step2: python logicFunSetup.py build
* step3: python logicFunSetup.py  bdist_wheel
* 上传: python logicFunSetup.py sdist bdist_wheel  upload -r logic 
*     
* 卸载 : pip uninstall logicFun -y
* 远程安装:
*   pip  --no-cache-dir install -U logicFun --trusted-host=www.logic-orz.top -i http://www.logic-orz.top:8180/simple 
*           
"""
 