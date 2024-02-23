from uvatool import *
from typing import Callable


def support_test() -> bool:
    supp = Support(array([0, 0, 0, 0, 0, 0]))

    return supp == array([0, 0, 0, 0, 0, 0])


def point_test() -> bool:
    p0 = Point(0, 10, 10)

    tru_div = p0 / 10 == Point(0, 1, 1)
    eq = p0 == Point(0, 10, 10)
    eq2 = p0 == array([0, 10, 10])
    add = p0 + Point(1, 1, 2) == Point(1, 11, 12)
    dist_to = Point(10, 0, 0).dist_to(Point(0, 0, 0)) == 10
    string = str(Point(0, 0, 0)) == f'(0; 0; 0)'

    return tru_div and eq and eq2 and add and dist_to and string


def nodal_force_test() -> bool:
    f1 = NodalForce(10, 10, 10)

    eq = f1 == NodalForce(10, 10, 10)
    eq2 = f1 == array([10, 10, 10])
    add = f1 + NodalForce(10, 10, 10) == NodalForce(20, 20, 20)
    string = str(f1) == f"fx=10; fy=10; m=10"

    return eq and eq2 and add and string


def node_test() -> bool:
    n1 = Node(0, 0, 0)

    eq = n1 == Node(0, 0, 0)
    string = str(n1) == f'(0; 0; 0); [0 0 0 0 0 0]; fx=0; fy=0; m=0'
    n1.set_nodal_force(NodalForce(10, 10, 10))
    set_nodal_force = n1.get_nodal_force() == NodalForce(10, 10, 10)
    n1.set_support(Support(array([1, 1, 1, 1, 1, 1])))
    set_support = n1.get_support() == Support(array([1, 1, 1, 1, 1, 1]))
    
    return eq and set_nodal_force and string and set_support


def main() -> bool:
    import uvatool_tester

    # CARREGARÁ TODAS AS FUNÇÕES DESSE ARQUIVO QUE CONTEM "test" NO NOME
    function_stack: ndarray[Callable] = array([getattr(uvatool_tester, nome) for nome in dir(
        uvatool_tester) if callable(getattr(uvatool_tester, nome)) and nome.__contains__('test')])

    ocurred_an_error = False
    for function in function_stack:
        result = function()
        if result:
            print(Colors.green(f'{function.__name__} pass.'))
        else:
            print(Colors.red(f'Ocurred an error in {function.__name__}.'))
            ocurred_an_error = True

    return ocurred_an_error


if __name__ == "__main__":
    main()
