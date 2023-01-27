import numpy
from datetime import datetime
from UVATool.Node import Node
from UVATool.Element import Element
from UVATool.Enums.Analise import Analise
from UVATool.Enums.Support import Support
from UVATool.Exceptions.StructureError import StructureError


class Process:
    '''
    ## Class who implement Displacement Method
    ### analisys={0,1} default=0

    0 = Analytical Rigidity Method

    1 = Minimum Euclidean Norm

    verbose param shows the steps being performed default=False
    '''
    __nodes: list[Node]
    __elements: list[Element]
    __analisys: Analise
    __equilibrium: numpy.array
    __equilibrium_cut_transpose: numpy.array
    __frame_stiffness: numpy.array
    __global_frame_stiffness: numpy.array
    __displacement: numpy.array
    __deformations: numpy.array
    __internal_forces: numpy.array
    __cuts: list
    __nodeSemiFixedCuts: list
    __elementSemiFixedCuts: list
    __process_time: datetime

    def __init__(self, nodes: list[Node], elements: list[Element], analisys: Analise=Analise.elastica.viaRigidezAnalitica, verbose=False) -> None:
        self.__nodes = nodes
        self.__elements = elements
        self.__analisys = analisys
        self.__nodeSemiFixedCuts = []
        self.__elementSemiFixedCuts = []
        self.__verifySemiFixedSupport()
        self.__processCalculations()
        self.__removeSemiFixedParts()
        if verbose:
            print("WARNING!! Verbose method not working yet.")

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
            raise StructureError("ESTRUTURA HIPOSTÁTICA")
        # Matriz de equilíbrio transposta com restrições
        equilibrium_matrix_transpose = self.__equilibrium.copy()  # Deep Copy
        equilibrium_matrix_transpose = equilibrium_matrix_transpose.transpose()  # Transpose
        equilibrium_matrix_transpose = numpy.delete(equilibrium_matrix_transpose, self.__cuts, 1)  # Cut
        self.__equilibrium_cut_transpose = equilibrium_matrix_transpose
        
        aux1 = numpy.dot(equilibrium_matrix_restriction, self.__frame_stiffness)
        global_frame_stiffnes = numpy.dot(aux1, equilibrium_matrix_transpose)
        return global_frame_stiffnes

    def __getNodalForcesVector(self) -> numpy.array:
        self.__getCuts()
        
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
        deformations = self.__equilibrium_cut_transpose @ self.__displacement
        return deformations

    def __getInternalForces(self) -> numpy.array:
        stress_resultants = self.__frame_stiffness @ self.__deformations
        return stress_resultants

    def __getIdentity(self) -> numpy.array:
        return numpy.identity(3*len(self.__elements))

    def __verifySemiFixedSupport(self):
        haveSemiFixedSupport = False
        for node in self.__nodes:
            if node.getSupport() == Support.semi_fixed:
                haveSemiFixedSupport = True
                break
        if haveSemiFixedSupport:
            nodePosCorrection = 0
            elemPosCorrection = 0
            for elemIndex in range(len(self.__elements)):
                node1 = Node(self.__elements[elemIndex].node1.x, self.__elements[elemIndex].node1.y)
                node2 = Node(self.__elements[elemIndex].node2.x, self.__elements[elemIndex].node2.y)
                node1HaveSupport = False
                node2HaveSupport = False
                naux1 = None
                naux2 = None
                if node1.getSupport() == Support.semi_fixed:
                    node1HaveSupport = True
                    nodePos = self.__nodes.index(node1, 0, len(self.__nodes)) + nodePosCorrection
                    self.__nodeSemiFixedCuts.append(self.__nodes.index(node1, 0, len(self.__nodes)))
                    naux1 = Node(node1.x, node1.y - 1e-31)
                    naux1.setSupport(Support.fixed)
                    self.__nodes.insert(nodePos, naux1)
                    node1.setSupport(Support.no_support)
                    nodePosCorrection += 1

                if node2.getSupport() == Support.semi_fixed:
                    node2HaveSupport = True
                    nodePos = self.__nodes.index(node2, 0, len(self.__nodes)) + 1 + nodePosCorrection
                    print(nodePos)
                    self.__nodeSemiFixedCuts.append(self.__nodes.index(node2, 0, len(self.__nodes)) + 1)
                    naux2 = Node(node2.x, node2.y - 1e-31)
                    naux2.setSupport(Support.fixed)
                    if nodePos < len(self.__nodes):
                        self.__nodes.insert(nodePos, naux2)
                    else:
                        self.__nodes.append(naux2)
                    node2.setSupport(Support.no_support)
                    nodePosCorrection += 1

                if node1HaveSupport:
                    elem = Element(naux1, node1, 1, 1, 1)
                    self.__elements.insert(elemIndex + elemPosCorrection, elem)
                    elemPosCorrection += 1
                    self.__elementSemiFixedCuts.append(elemIndex)
                if node2HaveSupport:
                    elem = Element(naux2, node2, 1, 1, 1)
                    if elemIndex < len(self.__elements):
                        self.__elements.insert(elemIndex + elemPosCorrection, elem)
                    else:
                        self.__elements.append(elem)
                    elemPosCorrection += 1
                    self.__elementSemiFixedCuts.append(elemIndex + 1)

    def __removeSemiFixedParts(self):
        # SUJEITO A ALTERAÇÕES - NÃO FINALIZADO
        if self.__nodeSemiFixedCuts != [] and self.__elementSemiFixedCuts != []:
            for i in reversed(range(0, len(self.__internal_forces))):
                if self.__elementSemiFixedCuts.__contains__(i):
                    self.__internal_forces = numpy.delete(self.__internal_forces, [[0 + i], [1 + i], [2 + i]])

    def __processCalculations(self):
        inicio = datetime.now()
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
        fim = datetime.now()
        self.__process_time = fim - inicio

    def getEquilibriumMatrix(self) -> numpy.array:
        '''
        ## MATRIZ DE EQUILIBRIO - [L]
        '''
        return self.__equilibrium

    def getFrameStiffness(self) -> numpy.array:
        '''
        ## MATRIZ DE RIGIDEZ (DO ELEMENTO) - [k]
        '''
        return self.__frame_stiffness

    def getGlobalFrameStiffness(self) -> numpy.array:
        """
        ## MATRIZ DE RIGIDEZ GLOBAL DO SISTEMA - [K]

        [K] = [l] * [k] * [L.T]
        """
        return self.__global_frame_stiffness

    def getNodalDisplacement(self) -> numpy.array:
        """
        ## VETOR DOS DESLOCAMENTOS NODAIS - {δ}

        Utilizando a resolução de matriz inversa -> {δ} = [L k LT] ^ -1 * {λ}
        """
        return self.__displacement

    def getDeformations(self) -> numpy.array:
        """
        ## VETOR DAS DEFORMAÇÕES CORRESPONDENTES - {θ}

            {θ} = [L.T] * {δ}
        """
        return self.__deformations

    def _getNodalForces(self) -> numpy.array:
        return self.__nodal_force

    def getInternalForces(self) -> numpy.array:
        """
        ## Esforços Seccionais Internos - {m}

            {m} = [k] * {θ}
        """
        return self.__internal_forces

    def getProcessTime(self) -> datetime:
        """
        ## Return the time processing calculations
        """
        return self.__process_time

    def getCuts(self) -> list:
        """
        ## Return positions removed in Equilibrium Matrix
        """
        return self.__cuts
