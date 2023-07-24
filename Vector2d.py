import numpy as np

class Vector2D:
    def __init__(self, x, y):
        self.data = np.array([x, y], dtype=float)

    def __repr__(self):
        return f"Vector2D({self.data[0]}, {self.data[1]})"

    def __add__(self, other):
        return Vector2D(self.data[0] + other.data[0], self.data[1] + other.data[1])

    def __sub__(self, other):
        return Vector2D(self.data[0] - other.data[0], self.data[1] - other.data[1])

    def __mul__(self, scalar):
        return Vector2D(self.data[0] * scalar, self.data[1] * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        return Vector2D(self.data[0] / scalar, self.data[1] / scalar)

    def dot(self, other):
        return np.dot(self.data, other.data)

    def magnitude(self):
        return np.linalg.norm(self.data)

    def normalized(self):
        mag = self.magnitude()
        return Vector2D(self.data[0] / mag, self.data[1] / mag)

    def angle_with(self, other):
        normalized_self = self.normalized()
        normalized_other = other.normalized()
        dot_product = normalized_self.dot(normalized_other)
        return np.arccos(np.clip(dot_product, -1.0, 1.0))

    def cross(self, other):
        return self.data[0] * other.data[1] - self.data[1] * other.data[0]