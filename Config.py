import os.path
import sys
from dataclasses import dataclass, fields
from enum import Enum
from json import dump, load
from logging import ERROR
from os import getlogin
from os.path import abspath, join
from uuid import uuid4

from dacite import from_dict

from logger import Logger


class EnglishLanguageLevel(Enum):
    NA = "Not provided"
    A0 = "Foundation"
    A1 = "Elementary (A1)"
    A2 = "Pre-Intermediate (A2)"
    B1 = "Intermediate (B1)"
    B2 = "Upper Intermediate (B2)"
    C1 = "Advanced (C1)"
    C2 = "Proficiency (C2)"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller
    Source: https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = abspath(".")

    return join(base_path, relative_path)

@dataclass
class Config:
    SERVER_ADDRESS = 'http://srv22.mikr.us:20304/typingtest/'
    CONFIG_FILE_PATH = resource_path(join('src', 'config.json'))
    SENTENCES_FILE = resource_path(join('src', 'sentences.txt'))
    OUT_PATH = resource_path('out')
    OUTPUT_FILE = resource_path(join('out', 'result.json'))
    LOGGER = Logger('MainLogger', resource_path(join('out', 'log', 'log.log')), file_level=ERROR, console_level=ERROR).get_logger()
    FONT_FAMILY: str = "Century"
    WIDTH: int = 1000
    HEIGHT: int = 600
    POPUP_SIZE = (500, 400)
    USERNAME: str = getlogin()
    AGE: int = 20
    TIME_LIMIT: int = 180
    LANGUAGE_LEVEL: str = EnglishLanguageLevel.NA.value
    DEFAULT_USERNAME: str = str(uuid4())
    GDPR_CLAUSE = resource_path('src/gdpr_clause.txt')
    CONTACT_EMAIL = 'biometrictypingtest@gmail.com'

    def save_to_json(self):
        data = {f.name: getattr(self, f.name) for f in fields(self)}
        with open(self.CONFIG_FILE_PATH, 'w+') as f:
            dump(data, f, ensure_ascii=False, indent=4)
        self.LOGGER.info(f'Configuration saved to file {self.CONFIG_FILE_PATH}')



if not os.path.isfile(Config().CONFIG_FILE_PATH):
    Config().save_to_json()

config = from_dict(data_class=Config, data=load(open(Config.CONFIG_FILE_PATH)))