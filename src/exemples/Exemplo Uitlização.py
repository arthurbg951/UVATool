from UVATool import *
from UVATool.Enums import *

# DEFINIR OS NOS
n1 = Node(0, 0)
n2 = Node(0, 6)
n3 = Node(4, 6)
n4 = Node(8, 6)
n5 = Node(8, 3)

# DEFINIR OS APOIOS
n1.setSupport(Apoio.segundo_genero)
n5.setSupport(Apoio.primeiro_genero)

# DEFINIR OS FORÇAS NODAIS
n3.setNodalForce(NodalForce(0, -60, 80))
n4.setNodalForce(NodalForce(40, 0, 0))

# DEFINIR SEÇÃO
rec = Rectangle(0.012, 0.001)
area = rec.area
inercia = rec.inertia

young = 1

# DEFINIR OS ELEMENTOS
e1 = Element(n1, n2, area, inercia, young)
e2 = Element(n2, n3, area, inercia, young)
e3 = Element(n3, n4, area, inercia, young)
e4 = Element(n4, n5, area, inercia, young)

# DEFINIR A LISTA DE NOS E ELEMENTOS PARA CALCULO
nodes = [n1, n2, n3, n4, n5]
elements = [e1, e2, e3, e4]

structure = Structure('EXEMPLO DE UTILIZAÇÃO', nodes, elements)

if __name__ == "__main__":
    # CALCULOS
    calc = Process(nodes, elements, Analise.elastica.viaRigidezAnalitica)

    # MOSTRANDO RESPOSTAS
    plot = Print(calc)
    plot.internalForces()
