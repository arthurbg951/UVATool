from UVATool.UVATool import *

n1 = Node(0, 0)
n2 = Node(5, 0)
n3 = Node(6, 0)

n1.setSupport(Apoio.segundo_genero)
n2.setSupport(Apoio.primeiro_genero)
n3.setNodalForce(NodalForce(0, -100, 0))

e1 = Element(n1, n2, 1, 1, 1)
e2 = Element(n2, n3, 1, 1, 1)

nodes = [n1, n2, n3]
elements = [e1, e2]

proc = Process(nodes, elements, Analise.elastica_via_rigidez_analitica)

plot = Print(proc)
plot.internalForces()