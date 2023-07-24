import numpy as np



def project_polygon_onto_axis(polygon, axis):
    polygon = np.array(polygon)
    axis = np.array(axis)
    
    dots = [np.dot(vertex, axis) for vertex in polygon]
    print(dots)
    return min(dots), max(dots)

def intervals_overlap(interval1, interval2):
    return interval1[0] <= interval2[1] and interval1[1] >= interval2[0]

def get_axis(polygon):
    polygon = np.array(polygon)
    edges = [(polygon[(i + 1) % len(polygon)] - polygon[i]) for i in range(len(polygon))]
    axis = [np.array([-edge[1], edge[0]]) for edge in edges]
    return axis//np.linalg.norm(axis)

def sat_collision(polygon1, polygon2):
    axes = get_axis(polygon1) + get_axis(polygon2)
    
    for axis in axes:
        projection1 = project_polygon_onto_axis(polygon1, axis)
        projection2 = project_polygon_onto_axis(polygon2, axis)
        
        if not intervals_overlap(projection1, projection2):
            return False,None
    
    return True,axes

def calculate_penetration_vector(polygon1, polygon2, axis):
    polygon1 = np.array(polygon1)
    polygon2 = np.array(polygon2)
    
    min_overlap = float('inf')
    min_overlap_axis = None
    projection = project_polygon_onto_axis(polygon1, axis)
    overlap = intervals_overlap(projection, project_polygon_onto_axis(polygon2, axis))
    if not overlap:
        return None

    if projection[1] - projection[0] < min_overlap:
        min_overlap = projection[1] - projection[0]
        min_overlap_axis = axis


    projection = project_polygon_onto_axis(polygon2, axis)
    overlap = intervals_overlap(projection, project_polygon_onto_axis(polygon1, axis))

    if not overlap:
        return None

    if projection[1] - projection[0] < min_overlap:
        min_overlap = projection[1] - projection[0]
        min_overlap_axis = -axis

    return min_overlap_axis * min_overlap

def resolve_collision(polygon1, polygon2):
    collides, axes = sat_collision(polygon1, polygon2)
    if collides:
        mtv = None
        min_mtv_length = float('inf')

        for axis in axes:
            penetration_vector = calculate_penetration_vector(polygon1, polygon2, axis)
            if penetration_vector is not None:
                mtv_length = np.linalg.norm(penetration_vector)
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
