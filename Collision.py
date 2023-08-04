import numpy as np

class Collision:
    def project_polygon_onto_axis(self, polygon, axis):
        dots = np.dot(polygon, axis)
        return np.min(dots), np.max(dots)

    def intervals_overlap(self, interval1, interval2):
        return interval1[0] <= interval2[1] and interval1[1] >= interval2[0]

    def get_axis(self, polygon):
        edges = np.diff(polygon, axis=0)
        return [np.array([-edge[1], edge[0]]) for edge in edges]

    def Polygon_collision(self, polygon1, polygon2):
        axes = self.get_axis(polygon1) + self.get_axis(polygon2)
        
        for axis in axes:
            projection1 = self.project_polygon_onto_axis(polygon1, axis)
            projection2 = self.project_polygon_onto_axis(polygon2, axis)
            
            if not self.intervals_overlap(projection1, projection2):
                return False, None
        
        return True, axes
    
    
    def calculate_penetration_vector(self, polygon1, polygon2, axis):
        projection1 = self.project_polygon_onto_axis(polygon1, axis)
        projection2 = self.project_polygon_onto_axis(polygon2, axis)

        overlap = self.intervals_overlap(projection1, projection2)
        if not overlap:
            return None

        min_overlap = np.min([projection1[1] - projection2[0], projection2[1] - projection1[0]])
        return axis * min_overlap

    def resolve_collision(self, polygon1, polygon2, axes):
        mtv = np.zeros(2)  # Initialize MTV to a zero vector
        min_mtv_length = float('inf')

        for axis in axes:
            penetration_vector = self.calculate_penetration_vector(polygon1, polygon2, axis)
            if penetration_vector is not None:
                mtv_length = np.linalg.norm(penetration_vector)
                if mtv_length < min_mtv_length:
                    mtv = penetration_vector
                    min_mtv_length = mtv_length

        return mtv/np.linalg.norm(mtv) # Return the calculated MTV, even if it's a zero vector


    def check_circle_collision(self,circle1, circle2):
        delta = circle2.position - circle1.position
        distance_squared = np.dot(delta, delta)
        if distance_squared < (circle1.radius + circle2.radius) ** 2:
            distance = np.sqrt(distance_squared)
            normal = delta / distance
            penetration_depth = (circle1.radius + circle2.radius) - distance
            return True, normal, penetration_depth
        else:
            return False, np.array([0.0, 0.0]), 0.0
