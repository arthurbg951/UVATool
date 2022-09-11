from libs.UVATool import *

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

calc = Process(nodes, elements, Analise.elastica.viaRigidezAnalitica)
plot = Print(calc)
plot.internalForces()
# plot.nodalDisplacement()
# plot.elementDeformations()


'''
----------------------------------------------------------------------------------------------
EXEMPLO (B)


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

# Fator Pi -----------------------------------------------------------------------------------
n2.setP(1)
n4.setP(1)
n6.setP(1)

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

nodes = [n1, n2, n3, n4, n5, n6, n7]
elements = [e1, e2, e3, e4, e5, e6]

calc = Process(nodes, elements, Analise.elastica.viaRigidezAnalitica)
plot = Print(calc)
plot.internalForces()
# plot.nodalDisplacement()



'''
----------------------------------------------------------------------------------------------
EXEMPLO (C)


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
calc = Process(nodes, elements, Analise.elastica.viaRigidezAnalitica)
plot = Print(calc)
# plot.nodalDisplacement()
# plot.elementDeformations()
plot.internalForces()



'''
----------------------------------------------------------------------------------------------
EXEMPLO (D)


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

# Fator Pi -----------------------------------------------------------------------------------
n2.setP(1)
n5.setP(1)

n7.setP(1)
n10.setP(1)

n11.setP(1)
n14.setP(1)

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
e5 = Element(n5, n6, area_p, inercia_p, young)

nodes = [n1, n2, n3, n4, n5, n6]
elements = [e1, e2, e3, e4, e5]

# Resultados ---------------------------------------------------------------------------------
calc = Process(nodes, elements, Analise.elastica.viaRigidezAnalitica)
plot = Print(calc)
# plot.nodalDisplacement()
# plot.elementDeformations()
plot.internalForces()
