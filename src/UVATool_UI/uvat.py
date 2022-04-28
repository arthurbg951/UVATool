from enum import Enum


class Apoio(Enum):
    primeiroGenero = 0
    segundoGenero = 1
    terceiroGenero = 2
    semiRigido = 3

class Canvas(object):
    def __init__(self) -> None:
        self.nodes = []
        self.elements = []
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
    def __init__(self, x: float, y: float, apoio: Apoio) -> None:
        self.x = x
        self.y = y
        self.apoio = apoio
        self.p = 1

    def __str__(self) -> str:
        return "({0}, {1})".format(self.x, self.y)


class Elemento(object):
    def __init__(self, no1: Node, no2: Node) -> None:
        self.no1 = no1
        self.no2 = no2
        self.moduloDeElasticidade = None
        self.momentoDeInercia = None

    def getLenght(self) -> float:
        return 10.

    def getAngulo(self) -> float:
        return 0.1

    def setModuloDeElasticidade(self, moduloDeElasticidade: float) -> None:
        self.moduloDeElasticidade = moduloDeElasticidade

    def setMomentoInercia(self, momentoDeInercia: float) -> None:
        self.momentoDeInercia = momentoDeInercia

    def __str__(self) -> str:
        return "{0}m {1}rad no1={2} no2={3}".format(self.getLenght(), self.getAngulo(), self.no1, self.no2)
