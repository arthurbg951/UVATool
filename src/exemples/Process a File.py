from UVATool import Process, StructureFile, Print
from UVATool.Colors import to_red
import os

'''
ESTE ARQUIVO MOSTRA COMO UTILIZAR A CLASSE StructureFile PARA ABRIR UMA
ESTRUTURA CONTIDA EM UM SCRIPT PYTHON
'''
# NOME DO SCRIPT PYTHON
python_script = os.path.join(os.path.dirname(__file__), 'fixed-middle-force.py')

# ABRE O ARQUIVO
struct_file = StructureFile(python_script)

# COLETA AS ESTRUTURAS DO ARQUIVO
# OBS: Função getStructure merece revisão
structures = struct_file.getStructure()

if __name__ == '__main__':
    for structure in structures:
        try:
            proc = Process(structure.nodes, structure.elements)
            plot = Print(proc)
            plot.internalForces()
        except Exception as e:
            print(to_red(f"{structure.structure_name} {str(e)}"))
else:
    # Retorna apenas a primeira estrutura
    structure = structures[0]
