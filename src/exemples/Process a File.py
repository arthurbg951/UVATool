from UVATool import Process, StructureFile, Print

struct_file = StructureFile("Porticos Sucessivos.py")
structure = struct_file.getStructure()[0]

if __name__ == '__main__':
    proc = Process(structure.nodes, structure.elements)
    plot = Print(proc)
    plot.internalForces()
