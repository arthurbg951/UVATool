from libs.UVATool import *

# SEÇÃO
secao = Rectangle(0.012, 0.001)
area = secao.area
inercia = secao.inertia

'''BALANÇO'''
structure_name = 'BALANÇO'
n1 = Node(0, 0)
n1.setSupport(Support.fixed)
n2 = Node(10, 0)
n2.setNodalForce(NodalForce(0, -100, 0))
nodes = [n1, n2]
e1 = Element(n1, n2, 1, 1, 1)
elements = [e1]
structure = Structure(structure_name, nodes, elements)
