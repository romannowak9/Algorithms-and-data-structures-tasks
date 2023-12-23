from typing import List, Tuple, Union


def points_turn(p1, p2, p3) -> float:
    """ prawo dla out > 0, lewo dla out < 0 """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return (y2 - y1) * (x3 - x2) - (y3 - y2) * (x2 - x1)


def jarvis(points: List[Tuple], v: str = '1') -> List[Tuple]:
    p_x = [x for x, y in points]
    min_x = min(p_x)
    min_x_points = [points[i] for i, x in enumerate(p_x) if x == min_x]
    p_idx = points.index((min_x, min([y for x, y in min_x_points])))
    p_start = points[p_idx]
    hull = [p_start]

    p = p_start
    while True:
        p_idx = points.index(p)
        q = points[p_idx + 1] if p_idx != len(points) - 1 else points[0]
        for r in points:
            if r != p and r != q:
                turn = points_turn(p, q, r)
                if turn > 0:  # prawoskrętne
                    q = r
                if v == '2' and turn == 0 and ((p[0] < q[0] < r[0] or p[0] > q[0] > r[0]) or (
                        p[1] < q[1] < r[1] or p[1] > q[1] > r[1])):  # współliniowe
                    q = r

        hull.append(q)
        p = q
        if p == p_start:
            break

    return hull


def main():
    print(jarvis([(0, 3), (0, 0), (0, 1), (3, 0), (3, 3)]))
    print(jarvis([(0, 3), (0, 1), (0, 0), (3, 0), (3, 3)]))
    print(jarvis([(0, 3), (0, 0), (0, 1), (3, 0), (3, 3)], v='2'))
    print(jarvis([(0, 3), (0, 1), (0, 0), (3, 0), (3, 3)], v='2'))
    print(jarvis([(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)]))
    print(jarvis([(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)], v='2'))

if __name__ == "__main__":
    main()
