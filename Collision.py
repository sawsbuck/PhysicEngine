from Vector2d import Vector2D
def project_polygon_onto_axis(polygon, axis):
    dots = [Vector2D(*vertex).dot(axis) for vertex in polygon]
    return min(dots), max(dots)


def intervals_overlap(interval1, interval2):
    return interval1[0] <= interval2[1] and interval1[1] >= interval2[0]


def get_axis(polygon):
    edges = [Vector2D(*(polygon[(i + 1) % len(polygon)]) - Vector2D(*polygon[i])) for i in range(len(polygon))]
    return [edge.normalized() for edge in edges]


def sat_collision(polygon1, polygon2):
    axes = get_axis(polygon1) + get_axis(polygon2)

    for axis in axes:
        projection1 = project_polygon_onto_axis(polygon1, axis)
        projection2 = project_polygon_onto_axis(polygon2, axis)

        if not intervals_overlap(projection1, projection2):
            return False, None

    return True, axes


def calculate_penetration_vector(polygon1, polygon2, axis):
    projection1 = project_polygon_onto_axis(polygon1, axis)
    projection2 = project_polygon_onto_axis(polygon2, axis)

    if not intervals_overlap(projection1, projection2):
        return None

    overlap = min(projection1[1], projection2[1]) - max(projection1[0], projection2[0])
    return axis * overlap


def resolve_collision(polygon1, polygon2):
    collides, axes = sat_collision(polygon1, polygon2)
    if collides:
        mtv = None
        min_mtv_length = float('inf')

        for axis in axes:
            penetration_vector = calculate_penetration_vector(polygon1, polygon2, axis)
            if penetration_vector is not None:
                mtv_length = penetration_vector.magnitude()
                if mtv_length < min_mtv_length:
                    mtv = penetration_vector
                    min_mtv_length = mtv_length

        if mtv is not None:
            for i in range(len(polygon1)):
                polygon1[i] += mtv
            for i in range(len(polygon2)):
                polygon2[i] += mtv

            return True

    return False


polygon1 = [Vector2D(0, 0), Vector2D(20, 0), Vector2D(20, 20), Vector2D(0, 20)]
polygon2 = [Vector2D(20, 20), Vector2D(55, 25), Vector2D(55, 55), Vector2D(25, 55)]

collides, axes = sat_collision(polygon1, polygon2)

if collides:
    print("Polygons are colliding.")
    resolve_collision(polygon1, polygon2)
    print("Updated Polygon 1:", polygon1)
    print("Updated Polygon 2:", polygon2)
    print("Collision resolved.")
else:
    print("Polygons will not collide after moving.")