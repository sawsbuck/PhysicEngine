import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse,Rectangle
from kivy.clock import Clock
from kivy.core.window import Window


from PhysicsEngine import *
from RigidBody import *
from Constants import *
from Popup import ChangeValuesPopup
from PolygonVertices import PolygonVertices
class PhysicsSimulation(Widget):
    def __init__(self, **kwargs):
        super(PhysicsSimulation, self).__init__(**kwargs)
        self.physics_engine = PhysicsEngine(time_step=0.1 / FPS)
        Clock.schedule_interval(self.update, 1 / FPS)

    def on_touch_down(self, touch):
        if touch.button == 'left':
            mouse_x, mouse_y = touch.pos
            for body in self.physics_engine.bodies:
                if self.is_point_inside_circle(mouse_x, mouse_y, body):
                    self.show_change_values_popup(body)
                    break
            else:
                self.physics_engine.add_body(position=[mouse_x, mouse_y],velocity=[0, 0], mass=1,radius=20,color=RED)
        if touch.button == 'right':
            mouse_x, mouse_y = touch.pos
            y=0
            self.physics_engine.add_body(position=[mouse_x, mouse_y],velocity=[0, 0], mass=1,radius=50,color=RED,vertices = PolygonVertices(4,100,0))
            y += 100
            

    def update(self, dt):
        
        self.physics_engine.apply_forces(dt)
        self.physics_engine.handle_collisions()
        self.physics_engine.collide_with_ground()
        self.canvas.clear()
        self.physics_engine.draw_bodies(self.canvas)

    def is_point_inside_circle(self, x, y, body):
        return (x - body.position[0]) ** 2 + (y - body.position[1]) ** 2 < body.radius ** 2

    def show_change_values_popup(self, body):
        popup = ChangeValuesPopup(body)
        popup.open()


class PhysicsApp(App):
    def build(self):
        Window.size = (WIDTH, HEIGHT)
        return PhysicsSimulation()


if __name__ == "__main__":
    PhysicsApp().run()
