    def collide_with_ground(self):
            for body in self.bodies:
                # Calculate the predicted next position of the body
                next_position = body.position + body.velocity * self.time_step

                # Check if the predicted next position is below the ground
                if next_position[1] - body.radius < self.ground.position[1] + 20:
                    # Apply ground reaction force to stop the body from penetrating the ground
                    penetration_depth = (self.ground.position[1] + 20) - (next_position[1] - body.radius)
                    normal = np.array([0.0, 1.0])
                    force_magnitude = penetration_depth / self.time_step  # Adjust force based on time step
                    reaction_force = normal * force_magnitude
                    body.apply_force(reaction_force)

                    # Apply friction to slow down the body's lateral movement
                    friction_force = -body.velocity * body.mass * self.friction_coefficient
                    body.apply_force(friction_force)

                    # Correct the position of the body to avoid penetrating the ground
                    body.position[1] = self.ground.position[1] + 20 + body.radius