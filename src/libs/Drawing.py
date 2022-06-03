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


class NodeDraw(QGraphicsEllipseItem):
    node: Node

    def __init__(self, x: float, y: float):
        self.__sceneXPos = x
        self.__sceneYPos = y
        self.raio = 10
        rec = QRectF(x - self.raio/2, y - self.raio/2, self.raio, self.raio)
        pen = QPen(Qt.GlobalColor.black, 1)
        brush = QBrush(Qt.GlobalColor.gray, Qt.BrushStyle.SolidPattern)
        super().__init__(rec)
        self.node = Node(x/100, y/100)
        self.setPen(pen)
        self.setBrush(brush)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setZValue(1)
        self.setFocus()

        self.setAcceptHoverEvents(True)

    # def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
    #     super().mousePressEvent(event)
    #     self.setColor(Qt.GlobalColor.red)
    #     self.setSelected(True)
    #     print('Element Clicked')

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            if self.isSelected():
                print('Botão deletar não implementado')

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
        return QPointF(self.__sceneXPos, self.__sceneYPos)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, NodeDraw):
            return NotImplemented
        testX = self.__sceneXPos + self.raio >= __o.__sceneXPos and self.__sceneXPos - self.raio <= __o.__sceneXPos
        testY = self.__sceneYPos + self.raio >= __o.__sceneYPos and self.__sceneYPos - self.raio <= __o.__sceneYPos
        return testX and testY
        # return self.node == __o.node


class ElementDraw(QGraphicsLineItem):
    element: Element

    def __init__(self, line: QGraphicsLineItem) -> None:
        super().__init__()
        node1, node2 = self.__verifyPointsAndGetNodes(line.line())
        self.element = Element(node1.node, node2.node, 1, 1, 1)
        self.setPen(line.pen())
        self.setLine(line.line())
        self.setAcceptHoverEvents(True)
        self.isDrawed = False

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, ElementDraw):
            return NotImplemented
        return self.element == __o.element

    def __verifyPointsAndGetNodes(self, line: QLineF) -> tuple[NodeDraw]:
        node1 = NodeDraw(line.p1().x(), line.p1().y())
        node2 = NodeDraw(line.p2().x(), line.p2().y())
        if node1.node == node2.node:
            range = 1e10-31
            node2 = NodeDraw(line.p2().x() + range, line.p2().y() - range)
        return node1, node2

    def setArea(self, area: float) -> None:
        self.element.area = area

    def setInertia(self, moment_inertia: float) -> None:
        self.element.moment_inertia = moment_inertia

    def setYoungModulus(self, young_modulus: float) -> None:
        self.element.young_modulus = young_modulus

    def setNode1(self, node1: NodeDraw) -> None:
        self.element.node1 = node1.node

    def setNode2(self, node2: NodeDraw) -> None:
        self.element.node2 = node2.node

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.setFocus()
        if self.isDrawed:
            self.setPen(QPen(self.pen().color(), 4, self.pen().style()))

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.clearFocus()
        if self.isDrawed:
            self.setPen(QPen(self.pen().color(), 2, self.pen().style()))

    # def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
    #     super().mousePressEvent(event)
    #     self.setPen(QPen(QPen(Qt.GlobalColor.red, 2, Qt.PenStyle.SolidLine)))
    #     self.setSelected(True)
    #     print('Element Clicked')

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
