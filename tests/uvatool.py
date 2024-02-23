from enum import Enum
from dataclasses import dataclass
from typing import Any
from numpy import array, ndarray, all, power
from abc import ABC, abstractmethod, abstractproperty
from math import sqrt, pow


@dataclass(slots=True)
class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    YELLOW = "\033[1;33m"
    BLACK = "\033[0;30m"
    BROWN = "\033[0;33m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"

    DARK_GRAY = "\033[1;30m"

    LIGHT_GRAY = "\033[0;37m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"

    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"

    NONE = '\u001b[0m'

    def red(text: str) -> str:
        return Colors.RED + text + Colors.NONE

    def green(text: str) -> str:
        return Colors.GREEN + text + Colors.NONE

    def blue(text: str) -> str:
        return Colors.BLUE + text + Colors.NONE

    def yellow(text: str) -> str:
        return Colors.YELLOW + text + Colors.NONE


@dataclass(slots=True)
class Point:
    x: float
    y: float
    z: float

    def __str__(self) -> str:
        return f"({self.x}; {self.y}; {self.z})"

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Point | ndarray):
            return NotImplemented
        if isinstance(__o, Point):
            return all(array([self.x, self.y, self.z]) == array([__o.x, __o.y, __o.z]))
        if isinstance(__o, ndarray):
            return all(array([self.x, self.y, self.z]) == array([__o[0], __o[1], __o[2]]))

    def __add__(self, __o: object):
        if not isinstance(__o, Point):
            return NotImplemented
        return Point(self.x + __o.x, self.y + __o.y, self.z + __o.z)

    def __truediv__(self, __o: object):
        if isinstance(__o, Point):
            # divisão de um ponto por outro (verificar existencia na geomegria analítica para implementação)
            return NotImplemented
        if isinstance(__o, float | int):
            return Point(self.x / __o, self.y / __o, self.z / __o)

    def dist_to(self, point: object):
        """Calculate de distance between 2 points"""
        if not isinstance(point, Point):
            return NotImplemented
        return sqrt(power(self.x - point.x, 2) + power(self.y - point.y, 2) + power(self.z - point.z, 2))


@dataclass(slots=True)
class Support:
    restrictions: ndarray

    def __init__(self, restrictions: ndarray = array([0, 0, 0, 0, 0, 0])):
        self.restrictions = restrictions
        self.__check_dof()

    def __str__(self) -> str:
        return f'{self.restrictions}'

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Support | ndarray):
            return NotImplemented
        if isinstance(__value, Support):
            return all(self.restrictions == __value.restrictions)
        if isinstance(__value, ndarray):
            return all(self.restrictions == __value)

    def __check_dof(self):
        if not 0 <= len(self.restrictions) <= 6:
            raise Exception(f'DoF must contains maximum of 6 positions, current={len(self.restrictions)}.')


@dataclass(slots=True)
class NodalForce:
    fx: float
    fy: float
    m: float

    def __str__(self) -> str:
        return f"fx={self.fx}; fy={self.fy}; m={self.m}"

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, NodalForce | ndarray):
            return NotImplemented
        if isinstance(__o, NodalForce):
            return all(array([self.fx, self.fy, self.m]) == array([__o.fx, __o.fy, __o.m]))
        if isinstance(__o, ndarray):
            return all(array([self.fx, self.fy, self.m]) == array([__o[0], __o[1], __o[2]]))

    def __add__(self, __o: object):
        if not isinstance(__o, NodalForce):
            return NotImplemented
        return NodalForce(self.fx + __o.fx, self.fy + __o.fy, self.m + __o.m)


@dataclass(slots=True, kw_only=True)
class Node(Point):
    __nodal_force: NodalForce = NodalForce(0, 0, 0)
    __support: Support = Support()

    def __str__(self) -> str:
        return f"{Point.__str__(self)}; {self.__support}; {self.__nodal_force}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return all(array([self.x, self.y]) == array([other.x, other.y]))

    def set_nodal_force(self, nodal_force: NodalForce) -> None:
        if not isinstance(nodal_force, NodalForce):
            raise Exception("Nodal Force must be from class NodalForce.")
        self.__nodal_force = nodal_force

    def get_nodal_force(self) -> NodalForce:
        return self.__nodal_force

    def set_support(self, support: Support) -> None:
        if not isinstance(support, Support):
            raise Exception("Support must be from class Support.")
        self.__support = support

    def get_support(self) -> Support:
        return self.__support
