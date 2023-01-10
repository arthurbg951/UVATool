from UVATool import *
from UVATool.Enums import *
import math

# SEÇÃO
secao = Rectangle(0.012, 0.001)
area = secao.area
inercia = secao.inertia


def balanco() -> Structure:
    '''BALANÇO'''
    structure_name = 'BALANÇO'
    n1 = Node(0, 0)
    n1.setSupport(Support.fixed)
    n2 = Node(10, 0)
    n2.setNodalForce(NodalForce(0, -100, 0))
    nodes = [n1, n2]
    e1 = Element(n1, n2, 1, 1, 1)
    elements = [e1]
    structure = Structure(structure_name, nodes, elements)
    return structure


def trelica():
    '''TRELIÇA'''
    structure_name = 'TRELIÇA'
    n1 = Node(0, 0)
    n2 = Node(0.5, math.sin(60 * math.pi / 180))
    n3 = Node(1, 0)
    n1.setSupport(Support.pinned)
    n3.setSupport(Support.roller)
    n2.setNodalForce(NodalForce(10, 0, 0))
    e1 = Element(n1, n2, area, inercia, 1)
    e2 = Element(n2, n3, area, inercia, 1)
    e3 = Element(n1, n3, area, inercia, 1)
    nodes = [n1, n2, n3]
    elements = [e1, e2, e3]
    structure = Structure(structure_name, nodes, elements)
    return structure


def edificio_de_3_andares():
    '''EDIFICIO DE 3 ANDARES'''
    structure_name = 'EDIFICIO DE 3 ANDARES'
    n1 = Node(0, 0)
    n2 = Node(15, 0)
    n3 = Node(0, 3)
    n4 = Node(15, 3)
    n5 = Node(0, 6)
    n6 = Node(15, 6)
    n7 = Node(0, 9)
    n8 = Node(15, 9)
    n1.setSupport(Apoio.segundo_genero)
    n2.setSupport(Apoio.primeiro_genero)
    n3.setNodalForce(NodalForce(100, 0, 0))
    n5.setNodalForce(NodalForce(100, 0, 0))
    n7.setNodalForce(NodalForce(100, 0, 0))
    e1 = Element(n1, n3, area, inercia, 1)
    e2 = Element(n2, n4, area, inercia, 1)
    e3 = Element(n3, n4, area, inercia, 1)
    e4 = Element(n3, n5, area, inercia, 1)
    e5 = Element(n4, n6, area, inercia, 1)
    e6 = Element(n5, n6, area, inercia, 1)
    e7 = Element(n5, n7, area, inercia, 1)
    e8 = Element(n6, n8, area, inercia, 1)
    e9 = Element(n7, n8, area, inercia, 1)
    nodes = [n1, n2, n3, n4, n5, n6, n7, n8]
    elements = [e1, e2, e3, e4, e5, e6, e7, e8, e9]
    structure = Structure(structure_name, nodes, elements)
    return structure


def estrutura_hipostatica():
    '''ESTRUTURA HIPOSTATICA'''
    structure_name = 'ESTRUTURA HIPOSTATICA'
    n1 = Node(0, 0)
    n1.setSupport(Support.pinned)
    n2 = Node(0, 10)
    n2.setNodalForce(NodalForce(0, -100, 0))
    nodes = [n1, n2]
    e1 = Element(n1, n2, 1, 1, 1)
    elements = [e1]
    structure = Structure(structure_name, nodes, elements)
    return structure


'''############ TESTES SEMI RIGIDEZ ############'''


def bi_engastado():
    '''BI ENGASTADO'''
    structure_name = 'BI ENGASTADO'
    n1 = Node(0, 0)
    n1.setSupport(Support.fixed)
    n2 = Node(5, 0)
    n2.setNodalForce(NodalForce(0, -10, 0))
    n3 = Node(10, 0)
    n3.setSupport(Support.fixed)
    nodes = [n1, n2, n3]
    e1 = Element(n1, n2, area, inercia, 1)
    e2 = Element(n2, n3, area, inercia, 1)
    elements = [e1, e2]
    structure = Structure(structure_name, nodes, elements)
    return structure


def semi_rigido():
    '''SEMI RIGIDO'''
    structure_name = 'SEMI RIGIDO'
    n1 = Node(0, 0)
    n2 = Node(5, 0)
    n3 = Node(10, 0)
    n1.setSupport(Support.semi_fixed)
    n1.setP(0.5)
    n2.setNodalForce(NodalForce(0, -10, 0))
    n3.setSupport(Support.semi_fixed)
    n3.setP(0.5)
    e1 = Element(n1, n2, area, inercia, 1)
    e2 = Element(n2, n3, area, inercia, 1)
    nodes = [n1, n2, n3]
    elements = [e1, e2]
    structure = Structure(structure_name, nodes, elements)
    return structure


def semi_rigido2():
    '''SEMI RIGIDO2'''
    structure_name = 'SEMI RIGIDO2'
    fator = 1e-31
    n1 = Node(0, 0)
    n2 = Node(0, fator)
    n3 = Node(5, fator)
    n4 = Node(10, fator)
    n5 = Node(10, 0)
    n6 = Node(-0.17, 2.29)
    n1.setSupport(Support.fixed)
    # n2.setP(0.5)
    n3.setNodalForce(NodalForce(0, -10, 0))
    # n4.setP(0.5)
    n5.setSupport(Support.fixed)
    n6.setSupport(Support.fixed)
    e1 = Element(n1, n2, area, inercia, 1)
    e2 = Element(n2, n3, area, inercia, 1)
    e2.setP(0.5, n3.getP())
    e3 = Element(n3, n4, area, inercia, 1)
    e3.setP(n3.getP(), 0.5)
    e4 = Element(n4, n5, area, inercia, 1)
    e5 = Element(n2, n6, area, inercia, 1)
    nodes = [n1, n2, n3, n4, n5, n6]
    elements = [e1, e2, e3, e4, e5]
    structure = Structure(structure_name, nodes, elements)
    return structure


def isostatico():
    '''ISOSTATICO'''
    structure_name = 'ISOSTATICO'
    n1 = Node(0, 0)
    n1.setSupport(Support.pinned)
    n2 = Node(5, 0)
    n2.setNodalForce(NodalForce(0, -10, 0))
    n3 = Node(10, 0)
    n3.setSupport(Support.roller)
    nodes = [n1, n2, n3]
    e1 = Element(n1, n2, 1, 1, 1)
    e2 = Element(n2, n3, 1, 1, 1)
    elements = [e1, e2]
    structure = Structure(structure_name, nodes, elements)
    return structure


def portico_com_vao_de_10m_pe_direito_3m():
    '''PORTICO COM VÃO DE 10m PE DIREITO 3m'''
    structure_name = 'PORTICO COM VÃO DE 10m PE DIREITO 3m'
    # 2 APOIOS FIXOS E 2 ROTULAS
    n1 = Node(0, 0)
    n2 = Node(0, 3)
    n3 = Node(10, 3)
    n4 = Node(10, 0)
    n1.setSupport(Support.fixed)
    n4.setSupport(Support.fixed)
    n2.setSupport(Support.middle_hinge)
    n3.setSupport(Support.middle_hinge)
    # n2.setP(0)
    # n3.setP(0)
    n2.setNodalForce(NodalForce(100, 0, 0))
    e1 = Element(n1, n2, area, inercia, 1)
    e2 = Element(n2, n3, area, inercia, 1)
    e3 = Element(n3, n4, area, inercia, 1)
    nodes = [n1, n2, n3, n4]
    elements = [e1, e2, e3]
    structure = Structure(structure_name, nodes, elements)
    return structure


def portico_maluco():
    '''PORTICO MALUCO'''
    structure_name = 'PORTICO MALUCO'
    n1 = Node(-0.17, 2.29)
    n2 = Node(0, 3)
    n3 = Node(10, 3)
    n4 = Node(10, 0)
    n5 = Node(0, 0)
    n1.setSupport(Apoio.terceiro_genero)
    n4.setSupport(Apoio.terceiro_genero)
    n5.setSupport(Apoio.terceiro_genero)
    n2.setNodalForce(NodalForce(100, 0, 0))
    sec = Rectangle(0.012, 0.001)
    area = sec.area
    inercia = sec.inertia
    e1 = Element(n1, n2, area, inercia, 1)
    e2 = Element(n2, n3, area, inercia, 1)
    e3 = Element(n3, n4, area, inercia, 1)
    e4 = Element(n2, n5, area, inercia, 1)
    nodes = [n1, n2, n3, n4, n5]
    elements = [e1, e2, e3, e4]
    structure = Structure(structure_name, nodes, elements)
    return structure


def semi_rigido3():
    '''SEMI RÍGIDO3'''
    structure_name = 'SEMI RÍGIDO3'
    n1 = Node(0, 0)
    n2 = Node(1, 0)
    n1.setSupport(Apoio.semi_rigido)
    n2.setSupport(Apoio.primeiro_genero)
    n2.setNodalForce(NodalForce(50, 0, 100))
    rec = Rectangle(0.012, 0.001)
    area = rec.area
    inercia = rec.inertia
    e1 = Element(n1, n2, area, inercia, 1)
    nodes = [n1, n2]
    elements = [e1]
    structure = Structure(structure_name, nodes, elements)
    return structure


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


def process_simulation(structure: Structure,
                       show_equilibrium_matrix=False,
                       show_frame_stiffness_matrix=False,
                       show_global_frame_stiffness=False,
                       show_nodal_displacement=False,
                       show_deformations=False,
                       show_internal_forces=False,
                       show_processed_time=True,
                       show_errors=True):
    try:
        erros: list[str] = []
        time = None
        proc = Process(structure.nodes, structure.elements,
                       Analise.elastica.viaRigidezAnalitica)
        time = proc.getProcessTime()
        plot = Print(proc)

        if show_equilibrium_matrix:
            print("MATRIZ DE EQUILIBRIO - [L]\n", proc.getEquilibriumMatrix(),
                  "\n")
        if show_frame_stiffness_matrix:
            print("MATRIZ DE RIGIDEZ (DO ELEMENTO) - [k]\n",
                  proc.getFrameStiffness(), "\n")
        if show_global_frame_stiffness:
            print("RIGIDEZ GLOBAL DO SISTEMA - [K]\n",
                  proc.getGlobalFrameStiffness(), "\n")
        if show_nodal_displacement:
            plot.nodalDisplacement()
        if show_deformations:
            plot.elementDeformations()
        if show_internal_forces:
            plot.internalForces()

    except ValueError and StructureError:
        erros.append(f" -> ESTRUTURA HIPOSTATICA '{structure.structure_name}'")
    except numpy.linalg.LinAlgError:
        erros.append(
            f" -> ERRO NOS CÁLCULOS DA ESTRUTURA '{structure.structure_name}'")
    except TypeError as e:
        erros.append(f" -> ENTRADA DE DADOS INCORRETA\n{e.args[0]}")
    finally:
        if show_errors:
            for erro in erros:
                print(erro)
        if show_processed_time and time is not None:
            print(
                f"UVATool DEMOROU {time} PARA PROCESSAR A ESTRUTURA '{structure.structure_name}'"
            )
        else:
            print(
                f'OCORREU UM ERRO INESPERADO NA ESTRUTURA {structure.structure_name}'
            )


if __name__ == "__main__":
    inicial_time = datetime.now()

    process_simulation(balanco())
    process_simulation(trelica())
    process_simulation(edificio_de_3_andares())
    process_simulation(estrutura_hipostatica())
    process_simulation(bi_engastado())
    process_simulation(semi_rigido())
    process_simulation(semi_rigido2())
    process_simulation(isostatico())
    process_simulation(portico_com_vao_de_10m_pe_direito_3m())
    process_simulation(portico_maluco())
    process_simulation(semi_rigido3())
    process_simulation(porticosSucessivos(n_andares=53, n_pilares_por_andar=2))

    print(f"TOTAL TIME = {(datetime.now() - inicial_time).seconds}s")
