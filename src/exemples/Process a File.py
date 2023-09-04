from UVATool import Process, StructureFile, Print
from UVATool.Colors import to_red

'''
ESTE ARQUIVO MOSTRA COMO UTILIZAR A CLASSE StructureFile PARA ABRIR UMA
ESTRUTURA CONTIDA EM UM SCRIPT PYTHON
'''

struct_file = StructureFile("Estrutura Desconexa.py")
structures = struct_file.getStructure()

if __name__ == '__main__':
    for structure in structures:
        try:
            proc = Process(structure.nodes, structure.elements)
            plot = Print(proc)
            plot.internalForces()
        except Exception as e:
            print(to_red(f"{structure.structure_name} {str(e)}"))
