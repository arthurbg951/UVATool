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
    area = 1
    momentoDeInercia = 1
    moduloDeElasticidade = 1
    

    def __str__(self) -> str:
        return "{0}{1}".format(self.moduloDeElasticidade, self.momentoDeInercia)
