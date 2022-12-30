from libs.UVATool import *


if __name__ == '__main__':
    struct = StructFile("/home/arthur/repos/UVATool/tests/exemples/Exemplo Simples.py").getStructure()
    proc = Process(struct.nodes, struct.elements, Analise.elastica.viaRigidezAnalitica)
    plot = Print(proc)
    plot.internalForces()
