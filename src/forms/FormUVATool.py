from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QMainWindow,
    QAction,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsSceneMouseEvent,
    QDialog,
    QToolBar,
    QGroupBox,
    QDockWidget,
    QGraphicsItem,
    QGraphicsSceneHoverEvent,
    QGraphicsEllipseItem,
    QLineEdit,
    QRadioButton,
    QGraphicsLineItem,
    QGraphicsSceneWheelEvent,
    QGraphicsSceneDragDropEvent,
    QMessageBox,
)
from PyQt5.QtCore import (
    Qt,
    QPointF,
    QLineF,
    QEvent,
    QObject,
    QThread,
    pyqtSignal
)
from PyQt5.QtGui import (
    QPixmap,
    QPen,
    QPolygonF,
    QBrush,
    QMouseEvent,
    QKeyEvent,
    QColor,
    QShowEvent,
    QWheelEvent,
    QPainter
)
from PyQt5 import uic
from UVATool import *
from libs.Drawing import *
from libs.DockWidgets.CreateNode import CreateNode
from libs.DockWidgets.Browser import Browser
from libs.Structures import Structures
from forms.FormTableResults import FormTableResults
from time import sleep


class FormUVATool(QMainWindow):

    GraphicsView: QGraphicsView

    DrawingsToolBar: QToolBar
    NodeAction: QAction
    ElementAction: QAction

    ToolsToolBar: QToolBar
    ProcessCalculations: QAction
    actionTableResults: QAction
    actionBrowser: QAction

    ChangeValues: QDockWidget
    fx: QLineEdit
    fy: QLineEdit
    m: QLineEdit
    p: QLineEdit
    primeiroGenero: QRadioButton
    segundoGenero: QRadioButton
    terceiroGenero: QRadioButton
    semiRigido: QRadioButton
    semApoio: QRadioButton
    confirmButton: QPushButton

    ElementParameters: QDockWidget
    area: QLineEdit
    momentInertia: QLineEdit
    youngModulus: QLineEdit
    confirmButton_2: QPushButton

    XCoordinate: QLineEdit
    YCoordinate: QLineEdit

    formTableResults: FormTableResults

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/FormUVATool.ui", self)

        self.scene = UVAGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 1, 1)
        self.GraphicsView.setScene(self.scene)

        """# DOCK WIDGETS AREA #"""
        self.ChangeValues.close()
        self.ElementParameters.close()
        # DOCK PARA ADICIONAR NOVO NODE
        self.nodePatameters = CreateNode(self.scene)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.nodePatameters)
        self.nodePatameters.close()
        # DOCK BROWSER
        self.browser = Browser(self.scene)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.browser)
        self.actionBrowser.setChecked(True)
        """# DOCK WIDGETS AREA #"""

        self.confirmButton.clicked.connect(self.confirmClicked)
        self.confirmButton_2.clicked.connect(self.confirmClicked_2)

        self.ElementAction.triggered.connect(self.elementActionClicked)
        self.ProcessCalculations.triggered.connect(self.ProcessCalculationsTriggered)
        self.actionTableResults.triggered.connect(self.showTableReultsForm)
        self.NodeAction.triggered.connect(self.nodeActionClicked)
        self.actionBrowser.triggered.connect(self.browserActionClicked)

        self.p.textChanged.connect(self.pValueChanged)

        self.ChangeValues.visibilityChanged.connect(self.ChangeValuesClose)

        # self.GraphicsView.DragMode(1)

        self.calc = None
        self.totalScale: float = 1

        # self.resize(900, 650)
        self.showMaximized()
        # self.show()

    def wheelEvent(self, event: QWheelEvent) -> None:
        """
        Zoom in or out of the view.
        """
        if self.GraphicsView.underMouse():
            zoomInFactor = 1.25
            zoomOutFactor = 1 / zoomInFactor
            # Save the scene pos
            oldPos = self.GraphicsView.mapToScene(event.pos())
            # Zoom
            if event.angleDelta().y() > 0:
                zoomFactor = zoomInFactor
            else:
                zoomFactor = zoomOutFactor
            self.totalScale *= zoomFactor
            self.GraphicsView.scale(zoomFactor, zoomFactor)
            # Get the new position
            newPos = self.GraphicsView.mapToScene(event.pos())
            # Move scene to old position
            delta = newPos - oldPos
            self.GraphicsView.translate(delta.x(), delta.y())

    def confirmClicked(self):
        for item in self.scene.items():
            try:
                if isinstance(item, NodeItem):
                    if item.isSelected():
                        for node in self.scene.nodes:
                            if node.getItem() == item:
                                fx = float(self.fx.text())
                                fy = float(self.fy.text())
                                m = float(self.m.text())
                                p = float(self.p.text())
                                node.setNodalForce(NodalForce(fx, fy, m))
                                node.setP(p)
                                if self.primeiroGenero.isChecked():
                                    node.setSupport(Apoio.primeiro_genero)
                                elif self.segundoGenero.isChecked():
                                    node.setSupport(Apoio.segundo_genero)
                                elif self.terceiroGenero.isChecked():
                                    node.setSupport(Apoio.terceiro_genero)
                                elif self.semiRigido.isChecked():
                                    node.setSupport(Apoio.semi_rigido)
                                elif self.semApoio.isChecked():
                                    node.setSupport(Apoio.sem_suporte)
                if isinstance(item, ElementDraw):
                    if item.isSelected():
                        for element in self.scene.elements:
                            if element.getItem() == item:
                                area = float(self.area.text())
                                inertia = float(self.momentInertia.text())
                                young_modulus = float(self.youngModulus.text())
                                element.area = area
                                element.moment_inertia = inertia
                                element.young_modulus = young_modulus
            except StructureError as se:
                QMessageBox.warning(self, "Warning", str(se))
                self.p.setText("")

    def confirmClicked_2(self):
        for item in self.scene.items():
            if isinstance(item, ElementDraw):
                if item.isSelected():
                    item.element.area = float(self.area.text())
                    item.element.moment_inertia = float(self.momentInertia.text())
                    item.element.young_modulus = float(self.youngModulus.text())

    def ChangeValuesClose(self):
        if not self.ChangeValues.isVisible():
            for item in self.scene.items():
                if item.isSelected():
                    item.setSelected(False)
                if isinstance(item, NodeDraw):
                    item.setColor(Qt.GlobalColor.gray)

    def pValueChanged(self):
        if self.p.text() == "0":
            self.semApoio.setChecked(True)
        elif self.p.text() == "1":
            self.semApoio.setChecked(True)

    def ProcessCalculationsTriggered(self):
        self.ChangeValues.close()
        self.ElementParameters.close()

        print()
        print("----------------------------------------------")
        print("            Processando Cálculos              ")
        analise = 0
        if self.browser.radioButton_2.isChecked():
            analise = Analise.rigidoPlastica.viaMinimaNormaEuclidiana
            print("         Via Mínima Norma Euclidiana          ")

        else:
            analise = Analise.elastica.viaRigidezAnalitica
            print("            Via Rigidez Analítica             ")

        print("----------------------------------------------")
        try:
            nodes = []
            elements = []

            for node in reversed(self.scene.nodes):
                nodes.append(node)
                # print('Node: support=', node.getSupport(), " p=", node.getP(), " node=", node.getPoint(), "fx=", node.getNodalForce().fx)
            for element in reversed(self.scene.elements):
                elements.append(element)
                # print('Element: node1=', element.node1, " node2=", element.node2)

            if len(nodes) == 0 and len(elements) == 0:
                raise Exception("Não existe nenhuma estrutura!")

            calc = Process(nodes, elements, analise)
            self.calc = calc
            plot = Print(calc)
            plot.internalForces()
        except Exception as e:
            QMessageBox.warning(self, "Warning", str(e))
            print("Error: " + str(e))

        print("----------------------------------------------")
        print()
        QMessageBox.warning(self, "Success", "A solution was founded.")

    def showTableReultsForm(self):
        try:
            self.formTableResults = FormTableResults(self.calc)
            self.formTableResults.showMaximized()
        except Exception as e:
            QMessageBox.warning(self, "Form Table Results Error", str(e))

    def nodeActionClicked(self):
        if self.ElementAction.isChecked():
            self.ElementAction.toggle()
        if self.NodeAction.isChecked():
            self.nodePatameters.show()
        else:
            self.nodePatameters.close()

    def elementActionClicked(self):
        if self.NodeAction.isChecked():
            self.NodeAction.toggle()

    def elementActionClicked(self):
        if self.NodeAction.isChecked():
            self.NodeAction.toggle()

    def browserActionClicked(self):
        self.browser.updateStructureList()
        if self.actionBrowser.isChecked():
            self.browser.show()
            self.actionBrowser.setChecked(True)
        else:
            self.browser.hide()
            self.actionBrowser.setChecked(False)

    def close(self) -> bool:
        self.formTableResults.close()
        super().close()


class UVAGraphicsScene(QGraphicsScene):
    nodes: list[NodeDraw]
    elements: list[ElementDraw]

    def __init__(self, form: FormUVATool):
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

        self.loadStructure(Structures.porticosSucessivos(n_pilares_por_andar=2, n_andares=20))
        # self.printStructure()

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
            self.form.GraphicsView.scale(1/self.form.totalScale, 1/self.form.totalScale)
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

    def drawNode(self, node: NodeDraw) -> None:
        self.addItem(node.getItem())
        self.nodes.insert(0, node)
        forcesItens = []
        forces = node.getNodalForceItems()
        for i in range(len(forces)):
            if forces[i] is not None:
                self.addItem(forces[i])
                forcesItens.append(forces[i])
        self.nodalForces.insert(0, forcesItens)

    def removeNode(self, node: NodeDraw) -> None:
        self.removeItem(node.getItem())
        self.nodes.remove(node)

    def drawElement(self, element: ElementDraw) -> None:
        self.addItem(element.getItem())
        self.elements.insert(0, element)

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
        try:
            max = Point2d(0, 0)
            min = Point2d(0, 0)
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
            self.form.GraphicsView.setSceneRect((max/2).x, (min/2).y, 1, 1)
        except Exception as e:
            print(str(e))
            print('################# DEBUG SECTION ERROR ##################')
            for index in debug_nodes:
                print(index)
            print('########################################################')
            raise Exception("Ocurred an error while trying to fit structure")

    def loadStructure(self, structure: Structures):
        try:
            nodes = structure[0]
            elements = structure[1]
            for node in nodes:
                self.drawNode(node)
            for element in elements:
                self.drawElement(element)
            self.fitStructure()
        except Exception as e:
            msg = "Ocurred an error whyle trying to load the writed structure.\nSkipping the load.\nError: " + str(e)
            QMessageBox.warning(self.form, "Warning", msg)
            print(msg)

    def printStructure(self):
        print('##################### NODES ########################')
        for node in self.nodes:
            print(node)
        print('#################### ELEMENTS ######################')
        for element in self.elements:
            print(element)
        print('####################################################')
