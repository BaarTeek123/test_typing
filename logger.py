import logging
from typing import Union
from pathlib import Path
from os.path import dirname
from os import makedirs

class Logger:
    def __init__(self, name: str, file_path: Union[str | Path], file_level=logging.ERROR, console_level=logging.DEBUG):

        makedirs(dirname(file_path), exist_ok=True)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Set the logger to the lowest level

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Create file handler and set level to file_level
        # fh = logging.FileHandler(file_path)
        # fh.setLevel(file_level)
        # fh.setFormatter(formatter)

        # Create console handler and set level to console_level
        ch = logging.StreamHandler()
        ch.setLevel(console_level)
        ch.setFormatter(formatter)

        # Add handlers to the logger
        # self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger


