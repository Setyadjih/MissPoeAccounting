import datetime
import sys
import os
import tempfile
import logging
from getpass import getuser

from PySide2.QtWidgets import QMessageBox

from core.constants import CAT_REF, DEFAULT_CATEGORIES

LOGGER_FORMAT = '%(asctime)s - ' \
                '%(module)s.%(funcName)s - ' \
                '%(levelname)s - %(message)s'
FORMATTER = logging.Formatter(LOGGER_FORMAT)


def get_console_handler():
    """Get the console log handler

    :rtype: logging.StreamHandler
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler(file_name, log_dir=None):
    """Get the file log handler

    :rtype: logging.StreamHandler
    """
    # set log path to temp location
    # this path resolve to something like this:
    # C:\Users\<USER_NAME>\AppData\Local\Temp\_LOG
    # file_dir for custom path
    log_temp_location = os.path.join(tempfile.gettempdir(), '_LOG')
    if log_dir:
        log_temp_location = log_dir
        print(f"log_dir: {log_dir}")
    if not os.path.exists(log_temp_location):
        os.makedirs(log_temp_location)

    today = str(datetime.date.today())
    log_file = os.path.join(log_temp_location, f'{file_name}_{today}.log')
    if log_dir:
        log_file = os.path.join(
            log_temp_location, f'{getuser()}_{file_name}_{today}.log'
        )

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


def write_categories_file():
    with open(CAT_REF, "w") as new_file:
        for key in DEFAULT_CATEGORIES.keys():
            new_file.write(f"[{key}]")
            for value in DEFAULT_CATEGORIES[key]:
                new_file.write(value)
    message = QMessageBox()
    message.setWindowTitle("Default categories file created")
    message.setText(f"A default category list was created. Please "
                    f"edit the {CAT_REF} file and rerun "
                    f"the program if you need to add categories")
    message.exec_()


def read_categories_file():
    category_dict = {}
    is_cat = False

    with open(CAT_REF, "r") as cat_file:
        lines = cat_file.readlines()

        for line in lines:
            if "[MISC]" in line:
                is_cat = False
                continue

            if "[CATEGORIES]" in line:
                is_cat = True
                continue

            key = "CATEGORIES" if is_cat else "MISC"
            category_dict[key] = line

    return category_dict