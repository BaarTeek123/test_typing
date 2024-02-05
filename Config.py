import os.path
from os import getlogin
from pathlib import Path
from uuid import getnode
from hashlib import sha256
from logging import ERROR, DEBUG
from logger import Logger
from dacite import from_dict
from dataclasses import dataclass, asdict, fields
from json import dump, load


@dataclass
class Config:
    ROOT_PATH = Path(__file__).parent
    SOURCE_PATH = ROOT_PATH / 'src'
    CONFIG_FILE_PATH = SOURCE_PATH / 'config.json'
    SENTENCES_FILE = SOURCE_PATH / 'sentences.txt'
    OUT_PATH = ROOT_PATH / 'out'
    OUTPUT_FILE = ROOT_PATH / 'out' / 'result.json'
    LOGGER = Logger('MainLogger', OUT_PATH / 'log' / 'log.log',  file_level=ERROR, console_level=DEBUG).get_logger()
    FONT_FAMILY: str = "Century"
    WIDTH: int = 600
    HEIGHT: int = 300
    DEFAULT_USERNAME: str = getlogin()+'_'+sha256(str(getnode()).encode()).hexdigest()

    def save_to_json(self):
        self.LOGGER.info('Configuration saved to file')
        data = {f.name: getattr(self, f.name) for f in fields(self)}
        with open(self.CONFIG_FILE_PATH, 'w') as f:
            dump(data, f, ensure_ascii=False, indent=4)


config = Config()
if not os.path.isfile(Config.CONFIG_FILE_PATH):
    config.save_to_json()

config = from_dict(data_class=Config, data=load(open(Config.CONFIG_FILE_PATH)))