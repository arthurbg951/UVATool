from libs.UVATool import *


def some_magic():
    import Structures
    for i in dir(Structures):
        item = getattr(Structures, i)
        # SE FOR UMA ESTRUTURA, O UVATOOL PODE EXECUTAR UMA SIMULAÇÃO
        if isinstance(item, Structure):
            print(f"Foi encontrado uma estrutura de nome '{item.structure_name}'")
        # CONSIGO ENCONTRAR TANTO NODES QUANTO ELEMENTOS EM UM ARQUIVO
        if isinstance(item, Node):
            print('Encontrei um node')
        if isinstance(item, Element):
            print('Encontrei um element')
        # É POSSÍVEL AINDA PROCURAR POR LISTA DE NÓS E ELEMENTOS EM UM ARQUIVO
        if isinstance(item, list):
            if isinstance(item[0], Node):
                print('Encontrei uma lista de Nodes')
            if isinstance(item[0], Element):
                print('Encontrei uma lista de Elements')


if __name__ == '__main__':
    some_magic()
