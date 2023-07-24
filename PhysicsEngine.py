import pygame
import numpy as np
from RigidBody import *
from Constants import *

class PhysicsEngine:
    def __init__(self):
        self.bodies = []
        self.ground = RigidBody(position=[0, HEIGHT-20], velocity=[0, 0], mass=float('inf'), radius=0, color=WHITE)

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
                    relative_velocity = body1.velocity - body2.velocity
                    impulse = (1 + COEFFICIENT_OF_RESTITUTION) * np.dot(relative_velocity, normal) / total_mass
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

    def draw_bodies(self, screen):
        for body in self.bodies:
            pygame.draw.circle(screen, body.color, (int(body.position[0]), int(body.position[1])), body.radius)
        pygame.draw.rect(screen, self.ground.color, pygame.Rect(self.ground.position[0], self.ground.position[1], WIDTH, 20))
