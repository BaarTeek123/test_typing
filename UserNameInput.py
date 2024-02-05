from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

from Config import config


class UsernameInputApp(App):
    def build(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        label = Label(text=f"Enter your username", size_hint=(1, None), height=50, halign="center", valign="top")
        label.bind(size=label.setter('text_size'))  # Bind size to automatically adjust text wrapping
        label.font_size = '20sp'  # Increase font size

        current_name_label = Label(text=f"(current name is: {config.DEFAULT_USERNAME})", size_hint=(1, None), height=50,
                                   halign="center", valign="middle")
        current_name_label.bind(size=current_name_label.setter('text_size'))
        current_name_label.font_size = '12sp'  # Increase font size

        # TextInput with centered text, increased font size, and confirming with Enter
        self.username_input = TextInput(size_hint=(1, None), height=50, multiline=False, font_size='20sp',
                                        halign='center')
        self.username_input.bind(on_text_validate=self.submit_username)  # Confirm with Enter
        self.username_input.bind(focus=self.on_focus)  # Adjust alignment when focused

        content.add_widget(label)
        content.add_widget(current_name_label)
        content.add_widget(self.username_input)

        submit_button = Button(text="Submit", size_hint=(1, None), height=50, font_size='20sp')
        submit_button.bind(on_press=self.submit_username)
        content.add_widget(submit_button)

        return content

    def submit_username(self, instance):
        self.username = self.username_input.text.strip()
        self.stop()  # Close the username collection window

    def on_focus(self, instance, value):
        if value:  # When the text input is focused, ensure text is properly aligned
            instance.do_cursor_movement('cursor_home')
