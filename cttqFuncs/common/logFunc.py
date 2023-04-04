import sys
from loguru import logger as log

class SimpleLog():
    _format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name: <10}</cyan>:<cyan>{function: <20}</cyan>:<cyan>{line: <3}</cyan> | <level>{message}</level>"


    @staticmethod
    def init(logFileName: str = 'tmp',
             useTimeRoute=False,
             useSizeRoute=False,
             logPath: str = './logs',
             logLevel: str = 'INFO') -> None:
        
        log.remove()
        log.add(
            sys.stdout,
            format=SimpleLog._format,
            level=logLevel
        )
  
        if useTimeRoute:
            log.add(logPath+'/'+logFileName+"_{time:YYYY-MM-DD}.log",
                    rotation="00:00",
                    encoding="utf-8",
                    enqueue=True,
                    compression="zip",
                    retention="100 days",
                    format=SimpleLog._format,
                    level=logLevel)

        if useSizeRoute:
            log.add(logPath+'/'+logFileName+"_{time:YYYY-MM-DD}.log",
                    rotation="100MB",
                    encoding="utf-8",
                    enqueue=True,
                    compression="zip",
                    format=SimpleLog._format,
                    retention="100 days",
                    level=logLevel)
