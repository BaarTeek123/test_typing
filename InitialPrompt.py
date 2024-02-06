from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.app import App


class InitialPromptApp(App):
    def build(self):
        self._show_initial_prompt()

    def _show_initial_prompt(self):
        content = BoxLayout(orientation='vertical')
        message = "Do you agree to proceed with the typing test?"
        content.add_widget(Label(text=message))

        btn_layout = BoxLayout(size_hint_y=None, height='50sp', spacing=5)
        agree_btn = Button(text="Agree", on_press=self._on_agree)
        disagree_btn = Button(text="Disagree", on_press=self._on_disagree)
        btn_layout.add_widget(agree_btn)
        btn_layout.add_widget(disagree_btn)

        content.add_widget(btn_layout)
        self.initial_popup = Popup(title="Confirmation", content=content, size_hint=(None, None), size=(400, 200))
        self.initial_popup.open()

    def _on_agree(self, instance):
        self.initial_popup.dismiss()
        self.stop()

    def _on_disagree(self, instance):
        self.initial_popup.dismiss()
        self.stop()
        quit(0)


