from UVATool import Node, Element, Support, Analise, NodalForce, Process, Retangle
from datetime import datetime
import math
import traceback

# VETORES RESPOSTA PADROES
nodes = []
elements = []

# VERIFICACAO DO TEMPO DE EXECUCAO
inicio = None
fim = None

try:
    inicio = datetime.now()
    # BALANÇO
    # n1 = Node(0, 0)
    # n1.setSupport(Support.fixed)
    # n2 = Node(10, 0)
    # n2.setNodalForce(NodalForce(0, -100, 0))
    # nodes = [n1, n2]
    # e1 = Element(n1, n2, 1, 1, 1)
    # elements = [e1]

    # TRELIÇA
    # n1 = Node(0, 0)
    # n1.setSupport(Support.pinned)
    # n2 = Node(0.5, math.sin(60*math.pi/180))
    # n3 = Node(1, 0)
    # n3.setSupport(Support.roller)
    # nodes = [n1, n2, n3]
    # e1 = Element(n1, n2, 1, 1, 1)
    # e2 = Element(n2, n3, 1, 1, 1)
    # e3 = Element(n1, n3, 1, 1, 1)
    # elements = [e1, e2, e3]

    # EDIFICIO DE 3 ANDARES
    n1 = Node(0, 0)
    n2 = Node(15, 0)
    n3 = Node(0, 3)
    n4 = Node(15, 3)
    n5 = Node(0, 6)
    n6 = Node(15, 6)
    n7 = Node(0, 9)
    n8 = Node(15, 9)
    n1.setSupport(Support.pinned)
    n2.setSupport(Support.roller)
    n3.setNodalForce(NodalForce(100, 0, 0))
    n5.setNodalForce(NodalForce(100, 0, 0))
    n7.setNodalForce(NodalForce(100, 0, 0))
    nodes = [n1, n2, n3, n4, n5, n6, n7, n8]
    secao = Retangle(0.012, 0.001)
    area = secao.area()
    momento_inercia = secao.momentInertia()
    e1 = Element(n1, n3, area, momento_inercia, 1)
    e2 = Element(n3, n5, area, momento_inercia, 1)
    e3 = Element(n2, n4, area, momento_inercia, 1)
    e4 = Element(n3, n4, area, momento_inercia, 1)
    e5 = Element(n4, n6, area, momento_inercia, 1)
    e6 = Element(n5, n6, area, momento_inercia, 1)
    e7 = Element(n5, n7, area, momento_inercia, 1)
    e8 = Element(n7, n8, area, momento_inercia, 1)
    e9 = Element(n6, n8, area, momento_inercia, 1)
    elements = [e1, e2, e3, e4, e5, e6, e7, e8, e9]

    # ESTRUTURA HIPOSTATICA
    # n1 = Node(0, 0)
    # n1.setSupport(Support.pinned)
    # n2 = Node(0, 10)
    # n2.setNodalForce(NodalForce(0, -100, 0))
    # nodes = [n1, n2]
    # e1 = Element(n1, n2, 1, 1, 1)
    # elements = [e1]

    # TESTES SEMI RIGIDEZ
    # BI ENGASTADO
    # n1 = Node(0, 0)
    # n1.setSupport(Support.fixed)
    # n2 = Node(5, 0)
    # n2.setNodalForce(NodalForce(0, -10, 0))
    # n3 = Node(10, 0)
    # n3.setSupport(Support.fixed)
    # nodes = [n1, n2, n3]
    # e1 = Element(n1, n2, 1, 1, 1)
    # e2 = Element(n2, n3, 1, 1, 1)
    # elements = [e1, e2]

    # SEMI RIGIDO
    # n1 = Node(0, 0)
    # n1.setSupport(Support.fixed)
    # n2 = Node(0, 0.0000001)
    # n2.setP(0.5)
    # n3 = Node(5, 0.0000001)
    # n3.setNodalForce(NodalForce(0, -10, 0))
    # n4 = Node(10, 0.0000001)
    # n4.setP(0.5)
    # n5 = Node(10, 0)
    # n5.setSupport(Support.fixed)
    # nodes = [n1, n2, n3, n4, n5]
    # e1 = Element(n1, n2, 1, 1, 1)
    # e2 = Element(n2, n3, 1, 1, 1)
    # e3 = Element(n3, n4, 1, 1, 1)
    # e4 = Element(n4, n5, 1, 1, 1)
    # elements = [e1, e2, e3, e4]

    # ISOSTATICO
    # n1 = Node(0, 0)
    # n1.setSupport(Support.pinned)
    # n2 = Node(5, 0)
    # n2.setNodalForce(NodalForce(0, -100, 0))
    # n3 = Node(10, 0)
    # n3.setSupport(Support.roller)
    # nodes = [n1, n2, n3]
    # e1 = Element(n1, n2, 1, 1, 1)
    # e2 = Element(n2, n3, 1, 1, 1)
    # elements = [e1, e2]

    # HIPOSTATICO
    # n1 = Node(0, 0)
    # n1.setSupport(Support.roller)
    # n2 = Node(5, 0)
    # n2.setNodalForce(NodalForce(0, -100, 0))
    # n3 = Node(10, 0)
    # n3.setSupport(Support.roller)
    # nodes = [n1, n2, n3]
    # e1 = Element(n1, n2, 1, 1, 1)
    # e2 = Element(n2, n3, 1, 1, 1)
    # elements = [e1, e2]

    # PORTICO ROTULADO ERRO
    # PORTICO COM VÃO DE 10m PE DIREITO 3m
    # 2 APOIOS FIXOS E 2 ROTULAS
    # n1 = Node(0, 0)
    # n1.setSupport(Support.fixed)
    # n2 = Node(0, 3)
    # # n2.setSupport(Support.middle_hinge)
    # n2.setP(0.001)
    # n2.setNodalForce(NodalForce(100_000, 0, 0))
    # n3 = Node(10, 3)
    # # n3.setSupport(Support.middle_hinge)
    # n3.setP(0.001)
    # n4 = Node(10, 0)
    # n4.setSupport(Support.fixed)
    # nodes = [n1, n2, n3, n4]
    # e1 = Element(n1, n2, 1, 1, 1)
    # e2 = Element(n2, n3, 1, 1, 1)
    # e3 = Element(n3, n4, 1, 1, 1)
    # elements = [e1, e2, e3]

    proc = Process(nodes, elements, Analise.elastica_via_rigidez_analitica )
    # print("MATRIZ DE EQUILIBRIO - [L]\n", proc.getEquilibriumMatrix(), "\n")
    # print("MATRIZ DE RIGIDEZ (DO ELEMENTO) - [k]\n", proc.getFrameStiffness(), "\n")
    # print("RIGIDEZ GLOBAL DO SISTEMA - [K]\n", proc.getGlobalFrameStiffness(), "\n")
    # print("VETOR DOS DESLOCAMENTOS NODAIS - {δ}\n", proc.getNodalDisplacement(), "\n")
    # print("DEFORMAÇÕES CORRESPONDENTES - {θ}\n", proc.getDeformations(), "\n")
    # print("Esforços Seccionais Internos - {m}\n", proc.getStressResultants(), "\n")

    # for i in range(0, len(proc.getStressResultants()), 3):
    #     # print(" N[{0}]={1:.2f}".format(int(i/3+1), proc.getStressResultants()[0 + i]))
    #     print("M1[{0}]={1:.2f}".format(int(i/3+1), proc.getStressResultants()[1 + i]))
    #     print("M2[{0}]={1:.2f}".format(int(i/3+1), proc.getStressResultants()[2 + i]))
    #     print()

    deformacoes = proc.getNodalDisplacement()
    for deformacao in deformacoes:
        print(deformacao)

except ValueError:
    print("ESTRUTURA HIPOSTATICA")
except TypeError:
    print("ENTRADA DE DADOS INCORRETA")
    print(traceback.format_exc())
finally:
    fim = datetime.now()
    print("TEMPO DE CALCULO = ", fim - inicio)
