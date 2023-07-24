import numpy as np
import sys
from Constants import *

import numpy as np

class RigidBody:
    def __init__(self, position, velocity, mass, radius, color, vertices=None):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.mass = mass
        self.radius = radius
        self.color = color
        self.vertices = vertices

    def transform_vertices(self, vertices, position):
        self.vertices += self.position
        return vertices

    def apply_force(self, force, dt):
        acceleration = force / self.mass
        self.velocity += acceleration * dt

    def update(self, dt):
        self.position += self.velocity * dt


def check_circle_collision(circle1, circle2):
    delta = circle2.position - circle1.position
    distance_squared = np.dot(delta, delta)
    if distance_squared < (circle1.radius + circle2.radius) ** 2:
        distance = np.sqrt(distance_squared)
        normal = delta / distance
        penetration_depth = (circle1.radius + circle2.radius) - distance
        return True, normal, penetration_depth
    else:
        return False, np.array([0.0, 0.0]), 0.0
