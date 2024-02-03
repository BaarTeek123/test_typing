from os import getlogin
from pathlib import Path
from uuid import getnode
from hashlib import sha256


class Config:
    ROOT_PATH = Path(__file__).parent
    DEFAULT_USERNAME=getlogin()+'_'+sha256(str(getnode()).encode()).hexdigest()
    DESTINATION_JSON_FILE_PATH = ROOT_PATH / 'destination_file.json'
    SENTENCES_FILE = ROOT_PATH / 'src' / 'sentences.txt'

