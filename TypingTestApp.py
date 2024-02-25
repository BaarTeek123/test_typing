import json
import time
from datetime import datetime
from os.path import join

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
from InitialPrompt import GDPRClause
from RealTimeListener import RealTimeKeyListener
from UserNameInput import UserInformationApp
from utils import generate_sentence, NoPasteTextInput
from Levenshtein import distance



KivyConfig.set('graphics', 'width', config.WIDTH)
KivyConfig.set('graphics', 'height', config.HEIGHT)
KivyConfig.write()


class TypingTestApp(App):
    """
    A Kivy application for typing test, which measures typing user.
    """

    def __init__(self, username: str = None):
        super().__init__()
        self.username = username or config.USERNAME
        self.start_time = None
        self.target_sentence = None
        self.key_listener = None
        self.input_text = None
        self.sentence_label = None
        self.app_gathered_characters = []
        self.popup = None
        self.last_interaction_time = None
        self.stopped = False

    def build(self):
        """Builds the application layout."""
        self.start_time = time.time()
        self.last_interaction_time = time.time()
        self.target_sentence = self._generate_new_sentence()
        self.key_listener = RealTimeKeyListener()
        self.root = self._create_layout()
        self.input_text.bind(text=self.on_input_text_change)
        self.title='Type Me'
        Window.bind(on_resize=self._adjust_font_size)
        Clock.schedule_interval(self._check_time_limit, 1)
        return self.root

    def mail_label(self):
        return Label(
            text=f"Contact e-mail [b][color=5bcefa]{config.CONTACT_EMAIL}[/color][/b]. \n",
            size_hint=(1, None),
            halign="center",
            valign="top",
            font_size='18sp',
            markup=True
        )

    def _create_layout(self):
        """Creates and returns the main layout for the app."""
        layout = BoxLayout(orientation='vertical', padding=5, spacing=10)

        self.sentence_label = self._create_readonly_text_input(self.target_sentence)
        self.input_text = self._create_editable_text_input()
        self.input_text = self._create_editable_text_input()
        self.submit_button = self._create_button(
            "Submit",
            self._submit,
            background_color=(0.314, 0.784, 0.471, 1), size_hint=(0.5, 1)
        )
        close_button = self._create_button(
            "Close",
            lambda x: self._confirm_quit(),
            background_color=(0.878, 0.066, 0.372, 1,), size_hint=(0.5, 1)
        )
        buttons_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=50)
        buttons_layout.add_widget(self.submit_button)
        buttons_layout.add_widget(close_button)

        for widget in [self.sentence_label, self.input_text, buttons_layout, self.mail_label()]:
            layout.add_widget(widget)

        return layout

    @staticmethod
    def _create_readonly_text_input(text):
        """Creates a readonly TextInput widget."""
        return TextInput(text=text, size_hint=(1, 0.4), multiline=True,
                         readonly=True, font_size='18sp')

    @staticmethod
    def _create_editable_text_input():
        """Creates an editable TextInput widget."""
        return NoPasteTextInput(multiline=True, size_hint=(1, 0.4), font_size='18sp')
        # return TextInput(multiline=True, size_hint=(1, 0.4), font_size='16sp')

    @staticmethod
    def _create_button(text, callback, **kwargs):
        """Creates a Button widget."""
        button = Button(text=text, font_size='18sp', **kwargs)
        button.bind(on_press=callback)
        return button

    def on_input_text_change(self, instance, value):
        """Handles text changes in the input_text widget."""
        # update last interaction
        self.last_interaction_time = time.time()
        if len(value.strip()) == len(self.target_sentence):
            self._ask_confirmation(value)

    def _submit(self, instance):
        """Handles submit button press."""
        self.last_interaction_time = time.time()
        self._ask_confirmation(self.input_text.text.strip())

    def _ask_confirmation(self, input_sentence, quit=False):
        """Asks the user for confirmation to submit or quit."""
        content = BoxLayout(orientation='vertical')
        message = f"Are you sure you want to {'quit' if quit else 'submit'}?"
        content.add_widget(Label(text=message))

        btn_layout = BoxLayout(size_hint_y=None, height='50sp', spacing=5)
        yes_btn = Button(text="Yes", on_press=lambda x: self._finalize_submission(input_sentence, quit),
                         font_size='18sp', background_color=(0.314, 0.784, 0.471, 1))
        no_btn = Button(text="No", on_press=lambda x: self.dismiss_popup(),
                        font_size='18sp', background_color=(0.878, 0.066, 0.372, 1))
        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)

        content.add_widget(btn_layout)
        self.popup = Popup(
            title="Confirmation",
            content=content,
            size_hint=(None, None),
            size=(400, 200),
            auto_dismiss=False
        )
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
            "user": config.USERNAME,
            "user_uid": config.DEFAULT_USERNAME,
            "age": config.AGE,
            "language_proficiency": config.LANGUAGE_LEVEL,
            "original_sentence": self.target_sentence,
            "input_sentence": input_sentence if isinstance(input_sentence, str) else "",
            "logger_sentence": self.key_listener.get_sentence() if isinstance(self.key_listener.get_sentence(),
                                                                              str) else "",
            "logger_keys": self.key_listener.get_pressed_keys() if isinstance(self.key_listener.get_pressed_keys(),
                                                                              list) else [],
            'elapsed_time': float(elapsed_time)
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
            if len(result['input_sentence'].strip()) > len(self.target_sentence) // 3:
                with open(join(config.OUT_PATH, f"{config.USERNAME}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"),
                          mode='w+') as f:
                    json.dump(result, f)
        except IOError as e:
            config.LOGGER.error(f"File write error: {e}")

    def _generate_new_sentence(self) -> str:
        """Generates a new sentence for the typing test."""
        try:
            return generate_sentence(config.SENTENCES_FILE)
        except Exception as e:
            config.LOGGER.error(f"Error generating new sentence: {e}")
            return "Cannot provide any sentence. Something went wrong."

    def _reset_test(self) -> None:
        """Resets the test for a new attempt."""
        # Implementation for resetting the test
        self.start_time = time.time()
        self.last_interaction_time = time.time()
        self.target_sentence = self._generate_new_sentence()
        self.sentence_label.text = self.target_sentence
        self.input_text.text = ""
        self.app_gathered_characters = []
        self.key_listener.clean_up()
        Clock.schedule_once(lambda dt: setattr(self.input_text, 'focus', True), 0.5)

    def _check_time_limit(self, dt, maxtime=config.TIME_LIMIT):
        """Checks if the typing duration has exceeded 2 minutes."""
        if time.time() - self.last_interaction_time > maxtime and not self.stopped:
            self.stopped = True
            self._reset_test_with_prompt(maxtime)

    def _reset_test_with_prompt(self, maxtime):
        """Resets the test with a prompt to the user."""
        self.dismiss_popup()  # Ensure any existing popup is closed
        message_label = Label(
            text=f"{maxtime} seconds without any action exceeded, restarting test.",
            font_size='18sp',
        )
        layout = BoxLayout(orientation='vertical', spacing=10)

        def on_confirm(instance=None):
            self.popup.dismiss()  # Dismiss the popup
            self.stopped = False  # Set stopped to False
            self._reset_test()  # Call reset_test

        self._reset_test()

        confirm_btn = Button(text="Confirm", size_hint=(1, 0.2),
                             background_color=(0.314, 0.784, 0.471, 1),
                             font_size='18sp',
                             on_press=on_confirm,
                             )

        layout.add_widget(message_label)
        layout.add_widget(confirm_btn)

        self.popup = Popup(title="Time Limit Exceeded",
                           content=layout,
                           size_hint=(None, None), size=config.POPUP_SIZE,
                           auto_dismiss=True)
        self.popup.open()

    def _calculate_metrics(self, input_sentence):
        if input_sentence is None or len(input_sentence) == 0:
            return {
                "levenshtein_distance": "No text detected",
                "time_elapsed": 0.0,
            }
        time_elapsed = time.time() - self.start_time
        return {
            "levenshtein_distance": distance(input_sentence, self.target_sentence),
            "time_elapsed": round(time_elapsed, 2),
        }

    def _show_results(self, results):
        """Displays the typing test results in a popup."""
        content = BoxLayout(orientation='vertical')
        message = f"Results:\nLevenshtein distance: {results['levenshtein_distance']}\nTime: {results['time_elapsed']} seconds"
        content.add_widget(Label(text=message))

        close_btn = Button(text="Close", on_press=lambda x: self.dismiss_popup())
        content.add_widget(close_btn)

        self.popup = Popup(
            title="Test Results", content=content, size_hint=(None, None), size=(400, 250), )
        self.popup.open()


if __name__ == '__main__':
    with open(config.GDPR_CLAUSE, mode='r', encoding='utf-8') as gdpr_clause:
        gdpr_clause = gdpr_clause.read()

    initial_prompt_app = GDPRClause(gdpr_clause)
    initial_prompt_app.run()
    username_app = UserInformationApp()
    username_app.run()

    typing_test_app = TypingTestApp(username=username_app.username)
    file_watcher = FileWatcher(config.SERVER_ADDRESS, config.OUT_PATH)
    file_watcher.start()
    typing_test_app.run()
