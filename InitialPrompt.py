from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from kivy.config import Config as KivyConfig

from Config import config

KivyConfig.set('graphics', 'width', config.POPUP_SIZE[0])
KivyConfig.set('graphics', 'height', config.POPUP_SIZE[1])
KivyConfig.write()


class GDPRClause(App):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def build(self):
        self.title = 'Type Me'
        self._show_initial_prompt()

    def _show_initial_prompt(self):
        content = BoxLayout(orientation='vertical')

        # Scrollable view for the message
        scroll_view = ScrollView(size_hint=(1, 0.8))
        message_label = Label(text=self.message, size_hint_y=None, valign="top", halign="left", markup=True)
        message_label.bind(
            width=lambda *x: message_label.setter('text_size')(message_label, (message_label.width, None)),
            texture_size=message_label.setter('size'))
        scroll_view.add_widget(message_label)
        content.add_widget(scroll_view)

        btn_layout = BoxLayout(size_hint_y=None, height='50sp', spacing=5)
        agree_btn = Button(
            text="Agree",
            on_press=self._on_agree,
            height=50,
            font_size='18sp',
            background_color=(0.314, 0.784, 0.471, 1)
        )
        disagree_btn = Button(
            text="Disagree",
            on_press=self._on_disagree,
            background_color=(0.862, 0.078, 0.235, 1),
            height=50,
            font_size='18sp',

        )
        btn_layout.add_widget(agree_btn)
        btn_layout.add_widget(disagree_btn)

        content.add_widget(btn_layout)
        self.initial_popup = Popup(title="GDP clause - Confirmation",
                                   content=content,
                                   size_hint=(None, None),
                                   auto_dismiss=False,
                                   size=config.POPUP_SIZE)
        self.initial_popup.open()

    def _on_agree(self, instance):
        self.initial_popup.dismiss()
        # Additional logic for agreement
        self.stop()

    def _on_disagree(self, instance):
        self.initial_popup.dismiss()
        # Additional logic for disagreement
        self.stop()
        quit(0)


if __name__ == '__main__':
    with open(config.GDPR_CLAUSE, mode='r', encoding='utf-8') as gdpr_clause:
        gdpr_clause = gdpr_clause.read()

    initial_prompt_app = GDPRClause(gdpr_clause)
    initial_prompt_app.run()
