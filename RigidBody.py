import numpy as np
from Constants import *

class RigidBody:
    def __init__(self, position, velocity, mass, radius, color, vertices=None, is_static=False):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.mass = mass
        self.radius = radius
        self.color = color
        self.vertices = vertices
        self.orientation = 0.0
        self.angular_velocity = 0.0
        self.force_accumulator = np.zeros(2, dtype=float)
        self.is_static = is_static

    def apply_force(self, force):
        self.force_accumulator += force
        
    def clear_forces(self):
        self.force_accumulator.fill(0.0)

    def apply_torque(self, torque, dt):
        angular_acceleration = torque / self.mass
        self.angular_velocity += angular_acceleration * dt

    def update_with_impulse(self, dt):
        if self.mass == 0:
            return

        acceleration = self.force_accumulator / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt

    def update(self, dt):
        acceleration = self.force_accumulator / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt + 0.5 * acceleration * dt ** 2
        delta_angle = self.angular_velocity * dt
        self.orientation += delta_angle

    def rotate(self, angle_radians):
        self.orientation += angle_radians
