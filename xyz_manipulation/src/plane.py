class Plane:
    def __init__(self, point, normal_vector):
        assert (len(point) == 3)
        assert (len(normal_vector) == 3)
        self.point = point
        self.normal_vector = normal_vector

    def get_point(self):
        return self.point.copy()

    def get_normal_vector(self):
        return self.normal_vector.copy()
