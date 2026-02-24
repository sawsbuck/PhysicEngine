# Copilot / AI Assistant Instructions for PhysicEngine

This file contains concise, actionable guidance for AI coding agents working on this repository.

Overview
- Big picture: `Main.py` is a Kivy UI wrapper that runs the simulation loop and delegates physics work to `PhysicsEngine.py`.
- `PhysicsEngine.py` manages a list of `RigidBody` objects (`RigidBody.py`), applies forces, resolves collisions using `Collision.py`, and draws via Kivy primitives.
- Bodies are either circles (no `vertices`) or polygons (`vertices` present). Static ground is represented as a `RigidBody` with `mass=float('inf')` and `is_static=True`.

Key files to inspect
- [Main.py](Main.py): Kivy app, input handling, scheduling (`Clock.schedule_interval`) and the main update order.
- [PhysicsEngine.py](PhysicsEngine.py): Physics loop order: `apply_forces(dt)` → `handle_collisions()` → `collide_with_ground()` → `draw_bodies(canvas)`.
- [RigidBody.py](RigidBody.py): `position` and `velocity` are NumPy arrays; `vertices` may be `None` (circle) or an array/list (polygon).
- [Collision.py](Collision.py): Narrow-phase helpers: `check_circle_collision`, `Polygon_collision`, `resolve_collision`.
- [Constants.py](Constants.py): Global parameters: `WIDTH, HEIGHT, FPS, GRAVITY, COEFFICIENT_OF_RESTITUTION, FRICTION`.
- [PolygonVertices.py](PolygonVertices.py): Helper to generate polygon vertex lists used when creating polygon bodies.

Project-specific patterns & conventions
- Vector representation: positions/velocities are NumPy arrays (use `np.array`). Kivy's `Vector` is also used in places — be careful to convert between types when needed.
- Body types: absence of `vertices` implies a circle; presence implies a polygon. Use `physics_engine.add_body(...)` and `add_static_body(...)` consistently.
- Colors are 3-tuples with integer RGB 0–255 values (e.g., `(255,0,0)`).
- Time-step: `PhysicsSimulation` constructs `PhysicsEngine(time_step=0.1 / FPS)` and schedules updates at `1/FPS` — note this project uses a custom `time_step` calculation.
- Ground: the engine uses a `ground` `RigidBody` with `vertices=[[0,0],[WIDTH,0],[0,20],[WIDTH,20]]` and draws a `Rectangle` at `ground.position` with height 20.

Common functions & signatures (examples)
- `PhysicsEngine.add_body(position, velocity, mass, radius, color, vertices=None)` — when `vertices` provided, body is a polygon.
- `Collision.check_circle_collision(circle1, circle2) -> (is_collision, normal, penetration_depth)`
- `Collision.Polygon_collision(polygon1, polygon2) -> (is_collision, axes)` and `resolve_collision(polygon1, polygon2, axes) -> mtv`

Implementation notes for AI edits
- Keep data types consistent: prefer using NumPy arrays for vector math and convert Kivy `Vector` to/from NumPy when necessary.
- When changing collision logic, update both circle and polygon paths; `handle_collisions()` branches by presence/absence of `vertices`.
- Drawing code expects `body.position` to be numeric sequences compatible with Kivy drawing calls.
- Static bodies use `is_static=True` and may have `mass=float('inf')`. Respect `is_static` when applying impulses / velocity changes.

Environment & run steps
- Dependencies: at minimum `kivy` and `numpy`. Example install:

```
pip install kivy numpy
python Main.py
```

Testing and debugging notes
- There are no automated tests in the repo. Use the Kivy UI (`Main.py`) to exercise behaviors.
- Useful debug targets: inspect `PhysicsEngine.handle_circle_collision`, `handle_polygon_collision`, and `Collision.resolve_collision` for physics correctness.
- Watch for mixed vector types (NumPy vs Kivy `Vector`) causing silent errors.

If you change physics constants
- Update `Constants.py` and run the app to observe behavior changes. Example tunables: `GRAVITY`, `COEFFICIENT_OF_RESTITUTION`, `FRICTION`, `FPS`.

When to open PRs
- Small, focused PRs that touch a single subsystem (collision, integrator, rendering) are preferred.
- Include a short manual test plan in PR description (how to reproduce and expected behavior in the UI).

If anything in this document is unclear or you want specific examples (unit-test stubs, small refactors, or type consistency fixes), tell me which area to expand.
