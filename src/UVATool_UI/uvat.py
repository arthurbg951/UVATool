from enum import Enum
# import typing

class Apoio(Enum):
    primeiroGenero = 0
    segundoGenero = 1
    terceiroGenero = 2
    semiRigido = 3
    semApoio = 4


class Canvas(object):
    def __init__(self) -> None:
        self.nodes = []
        self.elements = []
        self.drawnNodes = []
        self.drawnElements = []
        self.loadings = []
        self.drawnLoadings = []
        self.grid = Grid()


class Grid(object):
    def __init__(self) -> None:
        self.points = []
        self.isActive = False


class Defaults(object):
    def __init__(self) -> None:
        self.moduloDeElasticidade = 1
        self.momentoDeInercia = 1

    def __str__(self) -> str:
        return "{0}{1}".format(self.moduloDeElasticidade, self.momentoDeInercia)


class Node(object):
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.apoio = None
        self.p = 1

    def __str__(self) -> str:
        return "{0},{1}".format(self.x, self.y)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.x == other.x and self.y == other.y


class Element(object):
    def __init__(self, node1: Node, node2: Node) -> None:
        self.node1 = node1
        self.node2 = node2
        self.coefficientElascity = None
        self.momentInertia = None

    def getLenght(self) -> float:
        raise NotImplementedError("A função não foi implementada pelos programadores!")

    def getAngulo(self) -> float:
        raise NotImplementedError("A função não foi implementada pelos programadores!")

    def setCoefficientElascity(self, moduloDeElasticidade: float) -> None:
        self.coefficientElascity = moduloDeElasticidade

    def setMomentInertia(self, momentoDeInercia: float) -> None:
        self.momentInertia = momentoDeInercia

    def __str__(self) -> str:
        return "Node1={0};Node2={1}".format(self.node1, self.node2)
