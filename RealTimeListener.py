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

