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
