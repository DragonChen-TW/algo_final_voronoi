def is_left(v0, v1, v2):
    direction = (v0[0] - v2[0])*(v1[1] - v2[1]) - (v0[1] - v2[1])*(v1[0] - v2[0])
    return direction > 0

def melkman(points):
    if len(points) == 1:
        return []
    elif len(points) == 2:
        return [points[0], points[1], points[0]]

    # init
    if is_left(points[0], points[1], points[2]):
        cv_points = [points[2], points[0], points[1], points[2]]
    else:
        cv_points = [points[2], points[1], points[0], points[2]]

    i = 3

    while i < len(points):
        # inside the cv, skip
        while is_left(cv_points[-2], cv_points[-1], points[i]) \
            and is_left(cv_points[0], cv_points[1], points[i]):
            i += 1

        # if in
        while not is_left(cv_points[-2], cv_points[-1], points[i]):
            cv_points.pop()
        cv_points.append(points[i])

        while not is_left(points[i], cv_points[0], cv_points[1]):
            cv_points.pop(0)
        cv_points.insert(0, points[i])

        i += 1

    return cv_points

if __name__ == '__main__':
    example4 = [
        [1., 1.],
        [3., 3.],
        [4., 1.1],
        [5.3, 1.0],
        [6.6, 1.5],
        [7.0, 3.0],
        [7.0, 5.0],
        [8.0, 5.0],
        [7.0, 1.0],
        [10.0, 1.0],
        [11.0, 5.8],
        [9.5, 6.5],
        [8.0, 8.0],
        [11.0, 1.2],
        [8.0, 6.0],
        [5.0, 6.0],
        [5.0, 9.5],
        [4.0, 5.5],
        [1.0, 10.0]
    ]

    cv_points = melkman(example4)

    print(cv_points)
