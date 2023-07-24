from kivy.graphics import Color, Ellipse, Rectangle
from kivy.vector import Vector
from RigidBody import *
from Constants import *

class PhysicsEngine:
    def __init__(self):
        self.bodies = []
        self.ground = RigidBody(position=[0, -(HEIGHT-20)], velocity=[0, 0], mass=float('inf'), radius=0, color=WHITE)

    def add_body(self, position, velocity, mass, radius, color):
        self.bodies.append(RigidBody(position, velocity, mass, radius, color))

    def apply_forces_and_update(self, dt):
        for body in self.bodies:
            body.apply_force(GRAVITY * body.mass, dt)
            body.update(dt)

    def handle_collisions(self):
        for i, body1 in enumerate(self.bodies):
            for body2 in self.bodies[i+1:]:
                is_collision, normal, penetration_depth = check_circle_collision(body1, body2)
                if is_collision:
                    total_mass = body1.mass + body2.mass
                    impulse = (1 + COEFFICIENT_OF_RESTITUTION) * (body1.velocity - body2.velocity).dot(normal) / total_mass
                    body1.velocity -= impulse * normal * body2.mass
                    body2.velocity += impulse * normal * body1.mass
                    separation = normal * penetration_depth / total_mass
                    body1.position -= separation * body2.mass
                    body2.position += separation * body1.mass

    def collide_with_ground(self):
        for body in self.bodies:
            if body.position[1] + body.radius > self.ground.position[1]:
                body.velocity[1] = -abs(body.velocity[1]) * COEFFICIENT_OF_RESTITUTION
                body.position[1] = self.ground.position[1] - body.radius
                body.velocity[0] *= FRICTION
            if 0 > body.position[0] + body.radius or body.position[0] + body.radius > WIDTH:
                body.velocity[0] = -abs(body.velocity[1]) * COEFFICIENT_OF_RESTITUTION
                body.position[0] = WIDTH - body.radius
                body.velocity[0] *= FRICTION

    def draw_bodies(self, canvas):
        for body in self.bodies:
            with canvas:
                Color(*body.color)
                Ellipse(pos=(body.position[0] - body.radius, body.position[1] - body.radius), size=(body.radius * 2, body.radius * 2))

        with canvas:
            Color(*self.ground.color)
            Rectangle(pos=self.ground.position, size=(WIDTH, 20))
