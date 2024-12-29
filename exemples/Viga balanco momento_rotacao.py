from uvatool import Node, Element, Process, Print, Rectangle, NodalForce, Apoio

"""
ATENÇÃO: Inserir todos os valores no sistema internacional de unidades (SI)
"""
# Materiais ----------------------------------------------------------------------------------
secao_p = Rectangle(0.2, 0.2)  # hy x hx
area_p = secao_p.area
inercia_p = secao_p.inertia
secao_v = Rectangle(0.15, 0.6)  # base x altura
area_v = secao_v.area
inercia_v = secao_v.inertia
young = 27e9

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

# --------------------------------------------------------------------------------------------
e1 = Element(n1, n2, area_p, inercia_p, young)
e2 = Element(n2, n3, area_v, inercia_v, young)

nodes = [n1, n2, n3]
elements = [e1, e2]

calc = Process(nodes, elements)
plot = Print(calc)
plot.internalForces()
plot.nodalDisplacement()
