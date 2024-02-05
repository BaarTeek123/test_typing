import json
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.config import Config as KivyConfig
from kivy.core.window import Window

from Config import config
from RealTimeListener import RealTimeKeyListener
from UserNameInput import UsernameInputApp
from utils import generate_sentence

#
# # Dynamically set the application window size
KivyConfig.set('graphics', 'width', config.WIDTH)
KivyConfig.set('graphics', 'height', config.HEIGHT)
KivyConfig.write()


class TypingTestApp(App):

    def __init__(self, username: str):
        super().__init__()
        self.input_text = None
        self.sentence_label = None
        self.key_listener = None
        self.target_sentence = None
        self.start_time = None
        self.user_name = None
        self.app_gathered_characters = []
        self.user_name: str = username

    def build(self):
        self.start_time = time.time()
        self.target_sentence = self. _generate_new_sentence()
        self.key_listener = RealTimeKeyListener()
        self.root = BoxLayout(orientation='vertical', padding=5, spacing=10)

        self.sentence_label = TextInput(text=self.target_sentence, size_hint=(1, 0.4), multiline=True,
                                        readonly=True, font_size='16sp')
        self.input_text = TextInput(multiline=True, size_hint=(1, 0.4), font_size='16sp')

        self.submit_button = Button(text="Submit", size_hint=(1, 0.1), font_size='16sp')
        self.submit_button.bind(on_press=self.submit)

        # Adding a Close button
        self.close_button = Button(text="Close", size_hint=(1, 0.1), font_size='16sp')
        self.close_button.bind(on_press=self.close_app)

        self.root.add_widget(self.sentence_label)
        self.root.add_widget(self.input_text)
        self.root.add_widget(self.submit_button)
        self.root.add_widget(self.close_button)
        self.input_text.bind(text=self.on_input_text_change)
        # Bind to window resize event to dynamically adjust font sizes
        Window.bind(on_resize=self._adjust_font_size)

        return self.root

    def on_input_text_change(self, instance, value):
        if len(self.app_gathered_characters) == len(self.target_sentence.replace(" ", "")):
            self.ask_confirmation(value)

    def submit(self, instance=None, quit=False) -> None:
        input_sentence = self.input_text.text.strip()
        if not quit:
            self.ask_confirmation(input_sentence, quit=False)


    def ask_confirmation(self, input_sentence, quit=False):
        content = BoxLayout(orientation='vertical')
        message = Label(text=f"Are you sure you want to {'quit' if quit else 'submit'}?")
        content.add_widget(message)

        btn_layout = BoxLayout(size_hint_y=None, height='50sp', spacing=5)
        yes_btn = Button(text="Yes", on_press=lambda x: self.finalize_submission(input_sentence))
        no_btn = Button(text="No", on_press=lambda x: self.dismiss_popup())
        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)

        content.add_widget(btn_layout)
        self.popup = Popup(title="Confirmation", content=content, size_hint=(None, None), size=(400, 200))
        self.popup.open()

    def _adjust_font_size(self, instance, width, height):
        new_font_size = max(0.02 * height, 16)
        self.sentence_label.font_size = f'{new_font_size}sp'
        self.input_text.font_size = f'{new_font_size}sp'
        self.submit_button.font_size = f'{new_font_size}sp'

    def on_key_press(self, instance, value) -> None:
        try:
            self.app_gathered_characters.append(value)
        except Exception as e:
            Logger.error(f"Error capturing key press: {e}")

    def finalize_submission(self, input_sentence):
        self.popup.dismiss()  # Dismiss the popup first
        try:
            result = {
                "user": self.user_name,
                "original sentence": self.target_sentence,
                "input sentence": input_sentence if len(input_sentence) > 0.5 * len(input_sentence) else None,
                "listener sentence": self.key_listener.get_sentence(),
                "typed characters": self.key_listener.get_pressed_keys(),
            }
            if None in result.values():
                raise Exception("No text input")
            self._write_results_to_file(result)
            self._reset_test()
        except Exception as e:
            Logger.error(f"Error finishing test: {e}")

    def dismiss_popup(self):
        self.popup.dismiss()

    def close_app(self, instance):
        self.submit(quit=True)
        App.get_running_app().stop()

    def _write_results_to_file(self, result: dict) -> None:
        try:
            with open(config.OUTPUT_FILE, mode='w+') as f:
                json.dump(result, f)
        except IOError as e:
            Logger.error(f"File write error: {e}")

    def _generate_new_sentence(self) -> str:
        try:
            return generate_sentence(config.SENTENCES_FILE)
        except Exception as e:
            Logger.error(f"Error generating new sentence: {e}")
            return "Error: Could not generate sentence."

    def _reset_test(self) -> None:
        self.start_time = time.time()
        self.target_sentence = self._generate_new_sentence()
        self.sentence_label.text = self.target_sentence
        self.input_text.text = ""
        self.app_gathered_characters = []
        self.key_listener.clean_up()
        Clock.schedule_once(lambda dt: setattr(self.input_text, 'focus', True), 0.5)


if __name__ == '__main__':
    username_app = UsernameInputApp()
    username_app.run()

    if username_app.username != config.DEFAULT_USERNAME and len(username_app.username) > 0:
        config.DEFAULT_USERNAME = username_app.username
        config.save_to_json()

    typing_test_app = TypingTestApp(username=username_app.username)
    typing_test_app.run()
