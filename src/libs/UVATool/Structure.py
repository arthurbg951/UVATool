from UVATool.Node import Node
from UVATool.Element import Element


class Structure:
    """
    
    """
    # This class define a structure
    # It deserve to load files with a script (.py file)
    structure_name: str
    structure_description: str
    nodes: list[Node]
    elements: list[Element]

    def __init__(self, structure_name: str, nodes: list[Node], elements: list[Element], structure_description: str = '') -> None:
        # CLASSE FALTANDO UMA VERIFICAÇÃO SE A ESTRUTURA REALMENTE SE CONECTA, CASO CONTRÁRIO, RETORNAR UM STRUCTURE ERROR
        self.structure_name = structure_name
        self.structure_description = structure_description
        self.nodes = nodes
        self.elements = elements
