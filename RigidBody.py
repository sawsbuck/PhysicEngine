import numpy as np
from Constants import *

class RigidBody:
    def __init__(self, position, velocity, mass, radius, color, vertices=None, is_static = False):
        
        self.position = np.array(position, dtype=float)
        self.prev_position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.mass = mass
        self.radius = radius
        self.color = color
        self.vertices = vertices
        self.orientation = 0.0  
        self.angular_velocity = 0.0
        self.force_accumulator = np.array([0.0, 0.0], dtype=float)

    def apply_force(self, force):
        self.force_accumulator += force

    def clear_forces(self):
        self.force_accumulator.fill(0.0)

    def update_with_impulse(self, dt):

        acceleration = self.force_accumulator / self.mass
        self.velocity += acceleration * dt

        self.position += self.velocity * dt

    def clear_forces(self):
        self.force_accumulator.fill(0.0)

    def apply_torque(self, torque, dt):
        angular_acceleration = torque / self.mass
        self.angular_velocity += angular_acceleration * dt

    def update(self, dt):
        if self.vertices is not None:
            delta_position = self.position - self.prev_position
            self.prev_position = np.copy(self.position)
            self.position += self.velocity + 0.5 * self.acceleration * dt**2
            for i in range(len(self.vertices)):
                self.vertices[i] += delta_position

            delta_angle = self.angular_velocity * dt
            self.angle += delta_angle
        else:
            self.prev_position = np.copy(self.position)
            self.position += self.velocity + 0.5 * self.acceleration * dt**2
            self.angle += self.angular_velocity * dt

    def rotate(self, angle_radians):
        self.angle += angle_radians

