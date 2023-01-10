import numpy


class NodalForce:
    fx: float
    fy: float
    m: float

    def __init__(self, fx: float, fy: float, m: float) -> None:
        self.fx = fx
        self.fy = fy
        self.m = -m

    def getAsVector(self) -> numpy.array:
        return numpy.array([self.fx, self.fy, self.m])

    def __str__(self) -> str:
        return "{0};{1};{2}".format(self.fx, self.fy, self.m)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, NodalForce):
            return NotImplemented
        return self.fx == __o.fx and self.fy == __o.fy and self.m == __o.m
