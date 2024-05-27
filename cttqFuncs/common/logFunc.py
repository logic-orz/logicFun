import sys
from loguru import logger as log
from typing import Any, Callable


class SimpleLog():
    """通用日志工具
    record
    """
    _format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> [<level>{level}</level>] <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"
    _hasInit = False
    _logPath = './logs'

    @staticmethod
    def init(logFileName: str = 'tmp',
             useTimeRoute=False,
             useSizeRoute=False,
             logPath: str = None,
             logLevel: str = 'INFO') -> None:

        if SimpleLog._hasInit:
            return

        if logPath:
            if logPath.endswith('/'):
                logPath = logPath[:-1]
            SimpleLog._logPath = logPath

        log.remove()
        log.add(
            sys.stdout,
            format=SimpleLog._format,
            level=logLevel
        )

        path = SimpleLog._logPath+'/'+logFileName+"_{time:YYYY-MM-DD}.log"
        if useTimeRoute:

            log.add(path,
                    rotation="00:00",
                    encoding="utf-8",
                    enqueue=True,
                    # compression="zip",
                    retention="100 days",
                    format=SimpleLog._format,
                    level=logLevel)

        if useSizeRoute:
            log.add(path,
                    rotation="100MB",
                    encoding="utf-8",
                    enqueue=True,
                    # compression="zip",
                    format=SimpleLog._format,
                    retention="100 days",
                    level=logLevel)

        SimpleLog._hasInit = True

    # ?     filter=lambda record:record['name'] == 'filterByName'
    # ?     filter=lambda record:record['function'] =='filterByFunc'
    # ?     filter=lambda record:record['level'].name == 'filterByLevel'

    @staticmethod
    def addTimeRoute(logFileName: str,
                     logLevel: str = 'DEBUG',
                     filter: Callable[[Any], bool] = None):

        path = SimpleLog._logPath+'/'+logFileName+"_{time:YYYY-MM-DD}.log"

        log.add(path,
                rotation="00:00",
                encoding="utf-8",
                enqueue=True,
                # compression="zip",
                retention="100 days",
                format=SimpleLog._format,
                level=logLevel,
                filter=filter)

    # ?     filter=lambda record:record['name'] == 'filterByName'
    # ?     filter=lambda record:record['function'] =='filterByFunc'
    # ?     filter=lambda record:record['level'].name == 'filterByLevel'
    @staticmethod
    def addSizeRoute(logFileName: str,
                     logLevel: str = 'DEBUG',
                     filter: Callable[[Any], bool] = None):
        path = SimpleLog._logPath+'/'+logFileName+"_{time:YYYY-MM-DD}.log"

        log.add(path,
                rotation="100MB",
                encoding="utf-8",
                enqueue=True,
                # compression="zip",
                format=SimpleLog._format,
                retention="100 days",
                level=logLevel,
                filter=filter)
