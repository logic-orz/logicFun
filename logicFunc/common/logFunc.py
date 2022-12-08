from datetime import datetime
import os
import traceback
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from logging import StreamHandler, Formatter, INFO, DEBUG, WARNING, ERROR, getLogger, getLevelName


class Log:

    basicPath = './'
    logFileName = 'tmp'
    useTimeRoute = False  # default SizeRouteHandler
    maxBytes = 1e7
    _root_path = None
    _hasInit = False
    _log_fmt = '[%(asctime)s | %(name)s | %(levelname)s]  %(message)s'
    _formatter = Formatter(_log_fmt, datefmt="%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _timeRoute(log_dir):
        log_filepath = os.path.join(log_dir, Log.logFileName+".log")
        time_file_handler = TimedRotatingFileHandler(filename=log_filepath,
                                                     when='midnight',
                                                     backupCount=0,
                                                     encoding="utf-8")

        time_file_handler.setFormatter(Log._formatter)
        return time_file_handler

    @staticmethod
    def _sizeRoute(log_dir):
        log_filepath = os.path.join(
            log_dir, Log.logFileName + "_" + datetime.now().strftime("%Y%m%d") + ".log")

        size_file_handler = RotatingFileHandler(filename=log_filepath,
                                                maxBytes=Log.maxBytes,
                                                backupCount=100,
                                                encoding="utf-8")
        size_file_handler.setFormatter(Log._formatter)
        return size_file_handler

    @staticmethod
    def init():
        Log._hasInit = True
        assert os.path.isdir(
            Log.basicPath), f'invalid home directory: "{Log.basicPath}"'
        Log._root_path = os.path.abspath(Log.basicPath)
        log_dir = os.path.join(Log._root_path, 'logs')
        if not os.path.isdir(log_dir):
            os.mkdir(log_dir)

        root_logger_name = os.path.basename(Log._root_path)
        root_logger = getLogger(root_logger_name)

        stream_handler = StreamHandler()
        stream_handler.setFormatter(Log._formatter)
        root_logger.addHandler(stream_handler)

        if Log.useTimeRoute:
            root_logger.addHandler(Log._timeRoute(log_dir))
        else:
            root_logger.addHandler(Log._sizeRoute(log_dir))

        root_logger.setLevel(INFO)  # default level

    @staticmethod
    def filter(name, level):
        level = str.upper(level)
        assert level in {'DEBUG', 'INFO', 'WARNING', 'ERROR'}
        getLogger(name).setLevel(getLevelName(level))

    @staticmethod
    def get():
        if not Log._hasInit:
            Log.init()
        # Construct the name of the logger based on the file path
        code_file = traceback.extract_stack()[-2].filename

        relpath = os.path.relpath(code_file, Log._root_path)\
            .replace('.py', '')\
            .replace('/', '.')\
            .replace("\\", '.')

        root_name = os.path.basename(Log._root_path)
        return getLogger(f"{root_name}.{relpath}")
