from datetime import datetime
import os
import logging
import traceback
from logging.handlers import RotatingFileHandler


class Log:

    _root = None
    _logger = None
    home = './'
    log_file_name = 'tmp'
    notInited = True

    #  1 0(m) 000(k) 000(B)
    maxBytes = 1e7

    @staticmethod
    def get():
        if Log.notInited:
            Log.init()
            Log.notInited = False

        # Construct the name of the logger based on the file path
        code_file = traceback.extract_stack()[-2].filename

        relpath = os.path.relpath(code_file, Log._root)\
            .replace('.py', '')\
            .replace('/', '.')\
            .replace("\\", '.')

        root_name = os.path.basename(Log._root)
        return logging.getLogger(f"{root_name}.{relpath}")

    @staticmethod
    def init():
        assert os.path.isdir(Log.home), f'invalid home directory: "{Log.home}"'
        Log._root = os.path.abspath(Log.home)
        log_dir = os.path.join(Log._root, 'logs')
        if not os.path.isdir(log_dir):
            os.mkdir(log_dir)
        Log._configure_root_logger(log_dir, Log.log_file_name)

    @staticmethod
    def filter(name, level):
        level = str.upper(level)
        assert level in {'DEBUG', 'INFO', 'WARNING', 'ERROR'}
        logging.getLogger(name).setLevel(getattr(logging, level))

    @staticmethod
    def _configure_root_logger(log_dir, file_name):
        log_fmt = '[%(asctime)s | %(name)s | %(levelname)s]  %(message)s'
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        log_filepath = os.path.join(
            log_dir,
            file_name + "_" + datetime.now().strftime("%Y%m%d") + ".log")
        log_file_handler = RotatingFileHandler(filename=log_filepath,
                                               maxBytes=Log.maxBytes,
                                               backupCount=0,
                                               encoding="utf-8")
        log_file_handler.setFormatter(formatter)

        root_logger_name = os.path.basename(Log._root)
        root_logger = logging.getLogger(root_logger_name)
        root_logger.addHandler(log_file_handler)
        root_logger.addHandler(stream_handler)
        root_logger.setLevel(logging.INFO)  # default level
