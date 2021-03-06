from libs.UVATool import *
from datetime import datetime
import math
import traceback

# VETORES RESPOSTA PADROES
nodes = []
elements = []

# VERIFICACAO DO TEMPO DE EXECUCAO
time = None

try:
    secao = Rectangle(0.012, 0.001)
    area = secao.area
    inercia = secao.inertia
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
    # n2 = Node(0.5, math.sin(60*math.pi/180))
    # n3 = Node(1, 0)
    # n1.setSupport(Support.pinned)
    # n3.setSupport(Support.roller)
    # n2.setNodalForce(NodalForce(10, 0, 0))
    # e1 = Element(n1, n2, area, inercia, 1)
    # e2 = Element(n2, n3, area, inercia, 1)
    # e3 = Element(n1, n3, area, inercia, 1)
    # nodes = [n1, n2, n3]
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
    # e1 = Element(n1, n2, area, inercia, 1)
    # e2 = Element(n2, n3, area, inercia, 1)
    # elements = [e1, e2]

    # SEMI RIGIDO
    # n1 = Node(0, 0)
    # n2 = Node(5, 0)
    # n3 = Node(10, 0)
    # n1.setSupport(Support.semi_fixed)
    # n1.setP(0.5)
    # n2.setNodalForce(NodalForce(0, -10, 0))
    # n3.setSupport(Support.semi_fixed)
    # n3.setP(0.5)
    # e1 = Element(n1, n2, area, inercia, 1)
    # e2 = Element(n2, n3, area, inercia, 1)
    # nodes = [n1, n2, n3]
    # elements = [e1, e2]

    # SEMI RIGIDO
    # fator = 1e-31
    # n1 = Node(0, 0)
    # n2 = Node(0, fator)
    # n3 = Node(5, fator)
    # n4 = Node(10, fator)
    # n5 = Node(10, 0)
    # n6 = Node(-0.17, 2.29)
    # n1.setSupport(Support.fixed)
    # # n2.setP(0.5)
    # n3.setNodalForce(NodalForce(0, -10, 0))
    # # n4.setP(0.5)
    # n5.setSupport(Support.fixed)
    # n6.setSupport(Support.fixed)
    # e1 = Element(n1, n2, area, inercia, 1)
    # e2 = Element(n2, n3, area, inercia, 1)
    # e2.setP(0.5, n3.getP())
    # e3 = Element(n3, n4, area, inercia, 1)
    # e3.setP(n3.getP(), 0.5)
    # e4 = Element(n4, n5, area, inercia, 1)
    # e5 = Element(n2, n6, area, inercia, 1)
    # nodes = [n1, n2, n3, n4, n5, n6]
    # elements = [e1, e2, e3, e4, e5]

    # ISOSTATICO
    # n1 = Node(0, 0)
    # n1.setSupport(Support.pinned)
    # n2 = Node(5, 0)
    # n2.setNodalForce(NodalForce(0, -10, 0))
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
    # n2.setNodalForce(NodalForce(0, -10, 0))
    # n3 = Node(10, 0)
    # n3.setSupport(Support.roller)
    # nodes = [n1, n2, n3]
    # e1 = Element(n1, n2, 1, 1, 1)
    # e2 = Element(n2, n3, 1, 1, 1)
    # elements = [e1, e2]

    # PORTICO COM VÃO DE 10m PE DIREITO 3m
    # 2 APOIOS FIXOS E 2 ROTULAS
    # n1 = Node(0, 0)
    # n2 = Node(0, 3)
    # n3 = Node(10, 3)
    # n4 = Node(10, 0)
    # rec = Rectangle(0.012, 0.001)
    # area = rec.area
    # inercia = rec.inertia
    # n1.setSupport(Support.fixed)
    # n4.setSupport(Support.fixed)
    # n2.setSupport(Support.middle_hinge)
    # n3.setSupport(Support.middle_hinge)
    # # n2.setP(0)
    # # n3.setP(0)
    # n2.setNodalForce(NodalForce(100, 0, 0))
    # e1 = Element(n1, n2, area, inercia, 1)
    # e2 = Element(n2, n3, area, inercia, 1)
    # e3 = Element(n3, n4, area, inercia, 1)
    # nodes = [n1, n2, n3, n4]
    # elements = [e1, e2, e3]

    # PORTICO MALUCO
    # n1 = Node(-0.17, 2.29)
    # n2 = Node(0, 3)
    # n3 = Node(10, 3)
    # n4 = Node(10, 0)
    # n5 = Node(0, 0)
    # n1.setSupport(Apoio.terceiro_genero)
    # n4.setSupport(Apoio.terceiro_genero)
    # n5.setSupport(Apoio.terceiro_genero)
    # n2.setNodalForce(NodalForce(100, 0, 0))
    # sec = Rectangle(0.012, 0.001)
    # area = sec.area
    # inercia = sec.inertia
    # e1 = Element(n1, n2, area, inercia, 1)
    # e2 = Element(n2, n3, area, inercia, 1)
    # e3 = Element(n3, n4, area, inercia, 1)
    # e4 = Element(n2, n5, area, inercia, 1)
    # nodes = [n1, n2, n3, n4, n5]
    # elements = [e1, e2, e3, e4]

    # SEMI RÍGIDO
    # n1 = Node(0, 0)
    # n2 = Node(1, 0)
    # n1.setSupport(Apoio.semi_rigido)
    # n2.setSupport(Apoio.primeiro_genero)
    # n2.setNodalForce(NodalForce(50, 0, 100))
    # rec = Rectangle(0.012, 0.001)
    # area = rec.area
    # inercia = rec.inertia
    # e1 = Element(n1, n2, area, inercia, 1)
    # nodes = [n1, n2]
    # elements = [e1]

    proc = Process(nodes, elements, Analise.elastica.viaRigidezAnalitica)
    time = proc.getProcessTime()

    # print("MATRIZ DE EQUILIBRIO - [L]\n", proc.getEquilibriumMatrix(), "\n")
    # print("MATRIZ DE RIGIDEZ (DO ELEMENTO) - [k]\n", proc.getFrameStiffness(), "\n")
    # print("RIGIDEZ GLOBAL DO SISTEMA - [K]\n", proc.getGlobalFrameStiffness(), "\n")
    # print("VETOR DOS DESLOCAMENTOS NODAIS - {δ}\n", proc.getNodalDisplacement(), "\n")
    # print("DEFORMAÇÕES CORRESPONDENTES - {θ}\n", proc.getDeformations(), "\n")
    # print("Esforços Seccionais Internos - {m}\n", proc.getInternalForces(), "\n")

    plot = Print(proc)
    plot.internalForces()

except ValueError:
    print("ESTRUTURA HIPOSTATICA")
except numpy.linalg.LinAlgError:
    print("ERRO NOS CÁLCULOS")
except TypeError:
    print("ENTRADA DE DADOS INCORRETA")
    print(traceback.format_exc())
finally:
    print("TEMPO DE CALCULO = ", time)
