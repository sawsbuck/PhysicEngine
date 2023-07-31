from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from Constants import *


class OptionsMenu:
    def __init__(self, physics_simulation):
        self.physics_simulation = physics_simulation
        self.menu = DropDown()
        self.create_menu_options()

    def create_menu_options(self):
        remove_balls_button = Button(text='Remove All Balls', size_hint_y=None, height=40)
        remove_balls_button.bind(on_release=self.remove_all_balls)
        self.menu.add_widget(remove_balls_button)

        gravity_label = Label(text='Change Gravity:', size_hint_y=None, height=40)
        self.menu.add_widget(gravity_label)

        gravity_input = TextInput(text=str(GRAVITY), multiline=False, size_hint_y=None, height=40)
        gravity_input.bind(on_text_validate=self.change_gravity)
        self.menu.add_widget(gravity_input)

    def remove_all_balls(self, *args):
        self.physics_simulation.remove_all_balls()

    def change_gravity(self, instance, text):
        try:
            GRAVITY = float(text)
        except ValueError:
            print("Invalid input")

    def open_menu(self, widget):
        self.menu.open(widget)