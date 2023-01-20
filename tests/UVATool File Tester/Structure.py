from UVATool import *
from UVATool.Enums import *

n1 = Node(0, 0)
n2 = Node(10, 0)

n1.setSupport(Support.fixed)
n2.setNodalForce(NodalForce(0, -100, 0))

e1 = Element(n1, n2, 1, 1, 1)

nodes = [n1, n2]
elements = [e1]
    
structure = Structure('BALANÇO', nodes, elements)
