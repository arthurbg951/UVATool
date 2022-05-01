from typing import Protocol, List, overload, Union, Optional
# from abc import abstractmethod
# from enum import Enum
import numpy
import math
from PyQt5 import QtGui


class Support:
    roller = 0        # PRIMEIRO GENERO
    pinned = 1        # SEGUNDO GENERO
    fixed = 2         # TERCEIRO GENERO
    middle_hinge = 3  # RÓTULA
    semi_fixed = 4    # SEMI RÍGIDO
    no_support = 5    # SEM SUPORTE

# CLASSE SUPPORT EM PORTUGUES


class Apoio:
    primeiro_genero = 0
    segunro_genero = 1
    terceiro_genero = 2
    rotula = 3
    semi_rigido = 4
    sem_suporte = 5


class Analise:
    elastica_via_rigidez_analitica = 0
    rigido_plastica_via_minima_norma_euclidiana = 1


class NodalForce:
    fx: float
    fy: float
    m: float

    def __init__(self, fx: float, fy: float, m: float) -> None:
        self.fx = fx
        self.fy = fy
        self.m = m

    def getAsVector(self) -> list:
        return numpy.array([self.fx, self.fy, self.m])

    def __str__(self) -> str:
        return "{0};{1};{2}".format(self.fx, self.fy, self.m)


class Point2d:
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "({0}, {1})".format(self.x, self.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point2d):
            return NotImplemented
        return self.x == other.x and self.y == other.y


class Node:
    x: float
    y: float
    __nodal_force: NodalForce
    __support: Support
    __p: float
    __displacement: numpy.array
    __angle: float
    __pix_map: QtGui.QPixmap

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.__support = Support.no_support
        self.__p = 1
        self.__nodal_force = NodalForce(0, 0, 0)

    def __str__(self) -> str:
        return "{0},{1}".format(self.x, self.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __checkP(self, p) -> None:
        value = round(p, 2)
        if value >= 4 or value < 0:
            raise ValueError("Node p must be greater or equal to 0 and less then 4.")

    def setP(self, p: float) -> None:
        self.__checkP()
        self.__p = p

    def getP(self) -> float:
        return self.__p

    def setDisplacement(self, displacement: numpy.array) -> None:
        self.__displacement = displacement

    def setAngle(self, angle: float) -> None:
        self.__angle = angle

    def setQPixmap(self, pix_map: QtGui.QPixmap) -> None:
        self.__pix_map = pix_map

    def getQPixmap(self) -> QtGui.QPixmap:
        return self.__pix_map

    def __checkSupport(self, support: Support) -> None:
        test = True
        s1 = Support.fixed
        s2 = Support.middle_hinge
        s3 = Support.no_support
        s4 = Support.semi_fixed
        s5 = Support.roller
        s6 = Support.pinned
        for sup in [s1, s2, s3, s4, s5, s6]:
            if support == sup:
                test = False
        if test:
            raise ValueError("Support needs to be from class Support.")

    def setSupport(self, support: Support) -> None:
        self.__checkSupport(support)
        self.__support = support

    def getSupport(self) -> Support:
        return self.__support

    def setNodalForce(self, nodal_force: NodalForce) -> None:
        if not isinstance(nodal_force, NodalForce):
            raise ValueError("Nodal Force must be from class NodalForce.")
        self.__nodal_force = nodal_force

    def getNodalForce(self) -> NodalForce:
        return self.__nodal_force


class Element:
    node1: Node
    node2: Node
    area: float
    moment_inertia: float
    young_modulus: float
    __deformations: numpy.array
    __stress_resultants: numpy.array
    __angle: float
    __length: float

    def __init__(self, node1: Node, node2: Node, area: float, moment_inertia: float, young_modulus: float) -> None:
        self.node1 = node1
        self.node2 = node2
        self.__verifyNodes()
        self.area = area
        self.moment_inertia = moment_inertia
        self.young_modulus = young_modulus
        self.__angle = self.__setAngle()
        self.__length = self.__setLength()

    def __str__(self) -> str:
        return "Node1={0};Node2={1}".format(self.node1, self.node2)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.node1.x == other.node1.x and self.node1.y == other.node1.y

    def __verifyNodes(self) -> None:
        if self.node1 == self.node2:
            raise ValueError("node1 cant be equal to node2.")

    def getLength(self) -> float:
        return self.__length

    def __setLength(self) -> float:
        return math.sqrt(math.pow(self.node1.x - self.node2.x, 2) + math.pow(self.node1.y - self.node2.y, 2))

    def getAngle(self) -> float:
        return self.__angle

    def __setAngle(self) -> float:
        resposta = None
        # x = self.node1.x
        # y = self.node1.y
        # # ZERANDO UCS
        # n1 = Point2d(x - x, y - y)
        # n2 = Point2d(self.node2.x - x, self.node2.y - y)
        # deltaX = n1.x - n2.x
        # deltaY = n1.y - n2.y
        deltaX = self.node1.x - self.node2.x
        deltaY = self.node1.y - self.node2.y
        if deltaX == 0:
            resposta = math.pi/2
        else:
            resposta = math.atan(deltaY/deltaX)
        return resposta

    def getDeformations(self) -> numpy.array:
        return self.__deformations

    def setDeformations(self, deformations: numpy.array) -> None:
        self.__deformations = deformations

    def getStressResultants(self) -> numpy.array:
        return self.__stress_resultants

    def setStressResultants(self, stress_resultants: numpy.array) -> None:
        self.__stress_resultants = stress_resultants


class Process:
    __nodes: List[Node]
    __elements: List[Element]
    # __nodal_forces: List[NodalForce]
    __analisys: Analise
    __equilibrium: numpy.array
    __equilibrium_cut: numpy.array
    __frame_stiffness: numpy.array
    __global_frame_stiffness: numpy.array
    __displacement: numpy.array
    __deformations: numpy.array
    __stress_resultants: numpy.array

    def __init__(self, nodes: List[Node], elements: List[Element], analisys: Analise) -> None:
        self.__nodes = nodes
        self.__elements = elements
        # self.__nodal_forces = nodal_forces
        self.__analisys = analisys
        self.__processCalculations()

    def __processCalculations(self):
        # CÁLCULANDO GRAUS DE LIBERDADE
        n_linhas = 3 * len(self.__nodes)
        n_colunas = 3 * len(self.__elements)
        # CONSTRUINDO MATRIZ DE EQUILÍBRIO ZERADA
        equilibrium_matrix = numpy.zeros((n_linhas, n_colunas))
        # PREENCHENDO MATRIZ DE EQUILÍBRIO COM VALORES
        for element in self.__elements:
            angle = element.getAngle()
            length = element.getLength()
            node_index = self.__nodes.index(element.node1) * 3
            # ENDEREÇO DO ELEMENTO NA MATRIZ DE EQUILIBRIO
            element_index = self.__elements.index(element) * 3
            # CONSTRUINDO RESULTADOS DO NODE1
            equilibrium_matrix[0+node_index, 0+element_index] = -numpy.cos(angle)
            equilibrium_matrix[0+node_index, 1+element_index] = numpy.sin(angle)/length
            equilibrium_matrix[0+node_index, 2+element_index] = -numpy.sin(angle)/length
            equilibrium_matrix[1+node_index, 0+element_index] = -numpy.sin(angle)
            equilibrium_matrix[1+node_index, 1+element_index] = -numpy.cos(angle)/length
            equilibrium_matrix[1+node_index, 2+element_index] = numpy.cos(angle)/length
            # equilibrium_matrix[2+node_index, 0+element_index] = 0 #(já está escrito)
            equilibrium_matrix[2+node_index, 1+element_index] = 1
            equilibrium_matrix[2+node_index, 2+element_index] = 0

            # ENDEREÇO DO NO NA MATRIZ DE EQUILIBRIO
            node_index = self.__nodes.index(element.node2) * 3
            # CONSTRUINDO RESULTADOS DO NODE2
            equilibrium_matrix[0+node_index, 0+element_index] = numpy.cos(angle)
            equilibrium_matrix[0+node_index, 1+element_index] = -numpy.sin(angle)/length
            equilibrium_matrix[0+node_index, 2+element_index] = numpy.sin(angle)/length
            equilibrium_matrix[1+node_index, 0+element_index] = numpy.sin(angle)
            equilibrium_matrix[1+node_index, 1+element_index] = numpy.cos(angle)/length
            equilibrium_matrix[1+node_index, 2+element_index] = -numpy.cos(angle)/length
            # equilibrium_matrix[2+node_index, 0+element_index] = 0 #(já está escrito)
            equilibrium_matrix[2+node_index, 1+element_index] = 0
            equilibrium_matrix[2+node_index, 2+element_index] = -1

        '''
        # RESULTADO DA MATRIZ DE EQUILIBRIO - [L]
        '''
        self.__equilibrium = equilibrium_matrix

        # CRIANDO MATRIZ DE RIGIDEZ DOS ELEMENTOS
        stifiness_matrix = numpy.zeros((3*len(self.__elements), 3*len(self.__elements)))
        for i in range(len(self.__elements)):
            young_module = self.__elements[i].young_modulus
            area = self.__elements[i].area
            length = self.__elements[i].getLength()
            p1 = self.__elements[i].node1.getP()
            p2 = self.__elements[i].node2.getP()
            moment_inertia = self.__elements[i].moment_inertia
            stifiness_matrix[0 + (3 * i), 0 + (3 * i)] = young_module * area / length
            stifiness_matrix[1 + (3 * i), 1 + (3 * i)] = (3 * p1 / (4 - p1 * p2)) * (4 * young_module * moment_inertia / length)
            stifiness_matrix[1 + (3 * i), 2 + (3 * i)] = (3 * p1 * p2 / (4 - p1 * p2)) * (-2 * young_module * moment_inertia / length)
            stifiness_matrix[2 + (3 * i), 1 + (3 * i)] = (3 * p1 * p2 / (4 - p1 * p2)) * (-2 * young_module * moment_inertia / length)
            stifiness_matrix[2 + (3 * i), 2 + (3 * i)] = (3 * p2 / (4 - p1 * p2)) * (4 * young_module * moment_inertia / length)

        '''
        # RESULTADO DA MATRIZ DE RIGIDEZ (DO ELEMENTO) - [k]
        '''
        self.__frame_stiffness = stifiness_matrix

        # CRIANDO MATRIZ IDENTIDADE RIGIDO-PLASTICA DOS ELEMENTOS
        identity_matrix = numpy.identity(3*len(self.__elements))

        cuts = []
        for element in self.__elements:
            # ENDEREÇO DO ELEMENTO NA MATRIZ DE EQUILIBRIO
            element_index = self.__elements.index(element) * 3
            nodes = [element.node1, element.node2]
            for node in nodes:
                # ENDEREÇO DO NO NA MATRIZ DE EQUILIBRIO
                node_index = self.__nodes.index(node) * 3
                if node.getSupport() == Support.roller:
                    cuts.append(node_index + 1)
                if node.getSupport() == Support.pinned:
                    cuts.append(node_index)
                    cuts.append(node_index + 1)
                if node.getSupport() == Support.fixed:
                    cuts.append(node_index)
                    cuts.append(node_index + 1)
                    cuts.append(node_index + 2)
                if node.getSupport() == Support.semi_fixed:
                    cuts.append(node_index)
                    cuts.append(node_index + 1)
                    cuts.append(node_index + 2)
                if node.getSupport() == Support.no_support:
                    pass

        cuts = list(dict.fromkeys(cuts))
        # print("Endereços do exemplo para corte: {0}".format(cuts))

        """
        # DEEP COPY NA MATRIZ DE EQUILÍBRIO ORIGINAL
        """

        # Matriz de equilíbrio com restrições
        equilibrium_matrix_restriction = equilibrium_matrix.copy()  # Deep Copy
        equilibrium_matrix_restriction = numpy.delete(equilibrium_matrix_restriction, cuts, 0)  # Cut

        # Matriz de equilíbrio transposta com restrições
        equilibrium_matrix_transpose = equilibrium_matrix.copy()  # Deep Copy
        equilibrium_matrix_transpose = equilibrium_matrix_transpose.transpose()  # Transpose
        equilibrium_matrix_transpose = numpy.delete(equilibrium_matrix_transpose, cuts, 1)  # Cut

        """
        # MATRIZ DE RIGIDEZ GLOBAL DO SISTEMA - [K] 
         
        [K] = [l] * [k] * [L.T]
        """
        
        global_frame_stiffnes = equilibrium_matrix_restriction @ stifiness_matrix @ equilibrium_matrix_transpose

        self.__global_frame_stiffness


        """
        # VETOR DOS DESLOCAMENTOS NODAIS - {δ}

        Utilizando a resolução de matriz inversa -> {δ} = [L k LT] ^ -1 * {λ}
        """

        # Criando o vetor das forças nodais
         
        nodal_forces = numpy.zeros((n_linhas))

        for node in self.__nodes:
            force = node.getNodalForce()
            nodal_forces.append(numpy.array([force.fx, force.fy, force.m]))
        
        # Transpondo o vetor das forças para realizar o corte de linhas

        nodal_forces = nodal_forces.transpose()

        nodal_forces = self.__nodal_force

        # Aplicando as restrições dos apoios - corte das linhas

        nodal_forces = numpy.delete(nodal_forces, cuts, 0)


        # RESOLVENDO O SISTEMA LINEAR

        displacement = numpy.linalg.inv(global_frame_stiffnes) @ nodal_forces

        self.__displacement = displacement


        """
        # VETOR DAS DEFORMAÇÕES CORRESPONDENTES - {θ}

            {θ} = [L.T] * {δ}
        """

        deformations = equilibrium_matrix_transpose @ displacement

        self.__deformations = deformations


        """
        Esforços Seccionais Internos - {m}

            {m} = [k] * {θ}
        """

        stress_resultants = stifiness_matrix @ deformations

        self.__stress_resultants = stress_resultants


    def getEquilibriumMatrix(self):
        return self.__equilibrium

    def getFrameStiffness(self):
        return self.__frame_stiffness

    def getGlobalFrameStiffness(self):
        return self.__global_frame_stiffness

    def getNodalDisplacement(self):
        return self.__displacement

    def getDeformations(self):
        return self.__deformations

    def getStressResultants(self):
        return self.__stress_resultants
