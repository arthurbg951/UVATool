from UVATool import *
from UVATool.Enums import *

n1 = Node(0, 0)
n2 = Node(2, 0)

n1.setSupport(Apoio.segundo_genero)
n2.setSupport(Apoio.primeiro_genero)

n1.setNodalForce(NodalForce(0, -10e3, 10e3))
n2.setNodalForce(NodalForce(0, -10e3, 10e3))

e1 = Element(n1, n2, 1, 1, 1)

structure = Structure(__file__, [n1, n2], [e1])

if __name__ == "__main__":
    proc = Process(structure.nodes, structure.elements)

    plot = Print(proc)
    plot.nodalDisplacement()
    plot.internalForces()
    plot.elementDeformations()
