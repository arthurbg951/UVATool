from UVATool import *
from UVATool.Enums import *
from numpy.linalg import LinAlgError

# DEFININDO NÓS
n1 = Node(0, 0)
n2 = Node(1, 0)
n3 = Node(2, 0)

# DEFININDO APOIOS
n1.setSupport(Apoio.segundo_genero)
n2.setSupport(Apoio.rotula)
n3.setSupport(Apoio.primeiro_genero)

# DEFININDO FORÇA
n2.setNodalForce(NodalForce(0, -10, 0))

# DEFININDO ELEMENTO
e1 = Element(n1, n2, 1, 1, 1)
e2 = Element(n2, n3, 1, 1, 1)

nodes = [n1, n2, n3]
elements = [e1, e2]


if __name__ == "__main__":
    try:
        calc = Process(nodes, elements)
        plot = Print(calc)
        plot.internalForces()
    except LinAlgError as e:
        print(e.args[0])
        print("O ERRO DEVE SER INVESTIGADO PARA DEMONSTRAR QUE A ESTRUTRURA É HIPOSTÁTICA ...")
else:
    structure = Structure('ESTRUTURA HIPOSTÁTICA COM ERRO PARA CORREÇÃO', nodes, elements)
