from PyQt5.QtWidgets import (
    QGraphicsScene,
    QGraphicsSceneMouseEvent,
    QMessageBox,
    QMainWindow
)
from PyQt5.QtCore import (
    Qt,
    QPointF,
)
from PyQt5.QtGui import (
    QKeyEvent,
)
from uvatool import *
from libs.Drawing import *
import traceback


class UVAGraphicsScene(QGraphicsScene):
    nodes: list[Node]
    elements: list[Element]

    def __init__(self, form: QMainWindow):
        super().__init__()
        self.form = form
        self.clickPoint = QPointF(0, 0)
        self.mousePoint = QPointF(0, 0)
        self.keyStack = []

        self.canMoveScene = False

        # NODAL FORCES É UMA LISTA DE LISTAS (UMA FORÇA PODE POSSUIR VÁRIOS ITENS)
        self.nodalForces = []
        self.nodes: list[NodeDraw] = []
        self.elements: list[ElementDraw] = []
        self.gridPoints = []

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.clickPoint.setX(event.scenePos().x())
        self.clickPoint.setY(event.scenePos().y())
        if event.button() == Qt.MouseButton.LeftButton:
            print('Qt.MouseButton.LeftButton CLICK NOT IMPLEMENTED')

        if event.button() == Qt.MouseButton.MiddleButton:
            self.canMoveScene = True

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.MouseButton.MiddleButton:
            self.form.GraphicsView.scale(1 / self.form.totalScale, 1 / self.form.totalScale)
            self.form.totalScale /= self.form.totalScale
            self.fitStructure()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.mousePoint.setX(event.scenePos().x())
        self.mousePoint.setY(event.scenePos().y())
        self.form.XCoordinate.setText(f"{self.mousePoint.x() / 100:.2f}")
        self.form.YCoordinate.setText(f"{-self.mousePoint.y() / 100:.2f}")
        super().mouseMoveEvent(event)
        if self.canMoveScene:
            velocityFactor = 0.6
            deltaX = (self.clickPoint.x() - self.mousePoint.x()) * velocityFactor
            deltaY = (self.clickPoint.y() - self.mousePoint.y()) * velocityFactor
            self.form.GraphicsView.setSceneRect(self.form.GraphicsView.sceneRect().x() + deltaX, self.form.GraphicsView.sceneRect().y() + deltaY, 1, 1)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.MiddleButton:
            self.canMoveScene = False
            self.form.GraphicsView.viewport().setCursor(Qt.CursorShape.ArrowCursor)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if not self.keyStack.__contains__(event.key()):
            self.keyStack.insert(0, event.key())
        # CONTROL + Z BEHAVIOR
        if self.keyStack.__contains__(Qt.Key.Key_Control) and self.keyStack.__contains__(Qt.Key.Key_Z):
            if len(self.items()) > 0:
                self.removeItem(self.items()[0])
        # DEL BEHAVIOR
        if event.key() == Qt.Key.Key_Delete:
            for i in range(len(self.items())):
                if self.items()[i].isSelected():
                    self.removeItem(self.items()[i])
                    break

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if self.keyStack.__contains__(event.key()):
            self.keyStack.remove(event.key())

    def drawNode(self, node: Node) -> None:
        nodeDraw = NodeDraw(node)
        self.addItem(nodeDraw.getItem())
        self.nodes.insert(0, nodeDraw)
        forcesItens = []
        forces = nodeDraw.getNodalForceItems()
        for i in range(len(forces)):
            if forces[i] is not None:
                self.addItem(forces[i])
                forcesItens.append(forces[i])
        self.nodalForces.insert(0, forcesItens)

    def removeNode(self, node: NodeDraw) -> None:
        self.removeItem(node.getItem())
        self.nodes.remove(node)

    def drawElement(self, element: Element) -> None:
        elementDraw = ElementDraw(element)
        self.addItem(elementDraw.getItem())
        self.elements.insert(0, elementDraw)

    def removeElement(self, element: ElementDraw) -> None:
        self.removeItem(element.getItem())
        self.elements.remove(element)

    def verifyExistingNode(self, x: float, y: float) -> NodeDraw:
        for node in self.nodes:
            x1 = node.x
            y1 = node.y
            if x1 == x and y1 == y:
                return node
        return None

    def verifyExistingElement(self, element: ElementDraw) -> ElementDraw:
        for e in self.elements:
            if e == element:
                return e

    def fitStructure(self) -> None:
        try:
            if len(self.nodes) > 0:
                x_max = 0
                y_min = 0
                for node in self.nodes:
                    if node.xDraw > x_max:
                        x_max = node.xDraw
                    if node.yDraw < y_min:
                        y_min = node.yDraw
                self.form.GraphicsView.setSceneRect(x_max / 2, y_min / 2, 1, 1)
        except Exception as e:
            msg = "Ocurred an error while trying to fit structure"
            QMessageBox.warning(self.form, "Warning", msg)
            print(to_red(traceback.format_exc()))

    def loadStructure(self, structure: Structure):
        try:
            nodes = structure.nodes
            elements = structure.elements
            for node in nodes:
                self.drawNode(node)
            for element in elements:
                self.drawElement(element)
            self.fitStructure()
        except Exception as e:
            msg = "Ocurred an error whyle trying to load the Structure.\nSkipping the load.\nError: " + str(e)
            QMessageBox.warning(self.form, "Warning", msg)
            print(to_red(traceback.format_exc()))

    def printStructure(self):
        print('##################### NODES ########################')
        for node in self.nodes:
            print(node)
        print('#################### ELEMENTS ######################')
        for element in self.elements:
            print(element)
        print('####################################################')
