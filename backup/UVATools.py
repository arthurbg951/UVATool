import sys
from enum import Enum
import numpy as np
# import typing
from typing import Protocol, List, overload
from abc import abstractmethod
import math


class Apoio(Enum):
    primeiroGenero = 0
    segundoGenero = 1
    terceiroGenero = 2
    semiRigido = 3
    semApoio = 4


class ISection(Protocol):
    @abstractmethod
    def area(self): raise NotImplementedError
    @abstractmethod
    def momentInertia(self): raise NotImplementedError


class Retangle(ISection):
    def __init__(self, b: float, h: float) -> None:
        super().__init__()
        self.__b = b
        self.__h = h

    def area(self) -> float:
        return self.__b * self.__h

    def momentInertia(self) -> float:
        return self.__b * math.pow(self.__h, 3) / 12


class Canvas(object):
    def __init__(self) -> None:
        self.nodes = []
        self.elements = []
        # ICONE DESENHADO NA TELA
        self.drawnNodes = []
        # LINHA DESENHADA NA TELA
        self.drawnElements = []
        self.nordal_forces = []
        # ICONE DESENHADA NA TELA
        self.drawn_forces = []
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


class NodalForce(object):
    def __init__(self, fx: float, fy: float, m: float) -> None:
        self.fx = fx
        self.fy = fy
        self.m = m

    def getAsVector(self) -> list:
        return np.array([self.fx, self.fy, self.m])

    def __str__(self) -> str:
        raise NotImplemented


class Node(object):
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.apoio = None
        self.p = 1
        self.__angle = None

    def __str__(self) -> str:
        return "{0},{1}".format(self.x, self.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def setAngle(self, angle: float) -> None:
        self.__angle = angle


class Element(object):
    def __init__(self, node1: Node, node2: Node) -> None:
        if node1 == node2:
            raise RuntimeError(
                "Não é possível criar um elemento com 2 nós iguais!")
        self.node1 = node1
        self.node2 = node2
        self.young_modulus = None
        self.moment_inertia = None
        self.area = None
        self.__section = None
        # ANGULO DADO EM RAD
        self.__angle = None

    def __str__(self) -> str:
        return "Node1={0};Node2={1}".format(self.node1, self.node2)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.node1.x == other.node1.x and self.node1.y == other.node1.y

    def getLength(self) -> float:
        return math.sqrt(math.pow(self.node1.x - self.node2.x, 2) + math.pow(self.node1.y - self.node2.y, 2))

    def getAngle(self) -> float:
        x = self.node1.x
        y = self.node1.y
        # ZERANDO UCS
        n1 = Node(x - x, y - y)
        n2 = Node(self.node2.x - x, self.node2.y - y)
        resposta = None
        deltaX = n1.x - n2.x
        deltaY = n1.y - n2.y
        if deltaX == 0:
            resposta = math.pi/2
        else:
            resposta = math.atan(deltaY/deltaX)
        return resposta

    def getCoefficientElasticity(self) -> float:
        return self.__coefficientElascity

    def setCoefficientElasticity(self, moduloDeElasticidade: float) -> None:
        self.__coefficientElascity = moduloDeElasticidade

    def setSection(self, section: ISection) -> None:
        self.__section = section


class Process(object):
    def __init__(self, nodes: List[Node], elements: List[Node], nodal_force: List[Node]) -> None:
        self.__nodes = nodes
        self.__elements = elements
        self.__nodal_forces = nodal_force
        # DESLOCAMENTO
        self.__nodal_displacement = np.array([])
        self.__deformation = np.array([])
        # ESFORÇOS INTERNOS
        self.__internal_requests = np.array([])
        self.__equilibrium_matrix = np.array([])
        self.__processCalculations()

    def __processCalculations(self):
        # CÁLCULANDO GRAUS DE LIBERDADE
        n_linhas = 3 * len(self.__nodes)
        n_colunas = 3 * len(self.__elements)
        # CONSTRUINDO MATRIZ DE EQUILÍBRIO ZERADA
        equilibrium_matrix = np.zeros((n_linhas, n_colunas))
        # PREENCHENDO MATRIZ DE EQUILÍBRIO COM VALORES
        for element in self.__elements:
            angle = element.getAngle()
            length = element.getLength()
            node_index = self.__nodes.index(element.node1) * 3
            # ENDEREÇO DO ELEMENTO NA MATRIZ DE EQUILIBRIO
            element_index = self.__elements.index(element) * 3
            # CONSTRUINDO RESULTADOS DO NODE1
            equilibrium_matrix[0+node_index, 0+element_index] = -np.cos(angle)
            equilibrium_matrix[0+node_index, 1+element_index] = np.sin(angle)/length
            equilibrium_matrix[0+node_index, 2+element_index] = -np.sin(angle)/length
            equilibrium_matrix[1+node_index, 0+element_index] = -np.sin(angle)
            equilibrium_matrix[1+node_index, 1+element_index] = -np.cos(angle)/length
            equilibrium_matrix[1+node_index, 2+element_index] = np.cos(angle)/length
            # equilibrium_matrix[2+node_index, 0+element_index] = 0 #(já está escrito)
            equilibrium_matrix[2+node_index, 1+element_index] = 1
            equilibrium_matrix[2+node_index, 2+element_index] = 0

            node_index = self.__nodes.index(element.node2) * 3
            # CONSTRUINDO RESULTADOS DO NODE2
            equilibrium_matrix[0+node_index, 0+element_index] = np.cos(angle)
            equilibrium_matrix[0+node_index, 1+element_index] = -np.sin(angle)/length
            equilibrium_matrix[0+node_index, 2+element_index] = np.sin(angle)/length
            equilibrium_matrix[1+node_index, 0+element_index] = np.sin(angle)
            equilibrium_matrix[1+node_index, 1+element_index] = np.cos(angle)/length
            equilibrium_matrix[1+node_index, 2+element_index] = -np.cos(angle)/length
            # equilibrium_matrix[2+node_index, 0+element_index] = 0 #(já está escrito)
            equilibrium_matrix[2+node_index, 1+element_index] = 0
            equilibrium_matrix[2+node_index, 2+element_index] = -1

        self.equilibrium_matrix = equilibrium_matrix

        # CRIANDO MATRIZ DE RIGIDEZ DOS ELEMENTOS
        stifiness_matrix = np.zeros((3*len(self.__elements), 3*len(self.__elements)))
        for i in range(len(self.__elements)):
            young_module = self.__elements[i].young_modulus
            area = self.__elements[i].area
            length = self.__elements[i].getLength()
            p1 = self.__elements[i].node1.p
            p2 = self.__elements[i].node2.p
            moment_inertia = self.__elements[i].moment_inertia
            stifiness_matrix[0 + (3 * i), 0 + (3 * i)] = young_module * area / length
            stifiness_matrix[1 + (3 * i), 1 + (3 * i)] = (3 * p1 / (4 - p1 * p2)) * (4 * young_module * moment_inertia / length)
            stifiness_matrix[1 + (3 * i), 2 + (3 * i)] = (3 * p1 * p2 / (4 - p1 * p2)) * (-2 * young_module * moment_inertia / length)
            stifiness_matrix[2 + (3 * i), 1 + (3 * i)] = (3 * p1 * p2 / (4 - p1 * p2)) * (-2 * young_module * moment_inertia / length)
            stifiness_matrix[2 + (3 * i), 2 + (3 * i)] = (3 * p2 / (4 - p1 * p2)) * (4 * young_module * moment_inertia / length)
        '''
        # IMPLEMENTAR:
        # self.stifiness_matrix = stifiness_matrix
        '''
        # CRIANDO MATRIZ IDENTIDADE RIGIDO-PLASTICA DOS ELEMENTOS
        identity_matrix = np.identity(3*len(self.__elements))

        # Utilizar apenas para o corte da matriz
        # for element in self.__elements:
        #     if element.node1.apoio == Apoio.primeiroGenero:
        #         pass
        #     if element.node1.apoio == Apoio.segundoGenero:
        #         pass
        #     if element.node1.apoio == Apoio.terceiroGenero:
        #         pass
        #     if element.node1.apoio == Apoio.semiRigido:
        #         pass
        #     if element.node1.apoio == Apoio.semApoio:
        #         pass

    def getEquilibriumMatrix(self):
        return self.__equilibrium_matrix

    def getNodalDisplacement(self):
        return self.__nodal_displacement

# ATUALIZAR CONSTRUTOR CLASSE NODE


# BALANÇO
n1 = Node(0, 0)
n2 = Node(10, 0)
n1.p = 1
n2.p = 1
n1.apoio = Apoio.terceiroGenero
n2.apoio = Apoio.semApoio
nodes = [n1, n2]
e1 = Element(n1, n2)
e1.young_modulus = 1
e1.area = 1
e1.moment_inertia = 1
e1.setSection(Retangle(20, 40))
elements = [e1]
nodal_forces = [NodalForce(0, 0, 0), NodalForce(0, -100, 0)]

# TRELIÇA
# n1 = Node(0,0)
# n2 = Node(0.5,math.sin(60*math.pi/180))
# n3 = Node(1,0)
# n1.apoio = Apoio.segundoGenero
# n2.apoio = Apoio.semApoio
# n3.apoio = Apoio.primeiroGenero
# nodes = [n1, n2, n3]
# e1 = Element(n1, n2)
# e2 = Element(n1, n3)
# e3 = Element(n2, n3)
# print(e1.getAngle()*180/math.pi)
# print(e2.getAngle()*180/math.pi)
# print(e3.getAngle()*180/math.pi)
# elements = [e1, e2, e3]
# nodal_forces = []


calc = Process(nodes, elements, nodal_forces)
# print(calc.getNodalDisplacement())
