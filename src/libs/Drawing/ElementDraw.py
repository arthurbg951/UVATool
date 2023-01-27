from UVATool import *
from UVATool.Enums import *
from PyQt5.QtWidgets import (
    QGraphicsLineItem,

)
from PyQt5.QtCore import (
    Qt,
    QLineF,
)
from PyQt5.QtGui import (
    QPen,
)

from libs.Drawing.ElementItem import ElementItem
from libs.Drawing.NodeDraw import NodeDraw


class ElementDraw(Element):
    __item: ElementItem

    def __init__(self, element: Element) -> None:
        super().__init__(element.node1, element.node2, element.area, element.moment_inertia, element.young_modulus)
        line = QGraphicsLineItem(QLineF(NodeDraw(element.node1).getPoint(), NodeDraw(element.node2).getPoint()))
        line.setPen(QPen(Qt.GlobalColor.gray, 2, Qt.PenStyle.SolidLine))
        self.__item = ElementItem(line)

    def getItem(self):
        return self.__item

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Element):
            normalDirection = self.node1 == other.node1 and self.node2 == other.node2
            reverseDirection = self.node1 == other.node2 and self.node2 == other.node1
            return normalDirection or reverseDirection
        else:
            return NotImplemented
