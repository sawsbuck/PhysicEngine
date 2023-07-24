import pygame
import sys
from PhysicsEngine import PhysicsEngine
from RigidBody import *
from Constants import *
pygame.init()

# Constants






def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SAT 2D Physics Engine")
    clock = pygame.time.Clock()

    physics_engine = PhysicsEngine()

    while True:
        dt = clock.tick(FPS) / 30.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Create a new ball at the mouse click position when left-clicked
                mouse_x, mouse_y = event.pos
                physics_engine.add_body(
                    position=[mouse_x, mouse_y],
                    velocity=[0, 0],  # Set the initial velocity as needed
                    mass=1,          # Set the mass and radius as needed
                    radius=20,
                    color=RED
                )



        screen.fill((0, 0, 0))

        physics_engine.apply_forces_and_update(dt)
        physics_engine.handle_collisions()
        physics_engine.collide_with_ground()
        physics_engine.draw_bodies(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
