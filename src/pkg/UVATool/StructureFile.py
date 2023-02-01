from UVATool.Structure import Structure, Node, Element
import sys
from os.path import isfile, basename, dirname, abspath


class StructureFile:
    """
    """
    # This class define a how to load a script file (.py)
    # for now, it just load a script file with a Structure defined
    # possible improovements: verify if the file contains some var with list[Nodes] and list[Elements] and try to load it

    def __init__(self, file_name: str, verbose: bool = True) -> None:
        self.file_name = file_name
        self.__checkFile(file_name)
        self.verbose = verbose
        self.__structure: list[Structure] = []
        self.__findStructure()

    def __checkFile(self, file_name: str):
        if not isfile(file_name):
            raise Exception('File not Exist!')

    def __writeOutput(self, msg: str) -> None:
        if self.verbose:
            print(msg)

    def __addStructure(self, item: Structure) -> None:
        self.__structure.append(item)

    def __findStructure(self) -> list[Structure]:
        path = abspath(dirname(self.file_name))
        module_name = basename(self.file_name)[:-3]
        sys.path.append(path)
        struct = __import__(module_name)

        self.__writeOutput(f"path={path}")
        self.__writeOutput(f"module_name={module_name}")
        self.__writeOutput(f"StructureFile={struct}")

        from types import FunctionType
        for i in dir(struct):
            item = getattr(struct, i)

            # PRINT ALL ITEM VALUE AND TYPE
            # self.__writeOutput(f"item={item}, type={type(item)}")

            # CHECK IF IS NODE OR ELEMENT
            if isinstance(item, Node) or isinstance(item, Element):
                self.__writeOutput(f"item={item}, type={type(item)}")

            # CHECK IF IS A FUNCTION
            if isinstance(item, FunctionType):
                self.__writeOutput(f"item()={item()}, type={type(item())}")
                # CHECK IF IS A FUNCTION WITH A STRUCTURE
                if isinstance(item(), Structure):
                    self.__addStructure(item())

            # CHECK IF IS A STANDALONE STRUCTURE
            if isinstance(item, Structure):
                self.__addStructure(item)
        self.__writeOutput(f"Founded {len(self.__structure)} structures in this File.")
        if len(self.__structure) == 0:
            raise Exception('This file not contains a Structure!')

    def getStructure(self) -> list[Structure]:
        return self.__structure
