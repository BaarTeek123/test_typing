import json
import time
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config as KivyConfig
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from Config import config
from FileWatcher import FileWatcher
from RealTimeListener import RealTimeKeyListener
from utils import generate_sentence

KivyConfig.set('graphics', 'width', config.WIDTH)
KivyConfig.set('graphics', 'height', config.HEIGHT)
KivyConfig.write()

class TypingTestApp(App):
    """
    A Kivy application for typing test, which measures typing user.
    """

    def __init__(self, username: str):
        super().__init__()
        self.username = username
        self.start_time = None
        self.target_sentence = None
        self.key_listener = None
        self.input_text = None
        self.sentence_label = None
        self.app_gathered_characters = []
        self.popup = None

    def build(self):
        """Builds the application layout."""
        self.start_time = time.time()
        self.target_sentence = self._generate_new_sentence()
        self.key_listener = RealTimeKeyListener()
        self.root = self._create_layout()
        self.input_text.bind(text=self.on_input_text_change)
        Window.bind(on_resize=self._adjust_font_size)
        Clock.schedule_interval(self._check_time_limit, 1)
        return self.root

    def _create_layout(self):
        """Creates and returns the main layout for the app."""
        layout = BoxLayout(orientation='vertical', padding=5, spacing=10)

        self.sentence_label = self._create_readonly_text_input(self.target_sentence)
        self.input_text = self._create_editable_text_input()
        self.submit_button = self._create_button("Submit", self._submit)
        close_button = self._create_button("Close", lambda x: self._confirm_quit())

        for widget in [self.sentence_label, self.input_text, self.submit_button, close_button]:
            layout.add_widget(widget)

        return layout
    @staticmethod
    def _create_readonly_text_input(text):
        """Creates a readonly TextInput widget."""
        return TextInput(text=text, size_hint=(1, 0.4), multiline=True,
                         readonly=True, font_size='16sp')

    @staticmethod
    def _create_editable_text_input():
        """Creates an editable TextInput widget."""
        return NoPasteTextInput(multiline=True, size_hint=(1, 0.4), font_size='16sp')
        # return TextInput(multiline=True, size_hint=(1, 0.4), font_size='16sp')

    @staticmethod
    def _create_button(text, callback):
        """Creates a Button widget."""
        button = Button(text=text, size_hint=(1, 0.1), font_size='16sp')
        button.bind(on_press=callback)
        return button

    def on_input_text_change(self, instance, value):
        """Handles text changes in the input_text widget."""
        if len(self.app_gathered_characters) == len(self.target_sentence.replace(" ", "")):
            self._ask_confirmation(value)

    def _submit(self, instance):
        """Handles submit button press."""
        self._ask_confirmation(self.input_text.text.strip())

    def _ask_confirmation(self, input_sentence, quit=False):
        """Asks the user for confirmation to submit or quit."""
        content = BoxLayout(orientation='vertical')
        message = f"Are you sure you want to {'quit' if quit else 'submit'}?"
        content.add_widget(Label(text=message))

        btn_layout = BoxLayout(size_hint_y=None, height='50sp', spacing=5)
        yes_btn = Button(text="Yes", on_press=lambda x: self._finalize_submission(input_sentence, quit))
        no_btn = Button(text="No", on_press=lambda x: self.dismiss_popup())
        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)

        content.add_widget(btn_layout)
        self.popup = Popup(title="Confirmation", content=content, size_hint=(None, None), size=(400, 200))
        self.popup.open()

    def _adjust_font_size(self, instance, width, height):
        """Adjusts font sizes dynamically based on window size."""
        new_font_size = max(0.02 * height, 16)
        for widget in [self.sentence_label, self.input_text, self.submit_button]:
            widget.font_size = f'{new_font_size}sp'

    def _finalize_submission(self, input_sentence, quit=False):
        """Finalizes the submission or quit process."""
        self.dismiss_popup()
        self._process_submission(input_sentence)
        if quit:
            self.stop()

    def _process_submission(self, input_sentence):
        """Processes the submission by the user."""
        elapsed_time = time.time() - self.start_time
        results = {
            "user": self.username,
            "original_sentence": self.target_sentence,
            "input_sentence": input_sentence,
            "typed_sentence": self.key_listener.get_sentence(),
            "typed_characters": self.key_listener.get_pressed_keys(),
            "elapsed_time": elapsed_time,
        }
        self._write_results_to_file(results)
        self._show_results(self._calculate_metrics(input_sentence))
        self._reset_test()

    def dismiss_popup(self):
        """Dismisses the current popup."""
        if self.popup:
            self.popup.dismiss()

    def _confirm_quit(self):
        """Confirms with the user before quitting."""
        self._ask_confirmation(None, quit=True)

    def _write_results_to_file(self, result: dict) -> None:
        """Writes the results to a file."""
        try:
            with open(config.OUT_PATH / f"{config.USERNAME}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json", mode='w+') as f:
                json.dump(result, f)
        except IOError as e:
            config.LOGGER.error(f"File write error: {e}")

    def _generate_new_sentence(self) -> str:
        """Generates a new sentence for the typing test."""
        try:
            return generate_sentence(config.SENTENCES_FILE)
        except Exception as e:
            config.LOGGER.error(f"Error generating new sentence: {e}")

    def _reset_test(self) -> None:
        """Resets the test for a new attempt."""
        # Implementation for resetting the test
        self.start_time = time.time()
        self.target_sentence = self._generate_new_sentence()
        self.sentence_label.text = self.target_sentence
        self.input_text.text = ""
        self.app_gathered_characters = []
        self.key_listener.clean_up()
        Clock.schedule_once(lambda dt: setattr(self.input_text, 'focus', True), 0.5)


    def _check_time_limit(self, dt):
        """Checks if the typing duration has exceeded 2 minutes."""
        if time.time() - self.start_time > 120:  # 2 minutes in seconds
            self._reset_test_with_prompt()

    def _reset_test_with_prompt(self):
        """Resets the test with a prompt to the user."""
        self.dismiss_popup()  # Ensure any existing popup is closed
        self.popup = Popup(title="Time Limit Exceeded",
                           content=Label(text="2 minutes exceeded, restarting test."),
                           size_hint=(None, None), size=(400, 200),
                           auto_dismiss=True)
        self.popup.open()
        self._reset_test()

    def _calculate_metrics(self, input_sentence):
        """Calculates typing accuracy and words per minute."""
        time_elapsed = time.time() - self.start_time
        words_typed = len(input_sentence.split())
        total_words = len(self.target_sentence.split())
        correct_chars = sum(1 for inp, target in zip(input_sentence, self.target_sentence) if inp == target)
        accuracy = (correct_chars / max(len(self.target_sentence), 1)) * 100
        wpm = (words_typed / (time_elapsed / 60)) if time_elapsed > 0 else 0

        return {
            "accuracy": accuracy,
            "words_per_minute": wpm,
            "time_elapsed": time_elapsed,
            "total_words": total_words
        }

    def _show_results(self, results):
        """Displays the typing test results in a popup."""
        content = BoxLayout(orientation='vertical')
        message = f"Results:\nAccuracy: {results['accuracy']:.2f}%\nTime: {results['time_elapsed']:.2f} seconds"
        content.add_widget(Label(text=message))

        close_btn = Button(text="Close", on_press=lambda x: self.dismiss_popup())
        content.add_widget(close_btn)

        self.popup = Popup(title="Test Results", content=content, size_hint=(None, None), size=(400, 250))
        self.popup.open()


if __name__ == '__main__':
    # initial_prompt_app = InitialPromptApp()
    # initial_prompt_app.run()
    # username_app = UsernameInputApp()
    # username_app.run()
    #
    # if username_app.username != config.DEFAULT_USERNAME and len(username_app.username) > 2:
    #     config.DEFAULT_USERNAME = username_app.username
    #     config.save_to_json()

    # typing_test_app = TypingTestApp(username=username_app.username)
    file_watcher = FileWatcher("127.0.0.1", config.OUT_PATH)
    file_watcher.start()
    typing_test_app = TypingTestApp(username="Bartek")
    typing_test_app.run()


