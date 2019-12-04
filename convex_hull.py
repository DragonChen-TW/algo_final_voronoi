class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, p2):
        return self.x == p2.x and self.y == p2.y

    def __repr__(self):
        return f'Point(x={self.x},y={self.y})'

def get_leftest(points):
    temp = [p.x for p in points]
    return temp.index(min(temp))

class ConvexHull:
    def __init__(self, points=[]):
        self.points = points
        self.cv_points = []

    def run(self):
        self.run_slow()

    def get_direction(self, mid, p1, p2):
        direction = ((p2.x - mid.x) * (p1.y - mid.y)) \
                    - ((p1.x - mid.x) * (p2.y - mid.y))
        return direction
