from UVATool.Process import Process
import numpy as np

class Print:
    __process: Process

    def __init__(self, process: Process) -> None:
        self.__process = process

    def nodalDisplacement(self) -> None:
        print('--------------------NODAL DISPLACEMENTS - {δ}--------------------')
        # preprocessing to fix node count with cuts while processing
        cuts = self.__process.getCuts()
        processed_displacement = self.__process.getNodalDisplacement()
        # None values are used because in this positions, have an reaction value, but it was not calculled at this moment by UVATool
        for cut in cuts:
            processed_displacement = np.insert(processed_displacement, cut, None)
        nNode = len(processed_displacement)
        for i in range(0, nNode, 3):
            print('Node: {0}'.format(int(i/3+1)))
            print("δx = {0:.3e} mm".format(processed_displacement[0 + i] * 1e3))
            print("δy = {0:.3e} mm".format(processed_displacement[1 + i] * 1e3))
            print("δm = {0:.3e} rad".format(processed_displacement[2 + i]))
            if i != nNode - 3:
                print()
        print('-----------------------------------------------------------------')

    def elementDeformations(self) -> None:
        print('--------------------ELEMENT DEFORMATIONS - {θ}--------------------')
        nElement = len(self.__process.getInternalForces())
        for i in range(0, nElement, 3):
            print('ELEMENT: {0}'.format(int(i/3+1)))
            print(" Δ = {0:.3e} mm".format(self.__process.getDeformations()[0 + i] * 1e3))
            print("θ1 = {0:.3e} rad".format(self.__process.getDeformations()[1 + i]))
            print("θ2 = {0:.3e} rad".format(self.__process.getDeformations()[2 + i]))
            if i != nElement - 3:
                print()
        print('-----------------------------------------------------------------')

    def internalForces(self) -> None:
        print('----------------------INTERNAL FORCES - {m}----------------------')
        nElement = len(self.__process.getInternalForces())
        for i in range(0, nElement, 3):
            print('ELEMENT: {0}'.format(int(i/3+1)))
            print(" N = {0:.1f} kN".format(self.__process.getInternalForces()[0 + i] * 1e-3))
            print("M1 = {0:.1f} kNm".format(self.__process.getInternalForces()[1 + i] * 1e-3))
            print("M2 = {0:.1f} kNm".format(self.__process.getInternalForces()[2 + i] * 1e-3))
            if i != nElement - 3:
                print()
        print('-----------------------------------------------------------------')
