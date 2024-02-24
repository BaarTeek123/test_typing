import os.path
from enum import Enum
from os import getlogin
from pathlib import Path
from uuid import getnode, uuid4
from hashlib import sha256
from logging import ERROR, DEBUG
from logger import Logger
from dacite import from_dict
from dataclasses import dataclass, fields
from json import dump, load


class EnglishLanguageLevel(Enum):
    NA = "Not provided"
    A0 = "Foundation"
    A1 = "Elementary (A1)"
    A2 = "Pre-Intermediate (A2)"
    B1 = "Intermediate (B1)"
    B2 = "Upper Intermediate (B2)"
    C1 = "Advanced (C1)"
    C2 = "Proficiency (C2)"


@dataclass
class Config:
    SERVER_ADDRESS = 'http://srv22.mikr.us:20304/typingtest/'
    ROOT_PATH = Path(__file__).parent
    SOURCE_PATH = ROOT_PATH / 'src'
    CONFIG_FILE_PATH = SOURCE_PATH / 'config.json'
    SENTENCES_FILE = SOURCE_PATH / 'sentences.txt'
    OUT_PATH = ROOT_PATH / 'out'
    OUTPUT_FILE = ROOT_PATH / 'out' / 'result.json'
    LOGGER = Logger('MainLogger', OUT_PATH / 'log' / 'log.log',  file_level=ERROR, console_level=DEBUG).get_logger()
    FONT_FAMILY: str = "Century"
    WIDTH: int = 1000
    HEIGHT: int = 600
    POPUP_SIZE = (500, 400)
    USERNAME: str = getlogin()
    AGE: int = 20
    TIME_LIMIT: int = 180
    LANGUAGE_LEVEL: str = EnglishLanguageLevel.NA.value
    DEFAULT_USERNAME: str = str(uuid4())
    GDPR_CLAUSE = SOURCE_PATH / 'gdpr_clause.txt'

    def save_to_json(self):
        data = {f.name: getattr(self, f.name) for f in fields(self)}
        with open(self.CONFIG_FILE_PATH, 'w+') as f:
            dump(data, f, ensure_ascii=False, indent=4)
        self.LOGGER.info(f'Configuration saved to file {self.CONFIG_FILE_PATH}')


config = Config()
if not os.path.isfile(Config.CONFIG_FILE_PATH):
    config.save_to_json()

config = from_dict(data_class=Config, data=load(open(Config.CONFIG_FILE_PATH)))