import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse,Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from PhysicsEngineKivy import *
from RigidBody import *
from Constants import *



class PhysicsSimulation(Widget):
    def __init__(self, **kwargs):
        super(PhysicsSimulation, self).__init__(**kwargs)

        self.physics_engine = PhysicsEngine()

        # Schedule the update method to be called repeatedly
        Clock.schedule_interval(self.update, 1 / FPS)

    def on_touch_down(self, touch):
        if touch.button == 'left':
            mouse_x, mouse_y = touch.pos
            for body in self.physics_engine.bodies:
                if self.is_point_inside_circle(mouse_x, mouse_y, body):
                    self.show_change_values_popup(body)
                    break
            else:
                # Create a new ball at the touch position when no ball is clicked
                self.physics_engine.add_body(
                    position=[mouse_x, mouse_y],
                    velocity=[0, 0],  # Set the initial velocity as needed
                    mass=1,          # Set the mass and radius as needed
                    radius=20,
                    color=RED
                )

    

    def update(self, dt):
        self.physics_engine.apply_forces_and_update(dt)
        self.physics_engine.handle_collisions()
        self.physics_engine.collide_with_ground()
        self.canvas.clear()
        self.physics_engine.draw_bodies(self.canvas)
    def is_point_inside_circle(self, x, y, body):
        return (x - body.position[0]) ** 2 + (y - body.position[1]) ** 2 < body.radius ** 2

    def show_change_values_popup(self, body):
        popup = Popup(title='Change Ball Values', size_hint=(None, None), size=(400, 200))
        content = BoxLayout(orientation='vertical')

        position_label = Label(text='Position (x, y):')
        position_input = TextInput(text=f'{body.position[0]}, {body.position[1]}')

        velocity_label = Label(text='Velocity (x, y):')
        velocity_input = TextInput(text=f'{body.velocity[0]}, {body.velocity[1]}')

        mass_label = Label(text='Mass:')
        mass_input = TextInput(text=str(body.mass))

        radius_label = Label(text='Radius:')
        radius_input = TextInput(text=str(body.radius))

        color_label = Label(text='Color (R, G, B):')
        color_input = TextInput(text=f'{body.color[0]}, {body.color[1]}, {body.color[2]}')

        save_button = Button(text='Save Changes', on_release=lambda btn: self.save_changes(body,popup, position_input.text,
                                                                                      velocity_input.text,
                                                                                      mass_input.text,
                                                                                      radius_input.text,
                                                                                      color_input.text))
        cancel_button = Button(text='Cancel', on_release=popup.dismiss)

        content.add_widget(position_label)
        content.add_widget(position_input)
        content.add_widget(velocity_label)
        content.add_widget(velocity_input)
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

        popup.content = content
        popup.open()

    def save_changes(self, body,popup,position_input, velocity_input, mass_input, radius_input, color_input):
        try:
            x, y = map(float, position_input.split(','))
            body.position = [x, y]

            vx, vy = map(float, velocity_input.split(','))
            body.velocity = [vx, vy]

            body.mass = float(mass_input)
            body.radius = float(radius_input)

            r, g, b = map(int, color_input.split(','))
            body.color = (r, g, b)

        # Close the popup after saving changes
            body.velocity[1] = -abs(body.velocity[1]) * COEFFICIENT_OF_RESTITUTION
            body.position[1] = self.physics_engine.ground.position[1] - body.radius
            body.velocity[0] *= FRICTION

        except ValueError:
            print("Invalid input. Please enter numeric values.")

        # Close the popup after saving changes
        popup.dismiss()

class PhysicsApp(App):
    def build(self):
        Window.size = (WIDTH, HEIGHT)
        return PhysicsSimulation()

if __name__ == "__main__":
    PhysicsApp().run()