from lib.UVATool import *
from traceback import format_exc as error

try:
    n1 = Node(0, 0)
    n2 = Node(1, 0)
    n3 = Node(2, 0)

    n1.setSupport(Apoio.segundo_genero)
    n2.setSupport(Apoio.rotula)
    n3.setSupport(Apoio.primeiro_genero)

    n2.setNodalForce(NodalForce(0, -10, 0))

    e1 = Element(n1, n2, 1, 1, 1)
    e2 = Element(n2, n3, 1, 1, 1)

    nodes = [n1, n2, n3]
    elements = [e1, e2]

    calc = Process(nodes, elements, Analise.elastica_via_rigidez_analitica)

    plot = Print(calc)
    plot.internalForces()

except numpy.linalg.LinAlgError:
    print(error())
    print("O ERRO ESTÁ DEVE SER INVESTIGADO PARA DEMONSTRAR QUE A ESTRUTRURA É HIPOSTÁTICA ...")


