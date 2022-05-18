from lib.UVATool import *

n1 = Node(0, 0)
n2 = Node(2.5, 0)
n3 = Node(5, 0)

n1.setSupport(Apoio.terceiro_genero)
n2.setNodalForce(NodalForce(0, -20, 0))

e1 = Element(n1, n2, 1, 1, 1)
e2 = Element(n2, n3, 1, 1, 1)

nodes = [n1, n2, n3]
elemets = [e1, e2]

calc = Process(nodes, elemets, Analise.elastica.viaRigidezAnalitica)

results = Print(calc)
results.nodalDisplacement()
