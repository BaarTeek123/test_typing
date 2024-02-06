import pynput.keyboard as keyboard
import pynput.mouse as mouse
from typing import List, Optional

from Config import Config


class Combinations:
    """A class which includes key combinations or sets of keys."""
    END_KEYS = {keyboard.Key.esc, keyboard.Key.f4}  # key combination to finish listening
    NEXT_WORD_KEYS = {keyboard.Key.space, ':', ",", "/", '"'}  # key of next words
    NEW_CONTEXT_KEYS = {}
    CONTEXT_END = {keyboard.Key.enter}
    NUMPAD_NUMBERS_KEYS = {}


class RealTimeKeyListener:
    """
       A class to listen to real-time keyboard and mouse events, processing them to manage a sentence construction.

       Attributes:
           __position (int): The current cursor position within the sentence.
           __previous_key (Optional[keyboard.Key]): The last pressed key.
           __sentence (str): The current accumulated sentence.
           __pressed_keys (List[str]): A list of pressed keys and mouse buttons.
       """
    __position: int = 0
    __previous_key: Optional[keyboard.Key] = None
    __sentence: str = ""
    __pressed_keys: List[str] = []

    def __init__(self):
        """Initializes the RealTimeKeyListener with keyboard and mouse listeners."""
        self.keyboard_listener = keyboard.Listener(on_press=self._on_press)
        self.mouse_listener = mouse.Listener(on_click=self._on_click)
        self.keyboard_listener.start()
        self.mouse_listener.start()
        Config.LOGGER.info("RealTimeKeyListener initialized and listeners started.")

    def get_sentence(self) -> str:
        """Returns the currently constructed sentence."""
        return self.__sentence

    def get_pressed_keys(self) -> list:
        """Returns the currently pressed keys."""
        return self.__pressed_keys

    def _on_click(self, x: int, y: int, button: mouse.Button, pressed: bool) -> None:
        """
        Callback function for mouse click events.

            Args:
                x (int): The x-coordinate of the mouse position (unused -> necessary for compatibility)
                y (int): The y-coordinate of the mouse position (unused -> necessary for compatibility)
                (mouse.Button): The mouse button that was pressed or released.
                pressed (bool): True if the button was pressed, False if released.
        """
        self.__pressed_keys.append(str(button))
        Config.LOGGER.debug(f"Mouse button {button} {'pressed' if pressed else 'released'} at ({x}, {y}).")
        if pressed and button == mouse.Button.left:
            Config.LOGGER.info("Left mouse button pressed.")
            self._left_button_mouse_is_pressed = True

    def _on_press(self, key) -> None:
        """Callback function for keyboard press events."""

        self.__pressed_keys.append(str(key))
        Config.LOGGER.debug(f"Key {key} pressed.")
        if key == keyboard.Key.delete and self.__sentence and self.__position != 0:
            self._delete_or_backspace_chars(delete=True)

        elif key == keyboard.Key.backspace and self.__sentence:
            self._delete_or_backspace_chars(delete=False)

        elif key == keyboard.Key.left and abs(self.__position) <= len(self.__sentence):
            self.__position -= 1

        elif key == keyboard.Key.right and self.__position < 0:
            self.__position += 1

        elif (hasattr(key, 'char') and key.char is not None and len(
                key.char) < 2) or key in Combinations.NUMPAD_NUMBERS_KEYS or key == keyboard.Key.space:
            self._insert_char(key)
        self.__previous_key = key
        self._left_button_mouse_is_pressed = False

    def clean_up(self) -> None:
        """Cleans up resources and resets the internal state when finished with the listener."""
        self.__pressed_keys.clear()
        self.__sentence = ''
        Config.LOGGER.info("Resetting state.")

    def finish_listening(self) -> None:
        """Stops the mouse and keyboard listeners, effectively ending the session."""
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        Config.LOGGER.info("Listeners stopped.")

    def _delete_or_backspace_chars(self, delete: bool) -> None:
        """Deletes or backspaces characters in the sentence based on the cursor position."""
        if delete and self.__position < -1:
            self.__sentence = self.__sentence[:self.__position] + self.__sentence[self.__position + 1:]
        elif delete and self.__position == -1:
            self.__sentence = self.__sentence[:-1]
        elif not delete and self.__position == 0:
            self.__sentence = self.__sentence[:-1]
        elif not delete and self.__position < 0:
            self.__sentence = self.__sentence[:self.__position - 1] + self.__sentence[self.__position:]
        self.__position = min(self.__position + 1, 0) if delete else self.__position
        Config.LOGGER.debug(f"{'Deleting' if delete else 'Backspacing'} character at position {self.__position}.")

    def _insert_char(self, key: str) -> None:
        """Inserts a character into the sentence at the current cursor position."""
        Config.LOGGER.debug(f"Inserting character '{key}' at position {self.__position}.")
        char = key.char if hasattr(key, 'char') and key.char else ''
        if key in Combinations.NUMPAD_NUMBERS_KEYS or key == keyboard.Key.space:
            char = key._value_.char
        if char and char.isprintable():
            if self.__position == 0:
                self.__sentence += char
            else:
                self.__sentence = self.__sentence[:self.__position] + char + self.__sentence[self.__position:]


# import json
# import time
# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
# from kivy.uix.popup import Popup
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button
# from kivy.clock import Clock
# from kivy.logger import Logger
# from kivy.config import Config as KivyConfig
# from kivy.core.window import Window
#
# from Config import config
# from RealTimeListener import RealTimeKeyListener
# from UserNameInput import UsernameInputApp
# from utils import generate_sentence
#
# #
# # # Dynamically set the application window size
# KivyConfig.set('graphics', 'width', config.WIDTH)
# KivyConfig.set('graphics', 'height', config.HEIGHT)
# KivyConfig.write()
#
#
# class TypingTestApp(App):
#
#     def __init__(self, username: str):
#         super().__init__()
#         self.input_text = None
#         self.sentence_label = None
#         self.key_listener = None
#         self.target_sentence = None
#         self.start_time = None
#         self.user_name = None
#         self.app_gathered_characters = []
#         self.user_name: str = username
#
#     def build(self):
#         self.start_time = time.time()
#         self.target_sentence = self. _generate_new_sentence()
#         self.key_listener = RealTimeKeyListener()
#         self.root = BoxLayout(orientation='vertical', padding=5, spacing=10)
#
#         self.sentence_label = TextInput(text=self.target_sentence, size_hint=(1, 0.4), multiline=True,
#                                         readonly=True, font_size='16sp')
#         self.input_text = TextInput(multiline=True, size_hint=(1, 0.4), font_size='16sp')
#
#         self.submit_button = Button(text="Submit", size_hint=(1, 0.1), font_size='16sp')
#         self.submit_button.bind(on_press=self.submit)
#
#         # Adding a Close button
#         self.close_button = Button(text="Close", size_hint=(1, 0.1), font_size='16sp')
#         self.close_button.bind(on_press=self.close_app)
#
#         self.root.add_widget(self.sentence_label)
#         self.root.add_widget(self.input_text)
#         self.root.add_widget(self.submit_button)
#         self.root.add_widget(self.close_button)
#         self.input_text.bind(text=self.on_input_text_change)
#         # Bind to window resize event to dynamically adjust font sizes
#         Window.bind(on_resize=self._adjust_font_size)
#
#         return self.root
#
#     def on_input_text_change(self, instance, value):
#         if len(self.app_gathered_characters) == len(self.target_sentence.replace(" ", "")):
#             self.ask_confirmation(value)
#
#     def submit(self, instance=None, quit=False) -> None:
#         input_sentence = self.input_text.text.strip()
#         if not quit:
#             self.ask_confirmation(input_sentence, quit=False)
#
#
#     def ask_confirmation(self, input_sentence, quit=False):
#         content = BoxLayout(orientation='vertical')
#         message = Label(text=f"Are you sure you want to {'quit' if quit else 'submit'}?")
#         content.add_widget(message)
#
#         btn_layout = BoxLayout(size_hint_y=None, height='50sp', spacing=5)
#         yes_btn = Button(text="Yes", on_press=lambda x: self.finalize_submission(input_sentence, quit))
#         no_btn = Button(text="No", on_press=lambda x: self.dismiss_popup())
#         btn_layout.add_widget(yes_btn)
#         btn_layout.add_widget(no_btn)
#
#         content.add_widget(btn_layout)
#         self.popup = Popup(title="Confirmation", content=content, size_hint=(None, None), size=(400, 200))
#         self.popup.open()
#
#     def _adjust_font_size(self, instance, width, height):
#         new_font_size = max(0.02 * height, 16)
#         self.sentence_label.font_size = f'{new_font_size}sp'
#         self.input_text.font_size = f'{new_font_size}sp'
#         self.submit_button.font_size = f'{new_font_size}sp'
#
#     def on_key_press(self, instance, value) -> None:
#         try:
#             self.app_gathered_characters.append(value)
#         except Exception as e:
#             Logger.error(f"Error capturing key press: {e}")
#
#     def finalize_submission(self, input_sentence, quit=False):
#         self.popup.dismiss()  # Dismiss the popup first
#         try:
#             result = {
#                 "user": self.user_name,
#                 "original sentence": self.target_sentence,
#                 "input sentence": input_sentence if len(input_sentence) > 0.5 * len(input_sentence) else None,
#                 "listener sentence": self.key_listener.get_sentence(),
#                 "typed characters": self.key_listener.get_pressed_keys(),
#             }
#             if None in result.values():
#                 raise Exception("No text input")
#             self._write_results_to_file(result)
#             if quit:
#                 self.close_app(None)
#
#             self._reset_test()
#         except Exception as e:
#             Logger.error(f"Error finishing test: {e}")
#
#     def dismiss_popup(self):
#         self.popup.dismiss()
#
#     def close_app(self, instance):
#         self.ask_confirmation(None, quit=True)
#
#         App.get_running_app().stop()
#
#     def _write_results_to_file(self, result: dict) -> None:
#         try:
#             with open(config.OUTPUT_FILE, mode='w+') as f:
#                 json.dump(result, f)
#         except IOError as e:
#             Logger.error(f"File write error: {e}")
#
#     def _generate_new_sentence(self) -> str:
#         try:
#             return generate_sentence(config.SENTENCES_FILE)
#         except Exception as e:
#             Logger.error(f"Error generating new sentence: {e}")
#             return "Error: Could not generate sentence."
#
#     def _reset_test(self) -> None:
#         self.start_time = time.time()
#         self.target_sentence = self._generate_new_sentence()
#         self.sentence_label.text = self.target_sentence
#         self.input_text.text = ""
#         self.app_gathered_characters = []
#         self.key_listener.clean_up()
#         Clock.schedule_once(lambda dt: setattr(self.input_text, 'focus', True), 0.5)
#
#
