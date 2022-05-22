from lib.UVATool import *

rec = Rectangle(0.012, 0.001)
area = rec.area
inercia = rec.inertia
young = 1


def hiperestatica():
    n1 = Node(0, 0)
    n2 = Node(5, 0)
    n3 = Node(10, 0)
    n1.setSupport(Support.fixed)
    n2.setNodalForce(NodalForce(0, -10, 0))
    n3.setSupport(Support.fixed)
    e1 = Element(n1, n2, area, inercia, young)
    e2 = Element(n2, n3, area, inercia, young)
    nodes = [n1, n2, n3]
    elements = [e1, e2]
    return nodes, elements


def semiRigida():
    n1 = Node(0, 0)
    n2 = Node(5, 0)
    n3 = Node(10, 0)
    rigidez = 0.5705
    n1.setSupport(Support.semi_fixed)
    n1.setP(rigidez)
    n2.setNodalForce(NodalForce(0, -10, 0))
    n3.setSupport(Support.semi_fixed)
    n3.setP(rigidez)
    e1 = Element(n1, n2, area, inercia, young)
    e2 = Element(n2, n3, area, inercia, young)
    nodes = [n1, n2, n3]
    elements = [e1, e2]
    return nodes, elements


def isostatica():
    n1 = Node(0, 0)
    n2 = Node(5, 0)
    n3 = Node(10, 0)
    n1.setSupport(Support.pinned)
    n2.setNodalForce(NodalForce(0, -10, 0))
    n3.setSupport(Support.roller)
    e1 = Element(n1, n2, area, inercia, young)
    e2 = Element(n2, n3, area, inercia, young)
    nodes = [n1, n2, n3]
    elements = [e1, e2]
    return nodes, elements


analise = Analise.rigidoPlastica.viaMinimaNormaEuclidiana


print("-----> HIPERESTÁTICA")
nodes, elements = hiperestatica()
proc = Process(nodes, elements, analise)
plot = Print(proc)
plot.internalForces()

print("-----> SEMIRIGIDA")
nodes, elements = semiRigida()
proc = Process(nodes, elements, analise)
plot = Print(proc)
plot.internalForces()

print("-----> ISOSTÁTICA")
nodes, elements = isostatica()
proc = Process(nodes, elements, analise)
plot = Print(proc)
plot.internalForces()
