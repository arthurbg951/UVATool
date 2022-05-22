from libs.UVATool import *

# DEFININDO PONTOS (NODES)
n1 = Node(0, 0)
n2 = Node(5, 0)
n3 = Node(8, 0)
n4 = Node(3, 0)

# DEFININDO FORÇAS
n2.setNodalForce(NodalForce(0, -10, 0))
n4.setNodalForce(NodalForce(0, -10, -10))

# DEFININDO APOIO
n1.setSupport(Apoio.terceiro_genero)
n2.setSupport(Apoio.primeiro_genero)
n3.setSupport(Apoio.primeiro_genero)

# DEFININDO SEÇÃO
rec = Rectangle(0.001, 0.012)
area = rec.area
momento_inercia = rec.inertia

# DEFININDO ELEMENTOS
e1 = Element(n1, n4, area, momento_inercia, 1)
e2 = Element(n4, n2, area, momento_inercia, 1)
e3 = Element(n2, n3, area, momento_inercia, 1)

nodes = [n1, n4, n2, n3]
elements = [e1, e2, e3]

# REALIZANDO CÁLCULOS
proc = Process(nodes, elements, Analise.elastica.viaRigidezAnalitica)

# PRINTANDO RESULTADOS
plot = Print(proc)
plot.internalForces()
