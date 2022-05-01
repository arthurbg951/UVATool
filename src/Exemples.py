from UVATool import Node, Element, Support, Analise, NodalForce, Process
from datetime import datetime
import math

print("A execução comecou em {0}\n".format(datetime.now()))
nodes = []
elements = []

# BALANÇO
n1 = Node(0, 0)
n1.setSupport(Support.fixed)
n2 = Node(10, 0)
n2.setNodalForce(NodalForce(0, -100, 0))
nodes = [n1, n2]
e1 = Element(n1, n2, 1, 1, 1)
elements = [e1]

# TRELIÇA
# n1 = Node(0, 0)
# n1.setSupport(Support.pinned)
# n2 = Node(0.5, math.sin(60*math.pi/180))
# n3 = Node(1, 0)
# n3.setSupport(Support.roller)
# nodes = [n1, n2, n3]
# e1 = Element(n1, n2, 1, 1, 1)
# e2 = Element(n2, n3, 1, 1, 1)
# e3 = Element(n1, n3, 1, 1, 1)
# elements = [e1, e2, e3]

# EDIFICIO DE 3 ANDARES
# n1 = Node(0, 0)
# n1.setSupport(Support.pinned)
# n2 = Node(15, 0)
# n2.setSupport(Support.roller)
# n3 = Node(0, 3)
# n3.setNodalForce(NodalForce(100, 0, 0))
# n4 = Node(15, 3)
# n5 = Node(0, 6)
# n5.setNodalForce(NodalForce(100, 0, 0))
# n6 = Node(15, 6)
# n7 = Node(0, 9)
# n7.setNodalForce(NodalForce(100, 0, 0))
# n8 = Node(15, 9)
# nodes = [n1, n2, n3, n4, n5, n6, n7, n8]
# e1 = Element(n1, n3, 1, 1, 1)
# e2 = Element(n2, n4, 1, 1, 1)
# e3 = Element(n3, n4, 1, 1, 1)
# e4 = Element(n3, n5, 1, 1, 1)
# e5 = Element(n4, n6, 1, 1, 1)
# e6 = Element(n5, n6, 1, 1, 1)
# e7 = Element(n5, n7, 1, 1, 1)
# e8 = Element(n6, n8, 1, 1, 1)
# e9 = Element(n7, n8, 1, 1, 1)
# elements = [e1, e2, e3, e4, e5, e6]

proc = Process(nodes, elements, Analise.elastica_via_rigidez_analitica)
print("MATRIZ DE EQUILIBRIO - [L]\n",proc.getEquilibriumMatrix(), "\n")
print("MATRIZ DE RIGIDEZ (DO ELEMENTO) - [k]\n",proc.getFrameStiffness(), "\n")
print("RIGIDEZ GLOBAL DO SISTEMA - [K]\n",proc.getNodalDisplacement(), "\n")
print("VETOR DOS DESLOCAMENTOS NODAIS - {δ}\n",proc.getDeformations(),"\n")
print("DEFORMAÇÕES CORRESPONDENTES - {θ}\n",proc.getStressResultants(),"\n")
# print("Esforços Seccionais Internos - {m}", proc.getse)
print("A execução terminou em {0}".format(datetime.now()))
