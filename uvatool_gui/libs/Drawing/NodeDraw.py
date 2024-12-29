from uvatool import *
from PyQt5.QtWidgets import (
    QGraphicsItem,

)
from PyQt5.QtCore import (
    QPointF,
    QRectF,
)
from PyQt5.QtGui import (
    QColor,
)
from libs.Drawing.NodalForceItem import NodalForceItem
from libs.Drawing.RollerItem import RollerItem
from libs.Drawing.PinnedItem import PinnedItem
from libs.Drawing.FixedItem import FixedItem
from libs.Drawing.MiddleRingeItem import MiddleRingeItem
from libs.Drawing.SemiFixedItem import SemiFixedItem
from libs.Drawing.NodeItem import NodeItem
from libs.Drawing.SemiFixedNodeItem import SemiFixedNodeItem
from libs.Drawing.Enums import *



class NodeDraw(Node):
    __item: QGraphicsItem = None
    __nodalForceItems: list[NodalForceItem] = [None, None, None]

    def __init__(self, node: Node) -> None:
        x = node.x
        y = node.y
        super().__init__(x, y)
        self.scaleFactor = 100
        self.xDraw = x * self.scaleFactor
        self.yDraw = - y * self.scaleFactor
        self.__diameter = 10
        self.__rect = QRectF(x * self.scaleFactor - self.__diameter/2, -y*self.scaleFactor - self.__diameter/2, self.__diameter, self.__diameter)
        self.setSupport(node.getSupport())
        self.setP(node.getP())
        self.setNodalForce(node.getNodalForce())

    def getRect(self) -> QRectF:
        return self.__rect

    def getDiameter(self) -> float:
        return self.__diameter

    def getItem(self) -> QGraphicsItem:
        return self.__item

    def getPoint(self) -> QPointF:
        return QPointF(self.x * self.scaleFactor, - self.y * self.scaleFactor)

    def setColor(self, color: QColor):
        self.__item.setColor(color)

    def setSupport(self, support: Support) -> None:
        super().setSupport(support)
        if support == Support.roller:
            self.__item = RollerItem(self.xDraw, self.yDraw)
        elif support == Support.pinned:
            self.__item = PinnedItem(self.xDraw, self.yDraw)
        elif support == Support.fixed:
            self.__item = FixedItem(self.xDraw, self.yDraw)
        elif support == Support.middle_hinge:
            self.__item = MiddleRingeItem(self.getRect())
        elif support == Support.semi_fixed:
            self.__item = SemiFixedItem(self.xDraw, self.yDraw)
        elif support == Support.no_support:
            self.__item = NodeItem(self.getRect())
        else:
            raise Exception("Not Found a Support for this node.")

    def setP(self, p: float) -> None:
        super().setP(p)
        if p > 0 and p != 1:
            self.__item = SemiFixedNodeItem(self.xDraw, self.yDraw)
        if p == 0:
            self.__item = MiddleRingeItem(self.getRect())

    def setNodalForce(self, nodalForce: NodalForce) -> None:
        super().setNodalForce(nodalForce)
        if nodalForce.fx != 0:
            self.__nodalForceItems[0] = NodalForceItem(NodalForceType.x, nodalForce.fx, self.xDraw, self.yDraw)
        if nodalForce.fy != 0:
            self.__nodalForceItems[1] = NodalForceItem(NodalForceType.y, nodalForce.fy, self.xDraw, self.yDraw)
        if nodalForce.m != 0:
            self.__nodalForceItems[2] = NodalForceItem(NodalForceType.m, nodalForce.m, self.xDraw, self.yDraw)

    def getNodalForceItems(self) -> list[NodalForceItem]:
        return self.__nodalForceItems

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, NodeDraw):
            return NotImplemented
        testX = self.getItem().x() + self.__diameter/2 >= __o.getItem().x() and self.getItem().x() - self.__diameter/2 <= __o.getItem().x()
        testY = self.getItem().y() + self.__diameter/2 >= __o.getItem().y() and self.getItem().y() - self.__diameter/2 <= __o.getItem().y()
        return testX and testY
