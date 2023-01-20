from UVATool.NodalForce import NodalForce
from UVATool.Enums.Support import Support
from UVATool.Exceptions.StructureError import StructureError


class Node:
    x: float
    y: float
    __nodal_force: NodalForce
    __support: Support
    __p: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.__support = Support.no_support
        self.__p = 1
        self.__nodal_force = NodalForce(0, 0, 0)

    def __str__(self) -> str:
        return f"x={self.x},y={self.y},p={self.getP()}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __checkP(self, p) -> float:
        if p == 0 and self.__support != Support.middle_hinge:
            p = 1e-31
        if p >= 4:
            raise StructureError("P must be less than 4")
        if p < 0:
            raise StructureError("P must be greater than or equal to 0")
        return p

    def setP(self, p: float) -> None:
        if p == 0:
            self.__support = Support.middle_hinge
        p = self.__checkP(p)
        self.__p = p

    def getP(self) -> float:
        return self.__p

    def __checkSupport(self, support: Support) -> None:
        test = True
        s1 = Support.fixed
        s2 = Support.middle_hinge
        s3 = Support.no_support
        s4 = Support.semi_fixed
        s5 = Support.roller
        s6 = Support.pinned
        for sup in [s1, s2, s3, s4, s5, s6]:
            if support == sup:
                test = False
        if test:
            raise StructureError("Support needs to be from class Support.")

    def setSupport(self, support: Support) -> None:
        self.__checkSupport(support)
        if support == Support.middle_hinge:
            self.setP(0)
        self.__support = support

    def getSupport(self) -> Support:
        return self.__support

    def setNodalForce(self, nodal_force: NodalForce) -> None:
        if not isinstance(nodal_force, NodalForce):
            raise StructureError("Nodal Force must be from class NodalForce.")
        self.__nodal_force = nodal_force

    def getNodalForce(self) -> NodalForce:
        return self.__nodal_force
