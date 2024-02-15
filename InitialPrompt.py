from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.app import App
from kivy.metrics import sp

class InitialPromptApp(App):
    def __init__(self, message: str, **kwargs):
        super().__init__(**kwargs)
        self.message = message

    def build(self):
        self._show_initial_prompt()

    def _show_initial_prompt(self):
        content = BoxLayout(orientation='vertical')

        # Enable text wrapping for the label
        message_label = Label(text=self.message, size_hint_y=None, valign="top")
        message_label.bind(width=lambda *x: message_label.setter('text_size')(message_label, (message_label.width, None)),
                           texture_size=lambda *x: self._adjust_popup_size(message_label))

        content.add_widget(message_label)

        btn_layout = BoxLayout(size_hint_y=None, height='50sp', spacing=5)
        agree_btn = Button(text="Agree", on_press=self._on_agree)
        disagree_btn = Button(text="Disagree", on_press=self._on_disagree)
        btn_layout.add_widget(agree_btn)
        btn_layout.add_widget(disagree_btn)

        content.add_widget(btn_layout)
        self.initial_popup = Popup(title="Confirmation", content=content, size_hint=(None, None), size=(400, 200))
        self.initial_popup.open()

    def _adjust_popup_size(self, label):
        # Adjust the popup size based on the message label size
        if label.texture_size[1] > 0:  # Ensure the texture size is calculated
            total_height = label.texture_size[1] + sp(100)  # Add some padding and space for buttons
            self.initial_popup.size = (400, total_height)

    def _on_agree(self, instance):
        self.initial_popup.dismiss()
        self.stop()

    def _on_disagree(self, instance):
        self.initial_popup.dismiss()
        self.stop()
        quit(0)