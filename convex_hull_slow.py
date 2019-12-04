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

    def run_slow(self): # O (n^2)
        points = self.points

        leftest_i = get_leftest(points)
        self.cv_points.append(points[leftest_i]) # start from leftest

        now_point = points[leftest_i]
        next_point = None
        while next_point is not points[leftest_i]: # run until a circle
            p1 = None
            for p in points:
                if p == now_point:
                    continue
                else:
                    p1 = p
                    break

            next_point = p1

            for p2 in points:
                if p2 == now_point or p2 == p1:
                    continue
                else:
                    direction = self.get_direction(now_point, next_point, p2)
                    if direction > 0: # if clockwise
                        next_point = p2
            self.cv_points.append(next_point)
            now_point = next_point


    def get_direction(self, mid, p1, p2):
        direction = ((p2.x - mid.x) * (p1.y - mid.y)) \
                    - ((p1.x - mid.x) * (p2.y - mid.y))
        return direction
