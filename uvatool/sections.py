import math


class Rectangle:
    b: float
    h: float
    __area: float
    __inertia: float

    def __init__(self, b: float, h: float) -> None:
        self.b = b
        self.h = h

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Rectangle):
            return NotImplemented
        return self.b == __o.b and self.h == __o.h

    @property
    def area(self) -> float:
        return self.b * self.h

    @property
    def inertia(self) -> float:
        return self.b * math.pow(self.h, 3) / 12
