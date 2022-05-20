from typing import List
import numpy
import math
from datetime import datetime


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
    segundo_genero = 1
    terceiro_genero = 2
    rotula = 3
    semi_rigido = 4

    # SUGESTÃO PARA SOLUCIONAR APOIO SEMI RIGIDO
    sem_suporte = 5
    sem_suporte_semi_rigido = 6


class Analise:
    class elastica:
        viaRigidezAnalitica = 0

    class rigidoPlastica:
        viaMinimaNormaEuclidiana = 1


class Point2d:
    __x: float
    __y: float

    def __init__(self, x: float, y: float) -> None:
        self.__x = x
        self.__y = y

    def __str__(self) -> str:
        return "({0}, {1})".format(self.__x, self.__y)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Point2d):
            return NotImplemented
        return self.x == __o.x and self.y == __o.y

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, value):
        if value is not float or value is not int:
            raise ValueError("x value must be an float number.")
        self.__x = value

    @property
    def y(self) -> float:
        return self.__y

    @x.setter
    def y(self, value):
        if value is not float or value is not int:
            raise ValueError("y value must be an float number.")
        self.__y = value


class Rectangle:
    __b: float
    __h: float
    __area: float
    __inertia: float

    def __init__(self, b: float, h: float) -> None:
        self.__b = b
        self.__h = h

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Rectangle):
            return NotImplemented
        return self.b == __o.b and self.h == __o.h

    @property
    def area(self) -> float:
        return self.__b * self.__h

    @property
    def inertia(self) -> float:
        return self.__b * math.pow(self.__h, 3) / 12

    @property
    def b(self):
        return self.__b

    @b.setter
    def b(self, value):
        if value is not float:
            raise ValueError("b must be an float number.")
        else:
            self.__b = value

    @property
    def h(self):
        return self.__h

    @h.setter
    def h(self, value):
        if value is not float:
            raise ValueError("h must be an float number.")
        else:
            self.__h = value


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


class Node:
    x: float
    y: float
    __nodal_force: NodalForce
    __support: Support
    __p: float

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

    def __checkP(self, p) -> float:
        if p == 0:
            p = 1e-31
        if p >= 4:
            raise ValueError("P must be less than 4")
        if p < 0:
            raise ValueError("P must be greater than or equal to 0")
        return p

    def setP(self, p: float) -> None:
        if p == 0:
            self.__support = Support.middle_hinge
        elif p != 1:
            self.__support = Support.semi_fixed
        p = self.__checkP(p)
        self.__p = p

    def getP(self) -> float:
        return self.__p

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
        if support == Support.middle_hinge:
            self.setP(0)
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
    # __deformations: numpy.array
    __internal_forces: numpy.array
    __angle: float
    __length: float
    __p1: float
    __p2: float

    def __init__(self, node1: Node, node2: Node, area: float, moment_inertia: float, young_modulus: float) -> None:
        self.node1 = node1
        self.node2 = node2
        self.__verifyNodes()
        self.area = area
        self.moment_inertia = moment_inertia
        self.young_modulus = young_modulus
        self.__angle = self.__setAngle()
        self.__length = self.__setLength()
        self.__p1 = node1.getP()
        self.__p2 = node2.getP()

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
        deltaX = self.node1.x - self.node2.x
        deltaY = self.node1.y - self.node2.y
        if deltaX == 0:
            resposta = math.pi/2
        else:
            resposta = math.atan(deltaY/deltaX)
        return resposta

    # def getDeformations(self) -> numpy.array:
    #     return self.__deformations

    def setDeformations(self, deformations: numpy.array) -> None:
        self.__deformations = deformations

    def getInternalForces(self) -> numpy.array:
        return self.__internal_forces

    def setInternalForces(self, internal_forces: numpy.array) -> None:
        self.__internal_forces = internal_forces

    def setP(self, p1: float, p2: float) -> None:
        self.__p1 = p1
        self.__p2 = p2

    def getP(self) -> list:
        return [self.__p1, self.__p2]


class Process:
    __nodes: List[Node]
    __elements: List[Element]
    # __nodal_forces: List[NodalForce]
    __analisys: Analise
    __equilibrium: numpy.array
    __equilibrium_cut_transpose: numpy.array
    __frame_stiffness: numpy.array
    __global_frame_stiffness: numpy.array
    __displacement: numpy.array
    __deformations: numpy.array
    __internal_forces: numpy.array
    __cuts: list
    __process_time: datetime

    def __init__(self, nodes: List[Node], elements: List[Element], analisys: Analise) -> None:
        self.__nodes = nodes
        self.__elements = elements
        # self.__nodal_forces = nodal_forces
        self.__analisys = analisys
        inicio = datetime.now()
        self.__processCalculations()
        fim = datetime.now()
        self.__process_time = fim - inicio

    def __getEquilibriumMatrix(self) -> numpy.array:
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
        return equilibrium_matrix

    def __getFrameStiffnessMatrix(self) -> numpy.array:
        # CRIANDO MATRIZ DE RIGIDEZ DOS ELEMENTOS
        stifiness_matrix = numpy.zeros((3*len(self.__elements), 3*len(self.__elements)))
        for i in range(len(self.__elements)):
            young_module = self.__elements[i].young_modulus
            area = self.__elements[i].area
            length = self.__elements[i].getLength()

            pno1 = self.__elements[i].node1.getP()
            pno2 = self.__elements[i].node2.getP()
            pele1 = self.__elements[i].getP()[0]
            pele2 = self.__elements[i].getP()[1]

            p1 = None
            p2 = None
            if pno1 > pele1 or pno2 > pele2:
                p1 = pele1
                p2 = pele2
            else:
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
        return stifiness_matrix

    def __getCuts(self) -> list:
        cuts = []
        for element in self.__elements:
            element_index = self.__elements.index(element) * 3
            nodes = [element.node1, element.node2]
            for node in nodes:
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
        self.__cuts = cuts

    def __getGlobalFrameStiffnessMatrix(self) -> numpy.array:
        self.__getCuts()
        """
        # DEEP COPY NA MATRIZ DE EQUILÍBRIO ORIGINAL
        """
        # Matriz de equilíbrio com restrições
        equilibrium_matrix_restriction = self.__equilibrium.copy()  # Deep Copy
        equilibrium_matrix_restriction = numpy.delete(equilibrium_matrix_restriction, self.__cuts, 0)  # Cut
        shapeX = equilibrium_matrix_restriction.shape[0]
        shapeY = equilibrium_matrix_restriction.shape[1]
        if shapeX > shapeY:
            raise ValueError("ESTRUTURA HIPOSTÁTICA")
        # Matriz de equilíbrio transposta com restrições
        equilibrium_matrix_transpose = self.__equilibrium.copy()  # Deep Copy
        equilibrium_matrix_transpose = equilibrium_matrix_transpose.transpose()  # Transpose
        equilibrium_matrix_transpose = numpy.delete(equilibrium_matrix_transpose, self.__cuts, 1)  # Cut
        self.__equilibrium_cut_transpose = equilibrium_matrix_transpose
        """
        # MATRIZ DE RIGIDEZ GLOBAL DO SISTEMA - [K] 
         
        [K] = [l] * [k] * [L.T]
        """
        aux1 = numpy.dot(equilibrium_matrix_restriction, self.__frame_stiffness)
        global_frame_stiffnes = numpy.dot(aux1, equilibrium_matrix_transpose)
        return global_frame_stiffnes

    def __getNodalForcesVector(self) -> numpy.array:
        self.__getCuts()
        """
        # VETOR DOS DESLOCAMENTOS NODAIS - {δ}

        Utilizando a resolução de matriz inversa -> {δ} = [L k LT] ^ -1 * {λ}
        """
        # Criando o vetor das forças nodais
        nodal_forces = numpy.array([])
        for node in self.__nodes:
            force = node.getNodalForce()
            forces = numpy.array([force.fx, force.fy, force.m])
            nodal_forces = numpy.append(nodal_forces, forces)
        # Transpondo o vetor das forças para realizar o corte de linhas
        nodal_forces = nodal_forces.transpose()
        # Aplicando as restrições dos apoios - corte das linhas
        nodal_forces = numpy.delete(nodal_forces, self.__cuts, 0)
        return nodal_forces

    def __getDisplacement(self) -> numpy.array:
        # RESOLVENDO O SISTEMA LINEAR
        displacement = numpy.linalg.inv(self.__global_frame_stiffness) @ self.__nodal_force
        return displacement

    def __getDeformations(self) -> numpy.array:
        """
        # VETOR DAS DEFORMAÇÕES CORRESPONDENTES - {θ}

            {θ} = [L.T] * {δ}
        """
        deformations = self.__equilibrium_cut_transpose @ self.__displacement
        return deformations

    def __getInternalForces(self) -> numpy.array:
        """
        Esforços Seccionais Internos - {m}

            {m} = [k] * {θ}
        """
        stress_resultants = self.__frame_stiffness @ self.__deformations
        return stress_resultants

    def __getIdentity(self) -> numpy.array:
        return numpy.identity(3*len(self.__elements))

    def __processCalculations(self):
        self.__equilibrium = self.__getEquilibriumMatrix()
        if self.__analisys == Analise.rigidoPlastica.viaMinimaNormaEuclidiana:
            self.__frame_stiffness = self.__getIdentity()
        else:
            self.__frame_stiffness = self.__getFrameStiffnessMatrix()
        self.__global_frame_stiffness = self.__getGlobalFrameStiffnessMatrix()
        self.__nodal_force = self.__getNodalForcesVector()
        self.__displacement = self.__getDisplacement()
        self.__deformations = self.__getDeformations()
        self.__internal_forces = self.__getInternalForces()

    def getEquilibriumMatrix(self) -> numpy.array:
        return self.__equilibrium

    def getFrameStiffness(self) -> numpy.array:
        return self.__frame_stiffness

    def getGlobalFrameStiffness(self) -> numpy.array:
        return self.__global_frame_stiffness

    def getNodalDisplacement(self) -> numpy.array:
        return self.__displacement

    def getDeformations(self) -> numpy.array:
        return self.__deformations

    def getInternalForces(self) -> numpy.array:
        return self.__internal_forces

    def getProcessTime(self) -> datetime:
        return self.__process_time

    def getCuts(self) -> list:
        return self.__cuts

    # NÃO ESTÁ FUNCIONANDO CORRETAMENTE
    # def matrixToCsv(self, file_name: str, matrix: numpy.array):
    #     # criar função para criar matrizes no exel
    #     file = open("{0}.csv".format(file_name), "w")
    #     linhas = matrix.shape[0]
    #     colunas = matrix.shape[1]
    #     print(linhas, colunas)
    #     linha = list()
    #     for i in range(linhas):
    #         for j in range(colunas):
    #             linha.append("{0},".format(matrix[i, j]))
    #         linha.append("\n")
    #     file.writelines(linha)


class Print:
    __process: Process

    def __init__(self, process: Process) -> None:
        self.__process = process

    def internalForces(self) -> None:
        for i in range(0, len(self.__process.getInternalForces()), 3):
            print('ELEMENT: {0}'.format(int(i/3+1)))
            print(" N={0:.2f}".format(self.__process.getInternalForces()[0 + i]))
            print("M1={0:.2f}".format(self.__process.getInternalForces()[1 + i]))
            print("M2={0:.2f}".format(self.__process.getInternalForces()[2 + i]))
            print()

    def nodalDisplacement(self):
        deformacoes = self.__process.getNodalDisplacement()
        for deformacao in deformacoes:
            print(f"{deformacao:.6f}")
