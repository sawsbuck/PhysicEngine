from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class ChangeValuesPopup(Popup):
    def __init__(self, body, **kwargs):
        super(ChangeValuesPopup, self).__init__(**kwargs)
        self.body = body
        self.title = 'Change Ball Values'
        self.size_hint = (None, None)
        self.size = (400, 200)
        self.content = self.create_popup_content()

    def create_popup_content(self):
        content = BoxLayout(orientation='vertical')




        mass_label = Label(text='Mass:')
        mass_input = TextInput(text=str(self.body.mass), multiline=False)
        self.ids.mass_input = mass_input

        radius_label = Label(text='Radius:')
        radius_input = TextInput(text=str(self.body.radius), multiline=False)
        self.ids.radius_input = radius_input

        color_label = Label(text='Color (R, G, B):')
        color_input = TextInput(text=f'{self.body.color[0]}, {self.body.color[1]}, {self.body.color[2]}',
                                multiline=False)
        self.ids.color_input = color_input

        save_button = Button(text='Save Changes', on_release=self.save_changes)
        cancel_button = Button(text='Cancel', on_release=self.dismiss)

        content.add_widget(mass_label)
        content.add_widget(mass_input)
        content.add_widget(radius_label)
        content.add_widget(radius_input)
        content.add_widget(color_label)
        content.add_widget(color_input)

        buttons_layout = BoxLayout(orientation='horizontal')
        buttons_layout.add_widget(save_button)
        buttons_layout.add_widget(cancel_button)

        content.add_widget(buttons_layout)

        return content

    def save_changes(self, *args):
        try:

            self.body.mass = float(self.ids.mass_input.text)
            self.body.radius = float(self.ids.radius_input.text)

            r, g, b = map(int, self.ids.color_input.text.split(','))
            self.body.color = (r, g, b)

        except ValueError:
            print("Invalid input")

        self.dismiss()
