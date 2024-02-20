from setuptools import setup

installs = [
    'impyla',
    'pymysql',
    'DBUtils',
    # 'IPython',
    # 'prettytable',
    # 'redis',
    # 'redis-py-cluster',
    'cacheout',
    'xlwt',
    'xlrd2',
    'xlsxwriter',
    'sqlalchemy',
    # 'python-consul',
    'apscheduler',
    'loguru',
    'aiohttp',
    # 'pyfiglet',
    'aiomysql',
    'pydantic'
]

setup(name="cttqFuncs",
      version='4.9',
      description="能力扩展",
      author="Logic",
      author_email='saltedfishno.5@gmail.com',
      url='',
      packages=['cttqFuncs',
                'cttqFuncs.conn',
                'cttqFuncs.basic',
                'cttqFuncs.common',
                'cttqFuncs.algorithm',
                'cttqFuncs.graph',
                'cttqFuncs.graph.extras',
                'cttqFuncs.web'
                ],
      install_requires=installs
      )
"""
* step1: python cttqFuncsSetup.py check
* step2: python cttqFuncsSetup.py build
* step3: python cttqFuncsSetup.py bdist_wheel  
* 本地安装： pip install dist/cttqFuncs-4.9-py3-none-any.whl 
* 上传: python cttqFuncsSetup.py sdist bdist_wheel  upload -r cttq
* 卸载 : pip uninstall cttqFuncs -y
* 远程安装: pip  --no-cache-dir install -U cttqFuncs --trusted-host=172.16.0.224 -i http://172.16.0.224:8180/simple
*
"""
