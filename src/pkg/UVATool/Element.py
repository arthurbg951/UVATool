from UVATool.Node import Node
from UVATool.Exceptions.StructureError import StructureError
from UVATool.Point2d import Point2d
import math


class Element:
    node1: Node
    node2: Node
    area: float
    moment_inertia: float
    young_modulus: float
    __p1: float
    __p2: float

    def __init__(self, node1: Node, node2: Node, area: float, moment_inertia: float, young_modulus: float) -> None:
        self.node1 = node1
        self.node2 = node2
        self.__verifyNodes()
        # self.__verifyRoute()
        self.area = area
        self.moment_inertia = moment_inertia
        self.young_modulus = young_modulus
        self.__p1 = node1.getP()
        self.__p2 = node2.getP()

    def __str__(self) -> str:
        return f"NODE1={self.node1}; NODE2={self.node2}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Element):
            normalDirection = self.node1 == other.node1 and self.node2 == other.node2
            reverseDirection = self.node1 == other.node2 and self.node2 == other.node1
            return normalDirection or reverseDirection
        else:
            return NotImplemented

    def __verifyNodes(self) -> None:
        if self.node1 == self.node2:
            raise StructureError("node1 cant be equal to node2.")

    def __verifyRoute(self) -> None:
        point = Point2d(self.node2.x - self.node1.x, self.node2.y - self.node1.y)
        print(point)
        inverter = (point.x < 0 and point.y < 0) or (point.x > 0 and point.y < 0)
        if inverter:
            newNode1 = self.node1
            newNode2 = self.node2
            self.node1 = newNode2
            self.node2 = newNode1

    def getLength(self) -> float:
        return math.sqrt(math.pow(self.node1.x - self.node2.x, 2) + math.pow(self.node1.y - self.node2.y, 2))

    def getAngle(self) -> float:
        sinalQuadrante = 1
        u = Point2d(1, 0)
        v = Point2d(self.node2.x - self.node1.x, self.node2.y - self.node1.y)
        if v.x < 0 and v.y < 0 or v.x > 0 and v.y < 0 or v.x <= 0 and v.y == 0 or v.x == 0 and v.y < 0:
            sinalQuadrante = -1
        # ALL POSSIBLE ANGLES
        # if v.x > 0 and v.y > 0:
        #     sinalQuadrante = 1
        # elif v.x < 0 and v.y > 0:
        #     sinalQuadrante = 1
        # elif v.x < 0 and v.y < 0:
        #     sinalQuadrante = -1
        # elif v.x > 0 and v.y < 0:
        #     sinalQuadrante = -1
        # elif v.x > 0 and v.y == 0:
        #     sinalQuadrante = 1
        # elif v.x == 0 and v.y > 0:
        #     sinalQuadrante = 1
        # elif v.x <= 0 and v.y == 0:
        #     sinalQuadrante = -1
        # elif v.x == 0 and v.y < 0:
        #     sinalQuadrante = -1
        uv = u.x * v.x + u.y * v.y
        modu = math.sqrt(math.pow(u.x, 2) + math.pow(u.y, 2))
        modv = math.sqrt(math.pow(v.x, 2) + math.pow(v.y, 2))
        return sinalQuadrante * math.acos(uv/(modu * modv))

    def setP(self, p1: float, p2: float) -> None:
        # possivel erro: implementar com verificações do node self.node1.setP(p1)
        self.__p1 = p1
        self.__p2 = p2

    def getP(self) -> list:
        return [self.__p1, self.__p2]
