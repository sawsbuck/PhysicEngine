import numpy as np
from RigidBody import RigidBody
from Constants import *
from Collision import Collision

class PhysicsEngine:
    def __init__(self,time_step):
        self.bodies = []
        self.time_step = time_step
        self.ground = RigidBody(position=[0, 0], velocity=[0, 0], mass=float('inf'), radius=0, color=WHITE, vertices=np.array([[0, 0], [WIDTH, 0], [0, 20], [WIDTH, 20]]))
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
        if not is_collision:
            return

        # relative velocity
        v_rel = circle1.velocity - circle2.velocity
        vel_along_normal = np.dot(v_rel, normal)

        # Do not resolve if velocities are separating
        if vel_along_normal > 0:
            # still correct penetration if any
            pass

        # inverse masses (static or infinite mass -> inv_mass = 0)
        inv_mass1 = 0.0 if circle1.is_static or circle1.mass == float('inf') else 1.0 / circle1.mass
        inv_mass2 = 0.0 if circle2.is_static or circle2.mass == float('inf') else 1.0 / circle2.mass

        # compute impulse scalar (standard formula)
        denom = inv_mass1 + inv_mass2
        if denom == 0:
            return

        # restitution
        e = COEFFICIENT_OF_RESTITUTION
        j = -(1 + e) * vel_along_normal / denom

        # if objects are moving apart, j may be negative; skip impulse application
        if j != 0:
            if not circle1.is_static:
                circle1.velocity += (j * inv_mass1) * normal
            if not circle2.is_static:
                circle2.velocity -= (j * inv_mass2) * normal

        # positional correction to avoid sinking (percent bias)
        percent = 0.8  # positional correction percentage
        correction_denom = denom
        if correction_denom > 0 and penetration_depth > 0:
            correction = (penetration_depth / correction_denom) * percent * normal
            if not circle1.is_static:
                circle1.position += correction * inv_mass1
            if not circle2.is_static:
                circle2.position -= correction * inv_mass2

    def handle_polygon_collision(self, body1, body2):
        body1points = body1.position + np.array(body1.vertices)
        body2points = body2.position + np.array(body2.vertices)
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
                body.position += np.array([0.0, penetration_depth])
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
        # Drawing is UI-specific; PhysicsEngine is UI-agnostic now.
        pass

    def step(self, dt):
        """Advance the physics simulation by dt seconds (single update)."""
        self.apply_forces(dt)
        self.handle_collisions()
        self.collide_with_ground()

    def get_state(self):
        """Return a serializable snapshot of bodies for external renderers.

        Format: list of dicts: {id, position:[x,y], velocity:[x,y], radius, color:[r,g,b], vertices:[[x,y],...], is_static}
        """
        out = []
        for i, body in enumerate(self.bodies):
            vertices = None
            if body.vertices is not None:
                vertices = [list(map(float, v)) for v in np.array(body.vertices)]

            out.append({
                "id": i,
                "position": [float(body.position[0]), float(body.position[1])],
                "velocity": [float(body.velocity[0]), float(body.velocity[1])],
                "radius": float(body.radius),
                "color": list(body.color),
                "vertices": vertices,
                "is_static": bool(body.is_static)
            })

        return {"bodies": out, "ground": {"position": [float(self.ground.position[0]), float(self.ground.position[1])], "color": list(self.ground.color)}}
