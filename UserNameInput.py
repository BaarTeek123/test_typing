from uuid import uuid4

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from Config import config, EnglishLanguageLevel



class UserInformationApp(App):

    def __init__(self):
        super(UserInformationApp, self).__init__()
        self.age_input = None
        self.username_input = None
        self.language_level_spinner = None
        self.username = config.USERNAME
        self.language_level = config.LANGUAGE_LEVEL
        self.age = config.AGE

    def build(self):
        self.title = 'User Information'
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Labels with formatting and text wrapping
        welcome_label = Label(
            text=f"Hello [b][color=5bcefa]{self.username}[/color][/b]. \n"
                 f"Your age is set to [b][color=5bcefa]{self.age}[/color][/b] and "
                 f"language proficiency level is set to [b][color=5bcefa]{self.language_level}[/color][/b]",
            size_hint=(1, None),
            halign="center",
            valign="top",
            font_size='18sp',
            markup=True
        )

        instruction_part1 = Label(text="Would you like to update your information?", height=50,
                                  size_hint=(1, None), halign="center")
        instruction_part1.font_size = '18sp'

        instruction_part2 = Label(text="Remember! \nChanging it will treat you as a new user.", height=50,
                                  size_hint=(1, None), halign="center", color=(1, 0, 0, 1))
        instruction_part2.font_size = '18sp'

        # Text inputs
        self.username_input = TextInput(
            size_hint=(1, None),
            height=50,
            multiline=False,
            font_size='18sp',
            halign='center',
            hint_text="Enter new username (min. 3, max. 60 characters)"
        )
        self.username_input.bind(on_text_validate=self.limit_username_length)

        self.age_input = TextInput(
            size_hint=(1, None),
            height=50,
            multiline=False,
            font_size='18sp',
            halign="center",
            input_filter=self.age_input_filter,
            hint_text="Enter age"
        )
        self.age_input.bind(text=self.validate_age_input)

        # Spinner
        language_levels = [level.value for level in EnglishLanguageLevel]
        self.language_level_spinner = Spinner(
            text='Select Language Level',
            values=language_levels,
            size_hint=(1, None),
            height=50,
            font_size='18sp',
            background_color=(0.357, 0.808, 0.980, 1)
        )

        skip_button = Button(
            text="Skip Update",
            size_hint=(0.5, 1),
            height=50,
            font_size='18sp',
            on_press=self.skip_update,
            background_color=(0.878, 0.066, 0.372, 1)
        )

        # Submit button
        submit_button = Button(
            text="Update Information",
            size_hint=(0.5, 1),
            height=50,
            font_size='18sp',
            on_press=self.attempt_submit,
            background_color=(0.314, 0.784, 0.471, 1)

        )


        buttons_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=50)
        buttons_layout.add_widget(skip_button)
        buttons_layout.add_widget(submit_button)

        for widget in [welcome_label, instruction_part1, instruction_part2, Widget(size_hint_y=0.05) , self.username_input, self.age_input,
                       self.language_level_spinner, Widget(size_hint_y=0.05), buttons_layout]:
            main_layout.add_widget(widget)

        return main_layout

    def skip_update(self, instance):
        self.show_popup("Configuration", f"No changes made. \nUsername: [color=5bcefa]{config.USERNAME}[/color]"
                                         f"\nAge: [color=5bcefa]{config.AGE}[/color]\n"
                                         f"Language Level: [color=5bcefa]{config.LANGUAGE_LEVEL}[/color]", if_close=True)
    def submit_user(self, instance=None):
        self.username = self.username_input.text.strip()
        self.age = self.age_input.text.strip()
        self.language_level = self.language_level_spinner.text

        if len(self.username) >= 3 and len(self.age) > 0:
            config.LANGUAGE_LEVEL = self._parse_language_level(self.language_level)
            config.USERNAME = self.username
            config.AGE = self._parse_age(self.age)
            config.DEFAULT_USERNAME = str(uuid4())
            config.save_to_json()
            self.show_popup("Configuration", f"Your information has been updated successfully. \nUsername: [color=5bcefa]{config.USERNAME}[/color]"
                                         f"\nAge: [color=5bcefa]{config.AGE}[/color]\n"
                                         f"Language Level: [color=5bcefa]{config.LANGUAGE_LEVEL}[/color]", if_close=True)
        self.skip_update(None)


    @staticmethod
    def _parse_language_level(input_str):
        """Parse and validate the language level input."""
        try:
            return EnglishLanguageLevel[input_str].value
        except KeyError:
            return EnglishLanguageLevel.NA.value

    @staticmethod
    def _parse_age(input_str):
        """Parse and validate the language level input."""
        try:
            return int(input_str)
        except TypeError:
            return -1

    @staticmethod
    def limit_username_length(instance):
        if len(instance.text) > 60:
            instance.text = instance[:60]

    @staticmethod
    def age_input_filter(value, from_undo):
        return value if value.isdigit() and 0 <= int(value) <= 100 else ''

    @staticmethod
    def validate_age_input(instance, value):
        if value:
            instance.text = str(min(100, max(0, int(value))))

    def attempt_submit(self, instance):
        username_condition = len(self.username_input.text.strip()) > 3
        age_condition = self.age_input.text.strip()
        language_level_condition = self.language_level_spinner.text not in ['Select Language Level', 'Not provided']

        fields_filled = sum(bool(field) for field in [username_condition, age_condition, language_level_condition])

        if 0 < fields_filled < 3:
            message = "Please ensure all fields are filled:\n\n"
            if not username_condition:
                message += "- Username is required.\n"
            if not age_condition:
                message += "- Age is required.\n"
            if not language_level_condition:
                message += "- Please select your language level."

            self.show_popup("Incomplete Submission", message)
        else:
            self.submit_user()


    def show_popup(self, title, message, if_close = False):
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text=message, font_size='18sp', markup=True))
        close_btn = Button(text='Close', size_hint=(1, None), height=50, font_size='18sp')
        popup = Popup(title=title, content=content, size_hint=(None, None), size=config.POPUP_SIZE,
                      auto_dismiss=False)
        if if_close:
            close_btn.bind(on_press=self.stop)
        else:
            close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()


if __name__ == '__main__':
    user_information_app = UserInformationApp()
    user_information_app.run()
