from UVATool import *
from UVATool.Enums import *

n1 = Node(0, 0)
nm = Node(1, 0)
n2 = Node(2, 0)

n1.setSupport(Apoio.segundo_genero)
n2.setSupport(Apoio.primeiro_genero)

nm.setNodalForce(NodalForce(0, -20e3, 0))

rec = Rectangle(0.01, 0.12)
e1 = Element(n1, nm, rec.area, rec.inertia, 10e6)
e2 = Element(nm, n2, rec.area, rec.inertia, 10e6)

structure = Structure(__file__, [n1, nm, n2], [e1, e2])

if __name__ == "__main__":
    proc = Process(structure.nodes, structure.elements)

    plot = Print(proc)
    plot.nodalDisplacement()
    plot.internalForces()
    plot.elementsDeformations()
