import numpy as np

def rotate_vector(vector, degrees):
    radians = np.radians(degrees)
    rotation_matrix = np.array([[np.cos(radians), -np.sin(radians)], [np.sin(radians), np.cos(radians)]])
    return np.dot(rotation_matrix, vector)

def PolygonVertices(number_vertices, length, breadth):
    degrees = 360 / number_vertices
    apothem = length / (2 * np.tan(np.pi / number_vertices))
    vertices = [rotate_vector([0, apothem], degrees * i) for i in range(number_vertices)]
    return vertices

# Example usage:
vertices = PolygonVertices(4, 1, 0)
print(vertices)
