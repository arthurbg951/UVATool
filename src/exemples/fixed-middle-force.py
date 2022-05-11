import sys
sys.path.append('..//..//')
from src.UVATool.UVATool import *

n1 = Node(0, 0)
n2 = Node(2.5, 0)
n3 = Node(5, 0)

n1.setSupport(Apoio.terceiro_genero)
n2.setNodalForce(NodalForce(0, -20_000, 0))

secao = Rectangle(0.012, 0.001)
area = secao.area()
inercia = secao.momentInertia()

e1 = Element(n1, n2, area, inercia, 1)
e2 = Element(n2, n3, area, inercia, 1)

nodes = [n1, n2, n3]
elemets = [e1, e2]

calc = Process(nodes, elemets, Analise.elastica_via_rigidez_analitica)
esforcos_internos = calc.getStressResultants()

for esforco in esforcos_internos:
    print(f"{esforco:.2f}")
