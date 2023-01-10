from UVATool import *
from UVATool.Enums import *


def biEngastada():
    n1 = Node(0, 0)
    n2 = Node(2, 0)
    n3 = Node(6, 0)
    n4 = Node(8, 0)

    rigidez = 1
    n1.setSupport(Apoio.terceiro_genero)
    n1.setP(rigidez)
    n4.setSupport(Apoio.terceiro_genero)
    n4.setP(rigidez)

    n2.setNodalForce(NodalForce(0, -10, 0))
    n3.setNodalForce(NodalForce(0, -10, 0))

    rec = Rectangle(0.012, 0.001)
    area = rec.area
    inercia = rec.inertia

    e1 = Element(n1, n2, area, inercia, 1)
    e2 = Element(n2, n3, area, inercia, 1)
    e3 = Element(n3, n4, area, inercia, 1)

    nodes = [n1, n2, n3, n4]
    elements = [e1, e2, e3]
    return nodes, elements


nodes, elements = biEngastada()

print("ANALISE ELASTICA VIA RIGIDEZ ANALITICA")
proc = Process(nodes, elements, Analise.elastica.viaRigidezAnalitica)
plot = Print(proc)
plot.internalForces()

print("ANALISE RIGIDO PLASTICA VIA MINIMA NORMA EUCLIDIANA")
proc = Process(nodes, elements,
               Analise.rigidoPlastica.viaMinimaNormaEuclidiana)
plot = Print(proc)
plot.internalForces()
