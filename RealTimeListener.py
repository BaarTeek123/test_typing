import pynput.keyboard as keyboard
import pynput.mouse as mouse
from typing import List, Dict, Optional

class Combinations:
    """A class which includes key combinations or sets of keys."""
    END_KEYS = {keyboard.Key.esc, keyboard.Key.f4}  # key combination to finish listening
    NEXT_WORD_KEYS = {keyboard.Key.space, ':', ",", "/", '"'}  # key of next words
    NEW_CONTEXT_KEYS = {}
    CONTEXT_END = {keyboard.Key.enter}
    NUMPAD_NUMBERS_KEYS = {}



class RealTimeKeyListener:
    _left_button_mouse_is_pressed: bool = False
    _position: int = 0
    _previous_key: Optional[keyboard.Key] = None
    _sentence: str = ""
    _list_of_words: List[str] = []
    _keys_counter: Dict[str, int] = {}
    _non_printable_counter: Dict[str, int] = {}
    _non_printable_digraphs: List[str] = []
    _pressed_keys: List[str] = []

    def __init__(self):
        self.keyboard_listener = keyboard.Listener(on_press=self._on_press)
        self.mouse_listener = mouse.Listener(on_click=self._on_click)
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def get_sentence(self) -> str:
        return self._sentence

    def _on_click(self, x: int, y: int, button: mouse.Button, pressed: bool) -> None:
        self._pressed_keys.append(str(button))
        if pressed and button == mouse.Button.left:
            self._left_button_mouse_is_pressed = True

    def _on_press(self, key) -> None:
        self._pressed_keys.append(str(key))
        if self._previous_key in Combinations.END_KEYS and key in Combinations.END_KEYS:
            self._is_finished()

        elif ((key in Combinations.CONTEXT_END) or (key in Combinations.NEW_CONTEXT_KEYS)
              or (self._left_button_mouse_is_pressed) or (hasattr(key, 'char') and key.char in Combinations.CONTEXT_END)) \
                and self._sentence:
            self._on_finished_context()

        elif key == keyboard.Key.delete and self._sentence and self._position != 0:
            self._delete_or_backspace_chars(delete=True)

        elif key == keyboard.Key.backspace and self._sentence:
            self._delete_or_backspace_chars(delete=False)

        elif key == keyboard.Key.left and abs(self._position) <= len(self._sentence):
            self._position -= 1

        elif key == keyboard.Key.right and self._position < 0:
            self._position += 1

        elif (hasattr(key, 'char') and key.char is not None and len(key.char) < 2) or key in Combinations.NUMPAD_NUMBERS_KEYS or key == keyboard.Key.space:
            self._insert_char(key)
        self._previous_key = key
        self._left_button_mouse_is_pressed = False

    def _on_finished_context(self) -> None:
        pass

    def _is_finished(self) -> None:
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

    def _delete_or_backspace_chars(self, delete: bool) -> None:
        if delete and self._position < -1:
            self._sentence = self._sentence[:self._position] + self._sentence[self._position + 1:]
        elif delete and self._position == -1:
            self._sentence = self._sentence[:-1]
        elif not delete and self._position == 0:
            self._sentence = self._sentence[:-1]
        elif not delete and self._position < 0:
            self._sentence = self._sentence[:self._position - 1] + self._sentence[self._position:]
        self._position = min(self._position + 1, 0) if delete else self._position

    def _insert_char(self, key) -> None:
        char = key.char if hasattr(key, 'char') and key.char else ''
        if key in Combinations.NUMPAD_NUMBERS_KEYS or key == keyboard.Key.space:
            char = key._value_.char  # Assuming _value_ contains the character representation
        if char and char.isprintable():
            if self._position == 0:
                self._sentence += char
            else:
                self._sentence = self._sentence[:self._position] + char + self._sentence[self._position:]

'''
class RealTimeKeyListener:
    __left_button_mouse_is_pressed = False
    __position = 0  # parameter is <=0
    __previous_key = None
    __sentence = ""
    __list_of_words = None
    __keys_counter = {}
    __non_printable_counter = {}
    __non_printable_digraphs = []
    __pressed_keys = []
    keyboard_listener = None
    mouse_listener = None

    def get_sentence(self):
        return self.__sentence

    def __init__(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.__on_press)
        self.mouse_listener = mouse.Listener(on_click=self.__on_click)
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def __on_click(self, x, y, button, pressed):
        self.__pressed_keys.append(str(button))
        if pressed and button == mouse.Button.left:
            self.__left_button_mouse_is_pressed = True

    def __on_press(self, key):
        """A method which is called whenever user presses a key. It checks type of typing key and call other functions,
         whenever defined trigger happens."""
        self.__pressed_keys.append(key)
        if self.__previous_key in Combinations.END_KEYS and key in Combinations.END_KEYS:
            self.__is_finished()

        elif ((key in Combinations.SENTENCE_END_KEYS) or (key in Combinations.NEW_CONTEXT_KEYS)
              or (self.__left_button_mouse_is_pressed) or (
                      hasattr(key, 'char') and key.char in Combinations.SENTENCE_END_KEYS)) \
                and len(self.__sentence) > 0:
            self.__on_finished_context()

        elif key == keyboard.Key.delete and self.__sentence and self.__position != 0:
            self.__delete_chars()

        elif key == keyboard.Key.backspace and self.__sentence:
            self.__backspace_chars()

        elif key == keyboard.Key.left and abs(self.__position) <= len(self.__sentence):
            self.__position -= 1

        elif key == keyboard.Key.right and self.__position < 0:
            self.__position += 1

        elif (hasattr(key, 'char') and key.char is not None and len(key.char) < 2) or key in Combinations.NUMPAD_NUMBERS_KEYS or key == keyboard.Key.space:
            self.__insert_key(key)
        self.__previous_key = key
        self.__left_button_mouse_is_pressed = False
        self.__pressed_keys.clear()
        self.__non_printable_digraphs.clear()

    def __on_finished_context(self):
        pass

    def __is_finished(self):
        # if self.__sentence:
        #     self.__on_finished_context(at_the_end=True)
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

    def __delete_chars(self):
        """A method which is called whenever user presses 'delete' key to delete chars from current writting sentence"""
        if self.__position < -1:
            self.__sentence = self.__sentence[:self.__position] + self.__sentence[self.__position + 1:]
        elif self.__position == -1:
            self.__sentence = self.__sentence[:-1]
        self.__position += 1

    def __backspace_chars(self):
        """A Method which is called whenever user presses 'backspace' key to delete chars from sentence """
        if self.__position == 0:
            self.__sentence = self.__sentence[:-1]
        elif self.__position < 0:
            self.__sentence = self.__sentence[:self.__position - 1] + self.__sentence[self.__position:]

    def __insert_key(self, key):
        char = ''
        if hasattr(key, 'char') and key.char is not None and len(key.char) < 2:
            char = key.char
        elif key in Combinations.NUMPAD_NUMBERS_KEYS or key == keyboard.Key.space:
            char = key._value_.char
        if char is not None and char.isprintable():
            if self.__position == 0:
                self.__sentence += char
            else:
                self.__sentence = self.__sentence[:self.__position] + char + self.__sentence[self.__position:]
'''
    # def __on_finished_context(self, at_the_end=False):
    #     """ Method that checks add list of words to file whenever the NEW_CONTEXT_KEYS or  combination is entered."""
    #     if search('[0-9a-zA-Z]', self.__sentence):
    #         if self.__position == 0:
    #             self.__list_of_words = SFExtractor.ListOfWords(self.__sentence)
    #             if self.__list_of_words.all_words:
    #                 SFExtractor.write_object_to_json_file(self.destination_json_file_path, 'Sentence',
    #                                                       SFExtractor.object_to_dicts(self.__list_of_words))
    #             self.__sentence = ''
    #         else:
    #             self.__list_of_words = SFExtractor.ListOfWords(self.__sentence[:self.__position])
    #             if self.__left_button_mouse_is_pressed:
    #                 self.__list_of_words.set_left_click()
    #                 self.__list_of_words = None
    #
    #             SFExtractor.write_object_to_json_file(self.destination_json_file_path, 'Sentence',
    #                                                   SFExtractor.object_to_dicts(self.__list_of_words))
    #             if self.__left_button_mouse_is_pressed or at_the_end:
    #                 self.__list_of_words = SFExtractor.ListOfWords(self.__sentence[self.__position:])
    #                 if self.__left_button_mouse_is_pressed:
    #                     self.__list_of_words.set_left_click()
    #                 if self.__list_of_words.all_words:
    #                     SFExtractor.write_object_to_json_file(self.destination_json_file_path, 'Sentence',
    #                                                           SFExtractor.object_to_dicts(self.__list_of_words))
    #
    #                 self.__list_of_words = None
    #                 self.__sentence = ''
    #                 self.__position = 0
    #             else:
    #                 self.__sentence = self.__sentence[self.__position:]
    #     self.__list_of_words = None
    #
    # def __is_finished(self):
    #     """A method that checks if the END KEY COMBINATION is clicked by user """
    #     SFExtractor.add_simple_dict_to_json_file(self.destination_json_file_path, 'Keys', self.__keys_counter)
    #     SFExtractor.add_simple_dict_to_json_file(self.destination_json_file_path, 'No printable keys',
    #                                              self.__non_printable_counter)
    #     if self.__sentence:
    #         self.__on_finished_context(at_the_end=True)
    #     self.mouse_listener.stop()
    #     self.keyboard_listener.stop()
