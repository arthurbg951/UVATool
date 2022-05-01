
from UVATool import *

# DEFININDO PONTOS (NODES)
n1 = Node(0, 0)
n2 = Node(5, 0)
n3 = Node(8, 0)
n4 = Node(3, 0)

# DEFININDO FORÇAS
n2.setNodalForce(NodalForce(0, -10, 0))
n4.setNodalForce(NodalForce(0, -10, -10))

# DEFININDO APOIO
n1.setSupport(Apoio.segundo_genero)
n2.setSupport(Apoio.primeiro_genero)
n3.setSupport(Apoio.primeiro_genero)

# DEFININDO SEÇÃO
rec = Retangle(1, 12)
area = rec.area()
momento_inercia = rec.momentInertia()

# DEFININDO ELEMENTOS
e1 = Element(n1, n4, area, momento_inercia, 1)
e2 = Element(n4, n2, area, momento_inercia, 1)
e3 = Element(n2, n3, area, momento_inercia, 1)

nodes = [n1, n4, n2, n3]
elements = [e1, e2, e3]

# REALIZANDO CÁLCULOS
proc = Process(nodes, elements, Analise.elastica_via_rigidez_analitica)

# ARMAZENANDO RESULTADOS
esforcos_internos = proc.getStressResultants()

# PRINTANDO RESULTADOS
for i in range(0, len(esforcos_internos), 3):
    print(" N[{0}]={1:.2f}".format(int(i/3+1), esforcos_internos[0 + i]))
    print("M1[{0}]={1:.2f}".format(int(i/3+1), esforcos_internos[1 + i]))
    print("M2[{0}]={1:.2f}".format(int(i/3+1), esforcos_internos[2 + i]))
