from random import choice
from json import dump

from kivy.uix.textinput import TextInput


def generate_sentence(path: str) -> str:
    with open(path, mode='r', encoding='utf-8') as f:
        return choice(f.read().split('\n\n'))


def save_and_send_data(data: str, file_path: str):
    with open(file_path, 'a+') as f:
        dump(data, f)


class NoPasteTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        # Check if the text is being pasted (substring length significantly larger than typical typing)
        if len(substring) > 1:
            # If it's likely a paste action, don't insert the text
            return
        # Otherwise, proceed with the normal text insertion
        super(NoPasteTextInput, self).insert_text(substring, from_undo=from_undo)


