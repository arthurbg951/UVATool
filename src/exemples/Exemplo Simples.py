from UVATool import *
from UVATool.Enums import *

# DEFININDO PONTOS (NODES)
n1 = Node(0, 0)
n2 = Node(5, 0)
n3 = Node(8, 0)
n4 = Node(3, 0)
n1 = Node(0, 0)
# DEFININDO FORÇAS
n2.setNodalForce(NodalForce(0, -10_000, 0))
n4.setNodalForce(NodalForce(0, -10_000, -10_000))

# DEFININDO APOIO
n1.setSupport(Apoio.segundo_genero)
n2.setSupport(Apoio.primeiro_genero)
n3.setSupport(Apoio.primeiro_genero)

# DEFININDO SEÇÃO
rec = Rectangle(0.001, 0.012)
area = rec.area
momento_inercia = rec.inertia
young = 1

# DEFININDO ELEMENTOS
e1 = Element(n1, n4, area, momento_inercia, young)
e2 = Element(n4, n2, area, momento_inercia, young)
e3 = Element(n2, n3, area, momento_inercia, young)

nodes = [n1, n4, n2, n3]
elements = [e1, e2, e3]

# DEFININDO ESTRUTURA (UTILIZADO PARA ABRIR UM ARQUIVO E PROCESSA-LO)
struct = Structure('Exemplo de utilização', nodes, elements)

# ESTE IF PREVINE O ARQUIVO DE SER CHAMADO DUAS VEZES AO CARREGAR O ARQUIVO
# EXEMPLO DE UTILIZAÇÃO: 'Process a File.py'
if __name__ == "__main__":
    # REALIZANDO CÁLCULOS
    proc = Process(nodes, elements, Analise.elastica.viaRigidezAnalitica)

    # PRINTANDO RESULTADOS
    plot = Print(proc)
    plot.internalForces()
