import numpy as np
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.vector import Vector
from RigidBody import RigidBody
from Constants import *
from Collision import Collision

class PhysicsEngine:
    def __init__(self,time_step):
        self.bodies = []
        self.time_step = time_step
        self.ground = RigidBody(position=[0, 0], velocity=[0, 0], mass=float('inf'), radius=0, color=WHITE, vertices=[[0, 0], [WIDTH, 0], [0, 20], [WIDTH, 20]])
        self.narrow_collision = Collision()
    def add_body(self, position, velocity, mass, radius, color,vertices = None):
        self.bodies.append(RigidBody(position, velocity, mass, radius, color,vertices))
    def add_static_body(self, position, velocity, mass, radius, color,vertices = None):
        self.bodies.append(RigidBody(position, velocity, mass, radius, color,vertices ,is_static= True))

    def apply_forces(self, dt):
        for body in self.bodies:

            body.clear_forces()

            body.apply_force(GRAVITY)

            body.update_with_impulse(dt)

    def handle_collisions(self):
        for i, body1 in enumerate(self.bodies):
            for body2 in self.bodies[i+1:]:
                if body1.vertices is None and body2.vertices is None:
                    self.handle_circle_collision(body1, body2)
                elif body1.vertices is not None and body2.vertices is not None:
                    self.handle_polygon_collision(body1, body2)

    def handle_circle_collision(self, circle1, circle2):
        is_collision, normal, penetration_depth = self.narrow_collision.check_circle_collision(circle1, circle2)
        if is_collision:
            total_mass = circle1.mass + circle2.mass
            impulse = (1 + COEFFICIENT_OF_RESTITUTION) * (circle1.velocity - circle2.velocity).dot(normal) / total_mass

            if not circle1.is_static:
                circle1.velocity -= impulse * normal * circle2.mass
            if not circle2.is_static:
                circle2.velocity += impulse * normal * circle1.mass

            separation = normal * penetration_depth / total_mass
            circle1.position -= separation * circle2.mass
            circle2.position += separation * circle1.mass

    def handle_polygon_collision(self, body1, body2):
        body1points = body1.position + body1.vertices
        body2points = body2.position + body2.vertices
        is_collision, axes = self.narrow_collision.Polygon_collision(body1points, body2points)

        if is_collision:
            mtv = self.narrow_collision.resolve_collision(body1points, body2points, axes)

            # Calculate relative velocity
            relative_velocity = body2.velocity - body1.velocity
            normal_velocity = np.dot(relative_velocity, mtv)

            # Check if the bodies are moving towards each other
            if normal_velocity < 0:
                # Calculate the impulse
                total_mass = body1.mass + body2.mass
                impulse = (1 + COEFFICIENT_OF_RESTITUTION) * normal_velocity / total_mass

                # Apply the impulse to the velocities
                body1.velocity += impulse * mtv / body1.mass
                body2.velocity -= impulse * mtv / body2.mass
                print(mtv)
                print(body1.velocity)




    def collide_with_ground(self):
        for body in self.bodies:
            ground_bottom = self.ground.position[1]
            if body.position[1] - body.radius < ground_bottom:
                penetration_depth = ground_bottom - (body.position[1] - body.radius)
                body.position += Vector(0, penetration_depth)
                normal = np.array([0.0, 1.0])
                relative_velocity = body.velocity
                normal_velocity = np.dot(relative_velocity, normal)

                if normal_velocity < 0:  # Check if the body is moving towards the ground
                    # Apply the impulse due to ground collision
                    impulse_magnitude = abs((1 + COEFFICIENT_OF_RESTITUTION) * normal_velocity)
                    impulse = impulse_magnitude * normal
                    body.velocity += impulse

                    # Apply friction force to the body
                    friction_force = -body.velocity * body.mass * FRICTION
                    body.apply_force(friction_force)

            # If the body is static, reset its velocity to zero to prevent any further movement
            if body.is_static:
                body.velocity = np.array([0.0, 0.0])



    def draw_bodies(self, canvas):
        for body in self.bodies:
            if body.vertices is None:
                with canvas:
                    Color(*body.color)
                    Ellipse(pos=(body.position[0] - body.radius, body.position[1] - body.radius), size=(body.radius * 2, body.radius * 2))
            else:
                with canvas:
                    Color(*body.color)
                    points = [(body.position[0] + x, body.position[1] + y) for x, y in body.vertices]
                    Line(points=points, close=True)
        with canvas:
            Color(*self.ground.color)
            Rectangle(pos=self.ground.position, size=(WIDTH, 20))
