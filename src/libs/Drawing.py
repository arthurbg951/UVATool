from UVATool import *
from UVATool.Enums import *
from PyQt5.QtWidgets import (
    QGraphicsSceneMouseEvent,
    QGraphicsItem,
    QGraphicsSceneHoverEvent,
    QGraphicsEllipseItem,
    QGraphicsRectItem,
    QGraphicsLineItem,
    QGraphicsPixmapItem,
    QGraphicsPolygonItem

)
from PyQt5.QtCore import (
    Qt,
    QPointF,
    QLineF,
    QRectF,
)
from PyQt5.QtGui import (
    QPen,
    QBrush,
    QKeyEvent,
    QColor,
    QFocusEvent,
    QGradient,
    QPixmap,
    QPolygonF
)


class NodalForceType:
    x = 0
    y = 1
    m = 2


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


class NodeItem(QGraphicsRectItem):
    # ESSE ITEM REPRESENTA O NÓ PADRÃO
    def __init__(self, rec: QRectF):
        super().__init__(rec)
        self.__x = rec.x()
        self.__y = rec.y()
        self.__pos = QPointF(self.__x, self.__y)
        self.setPen(QPen(Qt.GlobalColor.black, 1))
        self.setBrush(QBrush(Qt.GlobalColor.black, Qt.BrushStyle.SolidPattern))
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
            self.setColor(Qt.GlobalColor.black)

    def isSelected(self) -> bool:
        if self.brush() == QBrush(Qt.GlobalColor.red):
            return True
        else:
            return False

    def scenePos(self) -> QPointF:
        return self.__pos

    def x(self):
        return self.__x * 10

    def y(self):
        return - self.__y * 10


class MiddleRingeItem(QGraphicsEllipseItem):
    # REPRESENTA O NÓ ROTULADO
    def __init__(self, rec: QRectF):
        super().__init__(rec)
        self.__x = rec.x()
        self.__y = rec.y()
        self.__pos = QPointF(self.__x, self.__y)
        self.setPen(QPen(Qt.GlobalColor.black, 1))
        self.setBrush(QBrush(Qt.GlobalColor.white, Qt.BrushStyle.SolidPattern))
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
            self.setColor(Qt.GlobalColor.white)

    def isSelected(self) -> bool:
        if self.brush() == QBrush(Qt.GlobalColor.red):
            return True
        else:
            return False

    def scenePos(self) -> QPointF:
        return self.__pos

    def x(self):
        return self.__x * 10

    def y(self):
        return - self.__y * 10


class SemiFixedNodeItem(QGraphicsPixmapItem):
    # REPRESENTA O NÓ SEMI RIGIDO
    def __init__(self, x: float, y: float):
        super().__init__(QPixmap("icons/apoio_semi_rigido_node.png"))
        self.__x = x - self.pixmap().width()/2
        self.__y = y - self.pixmap().height()/2
        self.__pos = QPointF(self.__x, self.__y)
        self.setPos(QPointF(self.__x, self.__y))
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

    def setColor(self, color: QColor):
        tmp = self.pixmap().toImage()
        for y in range(tmp.height()):
            for x in range(tmp.width()):
                color.setAlpha(tmp.pixelColor(x, y).alpha())
                tmp.setPixelColor(x, y, color)
        self.setPixmap(QPixmap.fromImage(tmp))

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.setFocus()

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.clearFocus()

    def setSelected(self, selected: bool) -> None:
        if selected:
            self.setColor(QColor(255, 0, 0))
            self.__isSelected = True
        else:
            self.setColor(QColor(0, 0, 0))
            self.__isSelected = False

    def isSelected(self) -> bool:
        if self.__isSelected:
            return True
        else:
            return False

    def scenePos(self) -> QPointF:
        return self.__pos

    def x(self):
        return self.__x * 10

    def y(self):
        return - self.__y * 10


class RollerItem(QGraphicsPixmapItem):
    # REPRESENTA O APOIO DE PRIMEIRO GENERO
    def __init__(self, x: float, y: float):
        super().__init__(QPixmap("icons/apoio_primeiro_genero.png"))
        self.__x = x - 17
        self.__y = y - 6
        self.__pos = QPointF(self.__x, self.__y)
        self.setPos(QPointF(self.__x, self.__y))
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

    def setColor(self, color: QColor):
        tmp = self.pixmap().toImage()
        for y in range(tmp.height()):
            for x in range(tmp.width()):
                color.setAlpha(tmp.pixelColor(x, y).alpha())
                tmp.setPixelColor(x, y, color)
        self.setPixmap(QPixmap.fromImage(tmp))

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.setFocus()

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.clearFocus()

    def setSelected(self, selected: bool) -> None:
        if selected:
            self.setColor(QColor(255, 0, 0))
            self.__isSelected = True
        else:
            self.setColor(QColor(0, 0, 0))
            self.__isSelected = False

    def isSelected(self) -> bool:
        if self.__isSelected:
            return True
        else:
            return False

    def scenePos(self) -> QPointF:
        return self.__pos

    def x(self):
        return self.__x * 10

    def y(self):
        return - self.__y * 10


class PinnedItem(QGraphicsPixmapItem):
    # REPRESENTA O APOIO DE SEGUNDO GENERO
    def __init__(self, x: float, y: float):
        super().__init__(QPixmap("icons/apoio_segundo_genero.png"))
        self.__x = x - 17
        self.__y = y - 7
        self.__pos = QPointF(self.__x, self.__y)
        self.setPos(QPointF(self.__x, self.__y))
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

    def setColor(self, color: QColor):
        tmp = self.pixmap().toImage()
        for y in range(tmp.height()):
            for x in range(tmp.width()):
                color.setAlpha(tmp.pixelColor(x, y).alpha())
                tmp.setPixelColor(x, y, color)
        self.setPixmap(QPixmap.fromImage(tmp))

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.setFocus()

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.clearFocus()

    def setSelected(self, selected: bool) -> None:
        if selected:
            self.setColor(QColor(255, 0, 0))
            self.__isSelected = True
        else:
            self.setColor(QColor(0, 0, 0))
            self.__isSelected = False

    def isSelected(self) -> bool:
        if self.__isSelected:
            return True
        else:
            return False

    def scenePos(self) -> QPointF:
        return self.__pos

    def x(self):
        return self.__x * 10

    def y(self):
        return - self.__y * 10


class FixedItem(QGraphicsPixmapItem):
    # REPRESENTA O APOIO DE TERCEIRO GENERO
    def __init__(self, x: float, y: float):
        super().__init__(QPixmap("icons/apoio_terceiro_genero.png"))
        self.__x = x - 16
        self.__y = y - 15
        self.__pos = QPointF(self.__x, self.__y)
        self.setPos(QPointF(self.__x, self.__y))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setZValue(1)
        self.setFocus()
        self.setAcceptHoverEvents(True)
        self.__isSelected = False

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            if self.isSelected():
                print('Botão deletar não implementado')
        if event.key() == Qt.Key.Key_Escape:
            self.setSelected(False)

    def setColor(self, color: QColor):
        tmp = self.pixmap().toImage()
        for y in range(tmp.height()):
            for x in range(tmp.width()):
                color.setAlpha(tmp.pixelColor(x, y).alpha())
                tmp.setPixelColor(x, y, color)
        self.setPixmap(QPixmap.fromImage(tmp))

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.setFocus()

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.clearFocus()

    def setSelected(self, selected: bool) -> None:
        if selected:
            self.setColor(QColor(255, 0, 0))
            self.__isSelected = True
        else:
            self.setColor(QColor(0, 0, 0))
            self.__isSelected = False

    def isSelected(self) -> bool:
        if self.__isSelected:
            return True
        else:
            return False

    def scenePos(self) -> QPointF:
        return self.__pos

    def x(self):
        return self.__x * 10

    def y(self):
        return - self.__y * 10


class SemiFixedItem(QGraphicsPixmapItem):
    # REPRESENTA O APOIO DE SEMI RIGIDO
    def __init__(self, x: float, y: float):
        super().__init__(QPixmap("icons/apoio_semi_rigido.png"))
        self.__x = x - 15
        self.__y = y - 11
        self.__pos = QPointF(self.__x, self.__y)
        self.setPos(QPointF(self.__x, self.__y))
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

    def setColor(self, color: QColor):
        tmp = self.pixmap().toImage()
        for y in range(tmp.height()):
            for x in range(tmp.width()):
                color.setAlpha(tmp.pixelColor(x, y).alpha())
                tmp.setPixelColor(x, y, color)
        self.setPixmap(QPixmap.fromImage(tmp))

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.setFocus()

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.clearFocus()

    def setSelected(self, selected: bool) -> None:
        if selected:
            self.setColor(QColor(255, 0, 0))
            self.__isSelected = True
        else:
            self.setColor(QColor(0, 0, 0))
            self.__isSelected = False

    def isSelected(self) -> bool:
        if self.__isSelected:
            return True
        else:
            return False

    def scenePos(self) -> QPointF:
        return self.__pos

    def x(self):
        return self.__x * 10

    def y(self):
        return - self.__y * 10


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


class NodeDraw(Node):
    __item: QGraphicsItem
    __nodalForceItems: list[NodalForceItem]

    def __init__(self,node: Node) -> None:
        x = node.x
        y = node.y
        self.setP(node.getP())
        super().__init__(x, y)
        self.scaleFactor = 100
        self.xDraw = x * self.scaleFactor
        self.yDraw = - y * self.scaleFactor
        self.__diameter = 10
        self.__rect = QRectF(x * self.scaleFactor - self.__diameter/2, -y*self.scaleFactor - self.__diameter/2, self.__diameter, self.__diameter)
        self.__item = NodeItem(self.getRect())
        self.__nodalForceItems = [None, None, None]

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
        self.setPen(QPen(self.pen().color(), 4, self.pen().style()))
        self.setFocus()

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.setPen(QPen(self.pen().color(), 2, self.pen().style()))
        self.clearFocus()

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

    def setColor(self, color: QColor):
        # line = QPen(color, self.pen().width(), self.pen().style())
        # self.setPen(line)
        self.pen().setColor(Qt.GlobalColor.red)

    def isSelected(self) -> bool:
        if self.pen().color() == Qt.GlobalColor.red:
            return True
        else:
            return False


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
