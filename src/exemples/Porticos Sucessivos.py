from UVATool import *
from UVATool.Enums import *

def porticosSucessivos(n_andares=20,
                       n_pilares_por_andar=7,
                       distancia_pilares=6,
                       pe_direito=3):
    '''PORTICOS SUCESSIVOS'''
    structure_name = f'PORTICOS SUCESSIVOS N_ANDARES={n_andares} PE_DIREITO={pe_direito} N_PILARES_POR_ANDAR={n_pilares_por_andar}'
    # CONDIÇÕES INICIAIS
    n_andares = n_andares + 1
    # n_pilares_por_andar = 7
    # distancia_pilares = 6
    # pe_direito = 3

    # SEÇÃO DOS PILARES
    rec = Rectangle(0.20, 0.20)
    area_p = rec.area
    inercia_p = rec.inertia

    # SEÇÃO DAS VIGAS
    rec = Rectangle(0.15, 0.60)
    area_v = rec.area
    inercia_v = rec.inertia

    # CONCRETO 30 MPa
    young_modulus = 27_000_000_000

    nodes: list[Node] = []
    elements: list[Element] = []

    for x in range(n_pilares_por_andar):
        for y in range(n_andares):
            nodes.append(Node(x * distancia_pilares, y * pe_direito))

    # PILARES
    for pilar in range(n_pilares_por_andar):
        for i in range(n_andares - 1):
            node_pos = i + pilar * n_andares
            elements.append(
                Element(nodes[node_pos], nodes[node_pos + 1], area_p,
                        inercia_p, young_modulus))

    # VIGAS
    for qtpilares in range(1, n_pilares_por_andar, 1):
        for i in range(1, n_andares, 1):
            elements.append(
                Element(nodes[i + (qtpilares - 1) * n_andares],
                        nodes[i + qtpilares * n_andares], area_v, inercia_v,
                        young_modulus))

    # APOIOS DOS PILARES MAIS INFERIORES
    for i in range(n_pilares_por_andar):
        nodes[i * n_andares].setSupport(Apoio.terceiro_genero)

    # FORÇA DE VENTO A CADA ANDAR
    for i in range(1, n_andares, 1):
        nodes[i].setNodalForce(NodalForce(i * i * 10, 0, 0))

    structure = Structure(structure_name, nodes, elements)

    return structure

    
structure = porticosSucessivos()

if __name__ == "__main__":
    proc = Process(structure.nodes, structure.elements)
    plot = Print(proc)
    plot.nodalDisplacement()