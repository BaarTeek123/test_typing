from random import choice
from json import dump


def generate_sentence(path: str) -> str:
    with open(path, mode='r', encoding='utf-8') as f:
        return choice(f.read().split('\n\n'))


def save_and_send_data(data: str, file_path: str):
    with open(file_path, 'a+') as f:
        dump(data, f)
