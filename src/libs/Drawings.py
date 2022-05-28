from PyQt5.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsSceneMouseEvent,
    QGraphicsSceneHoverEvent,
    QDockWidget,
    QGraphicsScene,
    QGraphicsItem,
    QAction
)
from PyQt5.QtGui import (
    QKeyEvent,
    QBrush,
    QPen,
)
from PyQt5.QtCore import Qt

from libs.UVATool import *


class Canvas(object):
    def __init__(self) -> None:
        self.nodes = []
        self.drawnNodes = []
        # self.elements = []
        # self.drawnElements = []
        # self.loadings = []
        # self.drawnLoadings = []
        # self.grid = Grid()


class Grid(object):
    def __init__(self) -> None:
        self.points = []
        self.isActive = False


class Defaults(object):
    area = 1
    momentoDeInercia = 1
    moduloDeElasticidade = 1


class NodeDrawing(QGraphicsEllipseItem):
    def __init__(self):
        super().__init__()
        self.setAcceptHoverEvents(True)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.setColor(Qt.GlobalColor.red)

    def setColor(self, color: Qt.GlobalColor):
        self.setBrush(QBrush(color))

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent):
        self.setColor(Qt.GlobalColor.red)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent):
        self.setColor(Qt.GlobalColor.gray)


class UVAGraphicsScene(QGraphicsScene):
    def __init__(self, nodeAction: QAction, elementAction: QAction):
        super().__init__()
        self.nodeAction = nodeAction
        self.elementAction = elementAction

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            if self.nodeAction.isChecked():
                node = Node(event.scenePos().x(), event.scenePos().y())
                self.createNode(node)

    def createNode(self, node: Node):
        pen = QPen(Qt.GlobalColor.black, 2)
        brush = QBrush(Qt.GlobalColor.gray, Qt.BrushStyle.SolidPattern)

        raio = 10
        nodeDraw = NodeDrawing()
        nodeDraw.setRect(node.x, node.y, raio, raio)
        nodeDraw.setPen(pen)
        nodeDraw.setBrush(brush)

        self.addItem(nodeDraw)
        nodeDraw.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        nodeDraw.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        nodeDraw.setFocus()

        # self.canvas.nodes.append(node)
        # self.canvas.nodesDrawed.append(nodeDraw)
