from UVATool import Process, StructureFile, Print


if __name__ == '__main__':
    struct_file = StructureFile("Exemplo Simples.py")
    structure = struct_file.getStructure()
    proc = Process(structure.nodes, structure.elements)
    plot = Print(proc)
    plot.internalForces()
