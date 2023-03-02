from datetime import datetime
import os
import logging
from logging import Logger
import colorlog
import traceback
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from logging import StreamHandler, Formatter, INFO, DEBUG, WARNING, ERROR, getLogger, getLevelName
from ..basic.configFunc import getDict,getValue
from typing import Dict

class BasicLog():
    
    _formatter = Formatter('[%(asctime)s | %(name)s | %(levelname)s]  %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    _color_formatter = colorlog.ColoredFormatter(
            '%(log_color)s [%(asctime)s | %(name)s |  %(log_color)s%(levelname)s]  %(message)s',
            datefmt="%Y-%m-%d %H:%M:%S",
            reset=True,
            log_colors={
                'DEBUG': 'bold_cyan',
                'INFO': 'bold_green',
                'WARNING': 'bold_yellow',
                'ERROR': 'bold_red',
                'CRITICAL': 'red',
            },
            secondary_log_colors={
                'message': {
                    'DEBUG': 'blue',
                    'INFO': 'blue',
                    'WARNING': 'blue',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red'
                }
            },
            style='%'
        )
    
    
    
    def _streamRoute(self):
        stream_handler = StreamHandler()
        stream_handler.setFormatter(BasicLog._color_formatter)
        return stream_handler
        

    def _timeRoute(self,when):
        log_filepath = os.path.join(self.logPath, self.logFileName+".log")
        time_file_handler = TimedRotatingFileHandler(filename=log_filepath,
                                                     when=when,
                                                     backupCount=0,
                                                     encoding="utf-8")

        time_file_handler.setFormatter(BasicLog._formatter)
        return time_file_handler
    
    def _sizeRoute(self,maxBytes):
        log_filepath = os.path.join(self.logPath, self.logFileName + "_" + datetime.now().strftime("%Y%m%d") + ".log")

        size_file_handler = RotatingFileHandler(filename=log_filepath,
                                                    maxBytes=maxBytes,
                                                    backupCount=100,
                                                    encoding="utf-8")
        size_file_handler.setFormatter(BasicLog._formatter)
        return size_file_handler
    
    def __init__(self,
                 logPath,
                 logFileName='tmp',
                 useTimeRoute:bool=False,
                 timeWhen='midnight',
                 useSizeRoute:bool=False,
                 maxBytes= 1e7,
                 logLevel='info'
             ):
        if useTimeRoute or useSizeRoute:
            self.checkLogPath(logPath)
        
        self.logFileName=logFileName
        
        self.root_logger_name = os.path.basename('./')
        root_logger = getLogger(self.root_logger_name)

        root_logger.addHandler(self._streamRoute())

        if useTimeRoute:
            root_logger.addHandler(self._timeRoute(timeWhen))
        if useSizeRoute:
            root_logger.addHandler(self._sizeRoute(maxBytes))

        self.setLevel(root_logger,logLevel) 
        
    
    def checkLogPath(self,logPath):
        # 创建日志文件夹
        assert os.path.isdir(
            logPath), f'invalid home directory: "{logPath}"'
        logPath = os.path.abspath(logPath)
        self.logPath=os.path.join(logPath, 'logs')
        if not os.path.isdir(self.logPath):
            os.mkdir(self.logPath)
    
    def setLevel(self,logger:Logger, level):
        level = str.upper(level)
        assert level in {'DEBUG', 'INFO', 'WARNING', 'ERROR'}
        logger.setLevel(getLevelName(level))

    def get(self,code_file):
        # Construct the name of the logger based on the file path
       
        relpath = os.path.relpath(code_file, self.root_logger_name)\
            .replace('.py', '')\
            .replace('/', '.')\
            .replace("\\", '.')

        return getLogger(f"{self.root_logger_name}.{relpath}")

class SimpleLog:

    basicPath = './'
    logFileName = 'tmp'
    logLevel='INFO'
    useTimeRoute = False  # default SizeRouteHandler
    useSizeRoute =False
    _instance = None
    
    @staticmethod
    def get():
        if not SimpleLog._instance:
            SimpleLog._instance=BasicLog(
                logPath=SimpleLog.basicPath,
                useSizeRoute=SimpleLog.useSizeRoute,
                useTimeRoute=SimpleLog.useTimeRoute,
                logFileName=SimpleLog.logFileName,
                logLevel=SimpleLog.logLevel)
        
        return  SimpleLog._instance.get( traceback.extract_stack()[-2].filename)
    

class ConfigLog():
    """
    
    @param fileName     :日志文件名             e.g. tmp
    @param logPath      :日志文件保存路径       e.g. E:\downloads
    @param timeRoute    :是否按照时间生成文件   e.g. False
    @param sizeRoute    :是否按照大小生成文     e.g. False
    @param logLevel     :日志输出等级           e.g. debug,info,warning,error
    
    
    """
    
    _instance = False
        
    @staticmethod
    def get():
        if not ConfigLog._instance:
            logConfig:Dict[str,str]=getDict('log')
        
            fileName=logConfig['fileName'] if 'fileName' in logConfig else 'tmp'
            logPath=logConfig['logPath'] if 'logPath' in logConfig else './'
            
            sizeRoute=False
            maxBytes=1e7
            if logConfig['sizeRoute'] and logConfig['sizeRoute'] == 'True':  
                sizeRoute=True
                if 'maxBytes' in logConfig:
                    maxBytes=int(logConfig['maxBytes'])
            
            timeRoute=False
            if logConfig['timeRoute'] and logConfig['timeRoute'] == 'True':  
                timeRoute=True
                
            level="info"
            if 'logLevel' in logConfig and logConfig['logLevel']!='':
                level = logConfig['logLevel']
            ConfigLog._instance=BasicLog(
                logPath=logPath,
                useSizeRoute=sizeRoute,
                maxBytes=maxBytes,
                useTimeRoute=timeRoute,
                logFileName=fileName,
                logLevel=level)
           
        return  ConfigLog._instance.get(traceback.extract_stack()[-2].filename)