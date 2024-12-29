from PyQt5.QtWidgets import (
    QGraphicsPolygonItem

)
from PyQt5.QtCore import (
    Qt,
    QPointF,
)
from PyQt5.QtGui import (
    QPen,
    QBrush,
    QPolygonF
)
from libs.Drawing.Enums import NodalForceType

class NodalForceItem(QGraphicsPolygonItem):
    def __init__(self, nodalForceType: NodalForceType, forceValue: float, xDraw, yDraw):
        self.xDraw = xDraw
        self.yDraw = yDraw
        self.__arrowSizeOffset = 15  # px
        self.__arrow = QPolygonF()
        if nodalForceType == NodalForceType.x:
            if forceValue > 0:
                self.__setArrowLeft()
            else:
                self.__setArrowRight()
        elif nodalForceType == NodalForceType.y:
            if forceValue > 0:
                self.__setArrowUp()
            else:
                self.__setArrowDown()
        elif nodalForceType == NodalForceType.m:
            if forceValue > 0:
                self.__setCounterclockwise()
            else:
                self.__setClockwise()
        super().__init__(self.__arrow)
        self.setPen(QPen(Qt.GlobalColor.blue, 2))
        self.setBrush(QBrush(Qt.GlobalColor.blue, Qt.BrushStyle.SolidPattern))
        self.setZValue(1)

    def __setArrowDown(self):
        self.__arrow.append(QPointF(self.xDraw, self.yDraw - self.__arrowSizeOffset))
        self.__arrow.append(QPointF(self.xDraw + self.__arrowSizeOffset/2, self.yDraw - 2*self.__arrowSizeOffset))
        self.__arrow.append(QPointF(self.xDraw, self.yDraw - 2*self.__arrowSizeOffset))
        self.__arrow.append(QPointF(self.xDraw, self.yDraw - 2*self.__arrowSizeOffset - self.__arrowSizeOffset))
        self.__arrow.append(QPointF(self.xDraw, self.yDraw - 2*self.__arrowSizeOffset))
        self.__arrow.append(QPointF(self.xDraw - self.__arrowSizeOffset/2, self.yDraw - 2*self.__arrowSizeOffset))

    def __setArrowUp(self):
        self.__arrow.append(QPointF(self.xDraw, self.yDraw + self.__arrowSizeOffset))
        self.__arrow.append(QPointF(self.xDraw + self.__arrowSizeOffset/2, self.yDraw + 2*self.__arrowSizeOffset))
        self.__arrow.append(QPointF(self.xDraw, self.yDraw + 2*self.__arrowSizeOffset))
        self.__arrow.append(QPointF(self.xDraw, self.yDraw + 2*self.__arrowSizeOffset + self.__arrowSizeOffset))
        self.__arrow.append(QPointF(self.xDraw, self.yDraw + 2*self.__arrowSizeOffset))
        self.__arrow.append(QPointF(self.xDraw - self.__arrowSizeOffset/2, self.yDraw + 2*self.__arrowSizeOffset))

    def __setArrowRight(self):
        self.__arrow.append(QPointF(self.xDraw + self.__arrowSizeOffset, self.yDraw))
        self.__arrow.append(QPointF(self.xDraw + 2*self.__arrowSizeOffset, self.yDraw - self.__arrowSizeOffset/2))
        self.__arrow.append(QPointF(self.xDraw + 2*self.__arrowSizeOffset, self.yDraw))
        self.__arrow.append(QPointF(self.xDraw + 2*self.__arrowSizeOffset + self.__arrowSizeOffset, self.yDraw))
        self.__arrow.append(QPointF(self.xDraw + 2*self.__arrowSizeOffset, self.yDraw))
        self.__arrow.append(QPointF(self.xDraw + 2*self.__arrowSizeOffset, self.yDraw + self.__arrowSizeOffset/2))

    def __setArrowLeft(self):
        self.__arrow.append(QPointF(self.xDraw - self.__arrowSizeOffset, self.yDraw))
        self.__arrow.append(QPointF(self.xDraw - 2*self.__arrowSizeOffset, self.yDraw - self.__arrowSizeOffset/2))
        self.__arrow.append(QPointF(self.xDraw - 2*self.__arrowSizeOffset, self.yDraw))
        self.__arrow.append(QPointF(self.xDraw - 2*self.__arrowSizeOffset - self.__arrowSizeOffset, self.yDraw))
        self.__arrow.append(QPointF(self.xDraw - 2*self.__arrowSizeOffset, self.yDraw))
        self.__arrow.append(QPointF(self.xDraw - 2*self.__arrowSizeOffset, self.yDraw + self.__arrowSizeOffset/2))

    def __setClockwise(self):
        raise NotImplementedError

    def __setCounterclockwise(self):
        raise NotImplementedError
