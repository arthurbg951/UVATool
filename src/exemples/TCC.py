from UVATool import *
from UVATool.Enums import *
'''  
ESTUDO DA LIGAÇÃO VIGA PILAR

TRABALHO DE CONCLUSÃO DE CURSO
'''

# Materiais ----------------------------------------------------------------------------------
secao_p = Rectangle(0.2, 0.8)  # hy x hx
area_p = secao_p.area
inercia_p = secao_p.inertia
secao_v = Rectangle(0.15, 0.6)  # base x altura
area_v = secao_v.area
inercia_v = secao_v.inertia
young = 27e9
'''
----------------------------------------------------------------------------------------------
EXEMPLO (A)

Viga em balanço


ATENÇÃO: Inserir todos os valores no sistema internacional de unidades (SI)
----------------------------------------------------------------------------------------------
'''

print('\n\nEXEMPLO (A)')

# Nós ----------------------------------------------------------------------------------------
n1 = Node(0, 0)
n2 = Node(0, 3)
n3 = Node(2, 3)

# Apoios -------------------------------------------------------------------------------------
n1.setSupport(Apoio.terceiro_genero)

# Fator Pi -----------------------------------------------------------------------------------
n2.setP(1)

# Cargas -------------------------------------------------------------------------------------
n3.setNodalForce(NodalForce(0, -10e3, 0))

# Definição dos elementos  -------------------------------------------------------------------
e1 = Element(n1, n2, area_p, inercia_p, young)
e2 = Element(n2, n3, area_v, inercia_v, young)

nodes = [n1, n2, n3]
elements = [e1, e2]

calc = Process(nodes, elements, Analise.viaRigidezAnalitica)
plot = Print(calc)
# plot.internalForces()
# plot.nodalDisplacement()
# plot.elementDeformations()
'''
----------------------------------------------------------------------------------------------
EXEMPLO (B)

Viga em balanço 3 pisos

ATENÇÃO: Inserir todos os valores no sistema internacional de unidades (SI)
----------------------------------------------------------------------------------------------
'''

print('\n\nEXEMPLO (B)')

# Nós ----------------------------------------------------------------------------------------
n1 = Node(0, 0)
n2 = Node(0, 3)
n3 = Node(2, 3)
n4 = Node(0, 6)
n5 = Node(2, 6)
n6 = Node(0, 9)
n7 = Node(2, 9)

# Apoios -------------------------------------------------------------------------------------
n1.setSupport(Apoio.terceiro_genero)

# Cargas -------------------------------------------------------------------------------------
n3.setNodalForce(NodalForce(0, -10e3, 0))
n5.setNodalForce(NodalForce(0, -10e3, 0))
n7.setNodalForce(NodalForce(0, -10e3, 0))

# Definição dos elementos  -------------------------------------------------------------------
e1 = Element(n1, n2, area_p, inercia_p, young)
e2 = Element(n2, n4, area_p, inercia_p, young)
e3 = Element(n4, n6, area_p, inercia_p, young)
e4 = Element(n2, n3, area_v, inercia_v, young)
e5 = Element(n4, n5, area_v, inercia_v, young)
e6 = Element(n6, n7, area_v, inercia_v, young)

# Fator Pi -----------------------------------------------------------------------------------
e4.setP(1, 1)
e5.setP(1, 1)
e6.setP(1, 1)

nodes = [n1, n2, n3, n4, n5, n6, n7]
elements = [e1, e2, e3, e4, e5, e6]

calc = Process(nodes, elements, Analise.viaRigidezAnalitica)
plot = Print(calc)
# plot.internalForces()
# plot.nodalDisplacement()
# plot.elementDeformations()
'''
----------------------------------------------------------------------------------------------
EXEMPLO (C)

pórtico

ATENÇÃO: Inserir todos os valores no sistema internacional de unidades (SI)
----------------------------------------------------------------------------------------------
'''
print('\n\nEXEMPLO (C)')

# Nós ----------------------------------------------------------------------------------------
n1 = Node(0, 0)
n2 = Node(0, 3)
n3 = Node(2, 3)
n4 = Node(4, 3)
n5 = Node(6, 3)
n6 = Node(6, 0)

# Apoios -------------------------------------------------------------------------------------
n1.setSupport(Apoio.terceiro_genero)
n6.setSupport(Apoio.terceiro_genero)

# Fator Pi -----------------------------------------------------------------------------------
n2.setP(1)
n5.setP(1)

# Cargas -------------------------------------------------------------------------------------
n3.setNodalForce(NodalForce(0, -10e3, 0))
n4.setNodalForce(NodalForce(0, -10e3, 0))

# Definição dos elementos  -------------------------------------------------------------------
e1 = Element(n1, n2, area_p, inercia_p, young)
e2 = Element(n2, n3, area_v, inercia_v, young)
e3 = Element(n3, n4, area_v, inercia_v, young)
e4 = Element(n4, n5, area_v, inercia_v, young)
e5 = Element(n5, n6, area_p, inercia_p, young)

nodes = [n1, n2, n3, n4, n5, n6]
elements = [e1, e2, e3, e4, e5]

# Resultados ---------------------------------------------------------------------------------
calc = Process(nodes, elements)
plot = Print(calc)
# plot.internalForces()
# plot.nodalDisplacement()
# plot.elementDeformations()
'''
----------------------------------------------------------------------------------------------
EXEMPLO (D)

pórtico 3 pisos

ATENÇÃO: Inserir todos os valores no sistema internacional de unidades (SI)
----------------------------------------------------------------------------------------------
'''
print('\n\nEXEMPLO (D)')

# Nós ----------------------------------------------------------------------------------------
n1 = Node(0, 0)
n2 = Node(0, 3)
n3 = Node(2, 3)
n4 = Node(4, 3)
n5 = Node(6, 3)
n6 = Node(6, 0)

n7 = Node(0, 6)
n8 = Node(2, 6)
n9 = Node(4, 6)
n10 = Node(6, 6)

n11 = Node(0, 9)
n12 = Node(2, 9)
n13 = Node(4, 9)
n14 = Node(6, 9)

# Apoios -------------------------------------------------------------------------------------
n1.setSupport(Apoio.terceiro_genero)
n6.setSupport(Apoio.terceiro_genero)

# Cargas -------------------------------------------------------------------------------------
n3.setNodalForce(NodalForce(0, -10e3, 0))
n4.setNodalForce(NodalForce(0, -10e3, 0))

n8.setNodalForce(NodalForce(0, -10e3, 0))
n9.setNodalForce(NodalForce(0, -10e3, 0))

n12.setNodalForce(NodalForce(0, -10e3, 0))
n13.setNodalForce(NodalForce(0, -10e3, 0))

# Definição dos elementos  -------------------------------------------------------------------
e1 = Element(n1, n2, area_p, inercia_p, young)
e2 = Element(n2, n3, area_v, inercia_v, young)
e3 = Element(n3, n4, area_v, inercia_v, young)
e4 = Element(n4, n5, area_v, inercia_v, young)
e5 = Element(n6, n5, area_p, inercia_p, young)

e6 = Element(n2, n7, area_p, inercia_p, young)
e7 = Element(n7, n8, area_v, inercia_v, young)
e8 = Element(n8, n9, area_v, inercia_v, young)
e9 = Element(n9, n10, area_v, inercia_v, young)
e10 = Element(n5, n10, area_p, inercia_p, young)

e11 = Element(n7, n11, area_p, inercia_p, young)
e12 = Element(n11, n12, area_v, inercia_v, young)
e13 = Element(n12, n13, area_v, inercia_v, young)
e14 = Element(n13, n14, area_v, inercia_v, young)
e15 = Element(n10, n14, area_p, inercia_p, young)

# Fator Pi -----------------------------------------------------------------------------------
e2.setP(0.5, 1)
e4.setP(1, 0.5)

e7.setP(0.5, 1)
e9.setP(1, 0.5)

e12.setP(0.5, 1)
e14.setP(1, 0.5)

nodes = [n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14]
elements = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15]

# Resultados ---------------------------------------------------------------------------------
calc = Process(nodes, elements)
plot = Print(calc)
# plot.nodalDisplacement()
# plot.elementDeformations()
# plot.internalForces()
""" ESTRUTURA EXEMPLO APRESENTADA NA IC UVA 2022.2 """
# Seções --------------------------------------------------------------------------------------
secao_v = Rectangle(0.15, 0.6)  # base x altura
area_v = secao_v.area
inercia_v = secao_v.inertia

# Materiais -----------------------------------------------------------------------------------
young = 27_000_000_000

# Nos -----------------------------------------------------------------------------------------
n1 = Node(0, 0)
n2 = Node(2, 0)
n3 = Node(4, 0)
n4 = Node(6, 0)

# Elementos -----------------------------------------------------------------------------------
e1 = Element(n1, n2, area_v, inercia_v, young)
e2 = Element(n2, n3, area_v, inercia_v, young)
e3 = Element(n3, n4, area_v, inercia_v, young)

# Apoios --------------------------------------------------------------------------------------
n1.setSupport(Apoio.semi_rigido)
n4.setSupport(Apoio.semi_rigido)

n1.setP(0.042)
n4.setP(0.042)

# Forças --------------------------------------------------------------------------------------
n2.setNodalForce(NodalForce(0, -10_000, 0))
n3.setNodalForce(NodalForce(0, -10_000, 0))

nodes = [n1, n2, n3, n4]
elements = [e1, e2, e3]

calc = Process(nodes, elements)
plot = Print(calc)
plot.internalForces()
