from lib.UVATool import *
from datetime import datetime

print('Montando estrutura ...')
est_inicio = datetime.now()
nodes = []
elements = []

rec = Rectangle(0.012, 0.001)
area = rec.area
inercia = rec.inertia

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

for i in range(2, 100, 1):
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
est_fim = datetime.now()

print('Processando cálculos ...')
calc = Process(nodes, elements, Analise.elastica.viaRigidezAnalitica)

results = Print(calc)

# PRINTA AS DEFORMAÇÕES (SEM FORMATAÇÃO - sujeito a análise)
# results.nodalDisplacement()

# PRINTA OS ESFORÇOS INTERNOS
results.internalForces()

# PRINTA O TAMANHO DA MATRIZ DE DE RIGIDEZ GLOBAL
print("TAMANHO DA MATRIZ DE RIGIDEZ GLOBAL CORTADA = " , calc.getGlobalFrameStiffness().shape)

# PRINTA OS TEMPOS DECORRIDOS NA EXECUÇÃO DO CÓDIGO
print("TEMPO PARA DEFINIR A ESTRUTURA = ", est_fim - est_inicio)
print("TEMPO DE CALCULO = ", calc.getProcessTime())
