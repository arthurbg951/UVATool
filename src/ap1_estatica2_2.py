from lib.UVATool import *

n1 = Node(0, 0)
n2 = Node(8, 0)
n3 = Node(4, 3)

n1.setSupport(Apoio.segundo_genero)
n2.setSupport(Apoio.primeiro_genero)
n3.setNodalForce(NodalForce(1000, 0, 0))

# rec = Retangle(0.012, 0.001)
# area = rec.area()
# inercia = rec.momentInertia()
# young = 100_000

area = 1
inercia = 1
young = 1

e1 = Element(n1, n2, area, inercia, young)
e2 = Element(n2, n3, area, inercia, young)
e3 = Element(n1, n3, area, inercia, young)

nodes = [n1, n2, n3]
elements = [e1, e2]

calc = Process(nodes, elements, Analise.elastica_via_rigidez_analitica)
deslocamentos = calc.getNodalDisplacement()

# contador = 0
# for node in nodes:
#     suporte = node.getSupport()
#     if suporte == Apoio.sem_suporte:
#         pass
#     if suporte == Apoio.primeiro_genero:
#         contador += 1
#     if suporte == Apoio.segundo_genero:
#         contador += 2
#     if suporte == Apoio.terceiro_genero:
#         contador += 3
#     if suporte == Apoio.semi_rigido:
#         contador += 3
#     print(deslocamentos[contador])

plot = Print(calc)
plot.internalForces()
