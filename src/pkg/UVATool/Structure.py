from UVATool.Node import Node
from UVATool.Element import Element


class Structure:
    """
    ## structure_name - insert a name to structure
    ## structure_description - insert a description to structure
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

    def __eq__(self, __o: object) -> bool:
        node_count = len(self.nodes)
        element_count = len(self.elements)
        node_sum = 0
        element_sum = 0
        if isinstance(__o, Structure):
            if len(__o.nodes) == node_count:
                for i in range(node_count):
                    if self.nodes[i] == __o.nodes[i]:
                        node_sum += 1
            if len(__o.elements) == element_count:
                for i in range(element_count):
                    if self.elements[i] == __o.elements[i]:
                        element_sum += 1
            equal_nodes = node_count == node_sum
            equal_elements = element_count == element_sum
            return equal_nodes and equal_elements
        else:
            raise Exception("This operation is invalid!")
