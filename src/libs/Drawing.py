from libs.UVATool import *
from PyQt5.QtWidgets import (
    QGraphicsSceneMouseEvent,
    QGraphicsItem,
    QGraphicsSceneHoverEvent,
    QGraphicsEllipseItem,
    QGraphicsLineItem,

)
from PyQt5.QtCore import (
    Qt,
    QPointF,
    QLineF,
    QRectF
)
from PyQt5.QtGui import (
    QPen,
    QBrush,
    QKeyEvent,
    QColor,
    QFocusEvent,
    QGradient
)


class Point(QPointF, QGraphicsEllipseItem):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)


class NodePreview(QGraphicsEllipseItem):
    def __init__(self, x: float, y: float):
        __diameter = 10
        self.__x = x
        self.__y = y
        self.__pos = QPointF(self.__x, self.__y)
        super().__init__(QRectF(x - __diameter/2, y - __diameter/2, __diameter, __diameter))
        self.setPen(QPen(Qt.GlobalColor.black, 1))
        self.setBrush(QBrush(Qt.GlobalColor.gray, Qt.BrushStyle.SolidPattern))
        self.setZValue(1)
        # self.setAcceptHoverEvents(True)

    def setSelected(self, selected: bool) -> None:
        super().setSelected(False)

    def scenePos(self) -> QPointF:
        return self.__pos


class NodeItem(QGraphicsEllipseItem):
    def __init__(self, rec: QRectF):
        super().__init__(rec)
        self.__x = rec.x()
        self.__y = rec.y()
        self.__pos = QPointF(self.__x, self.__y)
        self.setPen(QPen(Qt.GlobalColor.black, 1))
        self.setBrush(QBrush(Qt.GlobalColor.gray, Qt.BrushStyle.SolidPattern))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setZValue(1)
        self.setFocus()
        self.setAcceptHoverEvents(True)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            if self.isSelected():
                print('Botão deletar não implementado')
        if event.key() == Qt.Key.Key_Escape:
            self.setSelected(False)

    def setColor(self, color: Qt.GlobalColor):
        self.setBrush(QBrush(color))

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.setFocus()

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.clearFocus()

    def setSelected(self, selected: bool) -> None:
        if selected:
            self.setColor(Qt.GlobalColor.red)
        else:
            self.setColor(Qt.GlobalColor.gray)

    def isSelected(self) -> bool:
        if self.brush() == QBrush(Qt.GlobalColor.red):
            return True
        else:
            return False

    def scenePos(self) -> QPointF:
        return self.__pos


class NodeDraw(Node):
    __item: NodeItem

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.__diameter = 10
        self.__rect = QRectF(self.x - self.__diameter/2, self.y - self.__diameter/2, self.__diameter, self.__diameter)
        self.__item = NodeItem(self.getRect())

    def updateDiameter(self, diameter: int) -> None:
        self.__diameter = diameter
        self.__item.setRect(self.getRect())

    def getRect(self) -> QRectF:
        return self.__rect

    def getDiameter(self) -> float:
        return self.__diameter

    def getItem(self) -> QGraphicsItem:
        return self.__item

    def getPoint(self) -> QPointF:
        return QPointF(self.x, self.y)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, NodeDraw):
            return NotImplemented
        testX = self.x + self.__diameter/2 >= __o.x and self.x - self.__diameter/2 <= __o.x
        testY = self.y + self.__diameter/2 >= __o.y and self.y - self.__diameter/2 <= __o.y
        return testX and testY


class ElementPreview(QGraphicsLineItem):
    def __init__(self, line: QLineF):
        super().__init__(line)
        self.setPen(QPen(QColor(255, 140, 0), 2, Qt.PenStyle.DashLine))


class ElementItem(QGraphicsLineItem):
    def __init__(self, line: QGraphicsLineItem) -> None:
        super().__init__()
        self.setPen(line.pen())
        self.setLine(line.line())
        self.setAcceptHoverEvents(True)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, ElementDraw):
            return NotImplemented
        return self.element == __o.element

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.setFocus()
        self.setPen(QPen(self.pen().color(), 4, self.pen().style()))

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.clearFocus()
        self.setPen(QPen(self.pen().color(), 2, self.pen().style()))

    def hasFocus(self) -> bool:
        if self.pen().width() == 4:
            return True
        else:
            return False

    def setSelected(self, selected: bool) -> None:
        width = self.pen().width()
        style = self.pen().style()
        if selected:
            self.setPen(QPen(Qt.GlobalColor.red, width, style))
        else:
            self.setPen(QPen(Qt.GlobalColor.gray, width, style))

    def isSelected(self) -> bool:
        if self.pen().color() == Qt.GlobalColor.red:
            return True
        else:
            return False


class ElementDraw(Element):
    __item: QGraphicsItem

    def __init__(self, node1: NodeDraw, node2: NodeDraw, area: float, moment_inertia: float, young_modulus: float) -> None:
        super().__init__(node1, node2, area, moment_inertia, young_modulus)
        line = QGraphicsLineItem(QLineF(node1.getPoint(), node2.getPoint()))
        line.setPen(QPen(Qt.GlobalColor.gray, 2, Qt.PenStyle.SolidLine))
        self.__item = ElementItem(line)

    def getItem(self):
        return self.__item

    def __eq__(self, other: object) -> bool:
        return super().__eq__(other)
