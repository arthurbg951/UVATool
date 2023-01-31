from UVATool import Process, StructureFile, Print

struct_file = StructureFile("Exemplo Simples.py")
structure = struct_file.getStructure()

if __name__ == '__main__':
    proc = Process(structure.nodes, structure.elements)
    plot = Print(proc)
    plot.internalForces()
