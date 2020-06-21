import datetime
import sys
import os
import tempfile
import logging


LOGGER_FORMAT = '%(asctime)s - ' \
                '%(module)s.%(funcName)s - ' \
                '(%(levelname)s) - %(lineno)d: %(message)s'
FORMATTER = logging.Formatter(LOGGER_FORMAT)


def get_console_handler():
    """Get the console log handler

    :rtype: logging.StreamHandler
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler(file_name):
    """Get the file log handler

    :rtype: logging.StreamHandler
    """
    # set log path to temp location
    # this path resolve to something like this:
    # C:\Users\<USER_NAME>\AppData\Local\Temp\_LOG
    log_temp_location = os.path.join(tempfile.gettempdir(), '_LOG')
    if not os.path.exists(log_temp_location):
        os.makedirs(log_temp_location)

    today = str(datetime.date.today())
    log_file = os.path.join(log_temp_location, f'{file_name}_{today}.log')

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name=__name__):
    """python logging module

    :param logger_name: name of logger handle
    :return: logger
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler(logger_name))
    logger.propagate = False
    return logger
