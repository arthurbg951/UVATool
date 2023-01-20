from UVATool import *


def some_magic():
    try:
        # from os.path import dirname, basename, isfile, join
        # import glob
        # modules = glob.glob(join(dirname(__file__), "*.py"))
        # __all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
        # for file in __all__:
        # import Structures
        struct = __import__('Another Structure')
        for i in dir(struct):
            item = getattr(struct, i)
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
    except TypeError:
        print('INVALID FILE!')


if __name__ == '__main__':
    some_magic()
