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
from UVATool import *
from UVATool.Enums import *
from UVATool.Exceptions import *
from libs.Drawing import *


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
        # for item in self.items():
        #     if item.hasFocus():
        #         if isinstance(item, ElementItem):
        #             item.setSelected(True)
        #             for element in self.elements:
        #                 if element.getItem() == item:
        #                     self.form.area.setText(str(element.area))
        #                     self.form.momentInertia.setText(str(element.moment_inertia))
        #                     self.form.youngModulus.setText(str(element.young_modulus))
        #                     self.form.ChangeValues.hide()
        #                     self.form.ElementParameters.show()
        #         else:
        #             isNode = isinstance(item, NodeItem)
        #             isRoller = isinstance(item, RollerItem)
        #             isPinned = isinstance(item, PinnedItem)
        #             isFixed = isinstance(item, FixedItem)
        #             isMiddleRinge = isinstance(item, MiddleRingeItem)
        #             isSemiFixed = isinstance(item, SemiFixedItem)
        #             if isNode or isRoller or isPinned or isFixed or isMiddleRinge or isSemiFixed:
        #                 item.setSelected(True)
        #                 for node in self.nodes:
        #                     if node.getItem() == item:
        #                         self.form.fx.setText(str(node.getNodalForce().fx))
        #                         self.form.fy.setText(str(node.getNodalForce().fy))
        #                         self.form.m.setText(str(node.getNodalForce().m))
        #                         self.form.p.setText(str(node.getP()))
        #                         if node.getSupport() == Apoio.sem_suporte:
        #                             self.form.semApoio.setChecked(True)
        #                         elif node.getSupport() == Apoio.primeiro_genero:
        #                             self.form.primeiroGenero.setChecked(True)
        #                         elif node.getSupport() == Apoio.segundo_genero:
        #                             self.form.segundoGenero.setChecked(True)
        #                         elif node.getSupport() == Apoio.terceiro_genero:
        #                             self.form.terceiroGenero.setChecked(True)
        #                         elif node.getSupport() == Apoio.semi_rigido:
        #                             self.form.semiRigido.setChecked(True)
        #                         self.form.ElementParameters.hide()
        #                         self.form.ChangeValues.show()
        #     else:
        #         item.setSelected(False)

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
        debug_nodes = self.nodes
        max = Point2d(0, 0)
        min = Point2d(0, 0)
        try:
            if len(self.nodes) > 0:
                for node in self.nodes:
                    if node.xDraw > max.x:
                        max.x = node.xDraw
                    if node.yDraw > max.y:
                        max.y = node.yDraw
                    if node.xDraw < min.x:
                        min.x = node.xDraw
                    if node.yDraw < min.y:
                        min.y = node.yDraw
                self.form.GraphicsView.setSceneRect((max / 2).x, (min / 2).y, 1, 1)
        except Exception as e:
            print(str(e))
            print('################# DEBUG SECTION ERROR ##################')
            print(f'max={max}')
            print(f'min={min}')
            for index in debug_nodes:
                print(index)
            print('########################################################')
            raise Exception("Ocurred an error while trying to fit structure")

    def loadStructure(self, structure: Structure):
        try:
            nodes = structure.nodes
            elements = structure.elements
            for node in nodes:
                print(node)
                self.drawNode(node)
            for element in elements:
                print(element)
                self.drawElement(element)
            # self.fitStructure()
        except Exception as e:
            msg = "Ocurred an error whyle trying to load the Structure.\nSkipping the load.\nError: " + str(e)
            QMessageBox.warning(self.form, "Warning", msg)
            import traceback
            print(traceback.format_exc())
            # print(str(e))

    def printStructure(self):
        print('##################### NODES ########################')
        for node in self.nodes:
            print(node)
        print('#################### ELEMENTS ######################')
        for element in self.elements:
            print(element)
        print('####################################################')
