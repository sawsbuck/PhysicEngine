from kivy.graphics import Color, Ellipse, Rectangle
from kivy.vector import Vector
from RigidBody import RigidBody
from Constants import *
from Collision import Collision

class PhysicsEngine:
    def __init__(self,time_step):
        self.bodies = []
        self.ground = RigidBody(position=[0,0], velocity=[0, 0], mass=float('inf'), radius=0, color=WHITE,vertices = [[0,0],[WIDTH,0],[0,20],[WIDTH,20]])
        self.time_step = time_step
    def add_body(self, position, velocity, mass, radius, color,vertices = None):
        self.bodies.append(RigidBody(position, velocity, mass, radius, color))
        
    def apply_forces(self, dt):
        for body in self.bodies:

            body.clear_forces()

            body.apply_force(GRAVITY)

            body.update_with_impulse(dt)

    def handle_collisions(self):
        for i, body1 in enumerate(self.bodies):
                for body2 in self.bodies[i+1:]:
                        is_collision, normal, penetration_depth = Collision.check_circle_collision(body1, body2)
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
            if body.position[1] - body.radius < self.ground.position[1] + 20:
                penetration_depth = (self.ground.position[1] + 20) - (body.position[1] - body.radius)
                body.position[1] += penetration_depth
                normal = np.array([0.0, 1.0])
                relative_velocity = body.velocity
                normal_velocity = np.dot(relative_velocity, normal)

                if normal_velocity < 0: 
                    impulse_magnitude = -(1 + COEFFICIENT_OF_RESTITUTION) * normal_velocity
                    impulse = impulse_magnitude * normal
                    body.velocity += impulse

                friction_force = -body.velocity * body.mass * FRICTION
                body.apply_force(friction_force)

    def draw_bodies(self, canvas):
        for body in self.bodies:
            if body.vertices == None:
                with canvas:
                    Color(*body.color)
                    Ellipse(pos=(body.position[0] - body.radius, body.position[1] - body.radius), size=(body.radius * 2, body.radius * 2))
        with canvas:
            Color(*self.ground.color)
            Rectangle(pos=self.ground.position, size=(WIDTH, 20))
