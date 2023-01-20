import math


class Point2d:
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "({0},{1})".format(self.x, self.y)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Point2d):
            return NotImplemented
        return self.x == __o.x and self.y == __o.y

    def __add__(self, __o: object):
        if not isinstance(__o, Point2d):
            return NotImplemented
        return Point2d(__o.x + self.x, __o.y + self.y)

    def __truediv__(self, __o: object):
        if isinstance(__o, Point2d):
            # divisão de um ponto por outro (verificar existencia na geomegria analítica para implementação)
            return NotImplemented
        if isinstance(__o, float or int):
            return Point2d(self.x/__o, self.y/__o)

    def distTo(self, point: object):
        """Calculate de distance between 2 points"""
        if not isinstance(point, Point2d):
            return NotImplemented
        return math.sqrt(math.pow(self.x - point.x, 2) + math.pow(self.y - point.y, 2))
