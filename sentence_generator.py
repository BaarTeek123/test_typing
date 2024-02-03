from random import choice

from Config import Config


def generate_sentence(path: str) -> str:
    with open(path, 'r') as f:
        return choice(f.read().split('\n\n'))

# print(generate_sentence(Config.SENTENCES_FILE))