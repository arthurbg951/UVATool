from UVATool import *
from datetime import datetime

inicio = datetime.now()

nodes = []
elements = []

rec = Retangle(12, 1)
area = rec.area()
inercia = rec.momentInertia()

n1 = Node(0, 0)
n1.setSupport(Apoio.terceiro_genero)
n2 = Node(0, 1)
n3 = Node(1, 1)
n4 = Node(1, 0)
n4.setSupport(Apoio.terceiro_genero)

e1 = Element(n1, n2, area, inercia, 1)
e2 = Element(n2, n3, area, inercia, 1)
e3 = Element(n3, n4, area, inercia, 1)

nodes.append(n1)
nodes.append(n2)
nodes.append(n3)
nodes.append(n4)

elements.append(e1)
elements.append(e2)
elements.append(e3)

for i in range(2, 1000, 1):
    n2, n3 = Node(0, i), Node(1, i)

    e1 = Element(nodes[len(nodes)-4], n2, area, inercia, 1)
    e2 = Element(n2, n3, area, inercia, 1)
    e3 = Element(n3, nodes[len(nodes)-1], area, inercia, 1)

    nodes.append(n2)
    nodes.append(n3)
    elements.append(e1)
    elements.append(e2)
    elements.append(e3)

nodes[len(nodes)-2].setNodalForce(NodalForce(-100, 0, 0))

print('iniciando calculos')
calc = Process(nodes, elements, Analise.elastica_via_rigidez_analitica)
esforcos = calc.getStressResultants()
print(calc.getGlobalFrameStiffness().shape)

# for i in range(0, len(calc.getStressResultants()), 3):
#     # print(" N[{0}]={1:.2f}".format(int(i/3+1), proc.getStressResultants()[0 + i]))
#     print("M1[{0}]={1:.2f}".format(int(i/3+1), calc.getStressResultants()[1 + i]))
#     print("M2[{0}]={1:.2f}".format(int(i/3+1), calc.getStressResultants()[2 + i]))
#     print()

fim = datetime.now()
print("TEMPO DE CALCULO = ", fim - inicio)
