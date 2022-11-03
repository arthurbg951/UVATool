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
    QPainter,

)
from PyQt5 import uic
from libs.UVATool import *
from libs.Drawing import *
from libs.Structures import Structures
from forms.FormTableResults import FormTableResults


class FormUVATool(QMainWindow):

    GraphicsView: QGraphicsView

    DrawingsToolBar: QToolBar
    NodeAction: QAction
    ElementAction: QAction

    ToolsToolBar: QToolBar
    ProcessCalculations: QAction
    actionTableResults: QAction

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

    ERA: QRadioButton
    MNE: QRadioButton

    formTableResults: FormTableResults

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/FormUVATool.ui", self)

        self.scene = UVAGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 1, 1)
        self.GraphicsView.setScene(self.scene)
        self.scene.fitStructure()

        self.ChangeValues.close()
        self.ElementParameters.close()

        self.confirmButton.clicked.connect(self.confirmClicked)
        self.confirmButton_2.clicked.connect(self.confirmClicked_2)

        self.ElementAction.triggered.connect(self.elementActionClicked)
        self.ProcessCalculations.triggered.connect(self.ProcessCalculationsTriggered)
        self.actionTableResults.triggered.connect(self.showTableReultsForm)
        self.NodeAction.triggered.connect(self.nodeActionClicked)

        self.p.textChanged.connect(self.pValueChanged)

        self.ChangeValues.visibilityChanged.connect(self.ChangeValuesClose)

        # self.GraphicsView.DragMode(1)

        self.calc = None

        self.resize(900, 650)
        self.show()

    def wheelEvent(self, event: QWheelEvent) -> None:
        """
        Zoom in or out of the view.
        """
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor
        # Save the scene pos
        oldPos = self.GraphicsView.mapToScene(event.pos())
        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
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
        if self.MNE.isChecked():
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

    def showTableReultsForm(self):
        try:
            self.formTableResults = FormTableResults(self.calc)
            self.formTableResults.showMaximized()
        except Exception as e:
            QMessageBox.warning(self, "Form Table Results Error", str(e))

    def nodeActionClicked(self):
        if self.ElementAction.isChecked():
            self.ElementAction.toggle()
            self.showElementPreview(False)
        if self.NodeAction.isChecked():
            self.showNodePreview(True)
        else:
            self.showNodePreview(False)

    def elementActionClicked(self):
        if self.NodeAction.isChecked():
            self.NodeAction.toggle()

        if self.ElementAction.isChecked():
            self.showNodePreview(True)
            self.showElementPreview(True)
        else:
            self.showNodePreview(False)
            self.showElementPreview(False)

    def elementActionClicked(self):
        if self.NodeAction.isChecked():
            self.NodeAction.toggle()

        if self.ElementAction.isChecked():
            self.showNodePreview(True)
            self.showElementPreview(True)
        else:
            self.showNodePreview(False)
            self.showElementPreview(False)

    def showNodePreview(self, changer: bool) -> None:
        if changer:
            self.scene.canDrawNode = True
            self.scene.nodePreview.show()
        else:
            self.scene.canDrawNode = False
            self.scene.nodePreview.hide()

    def showElementPreview(self, changer: bool) -> None:
        if changer:
            self.scene.canDrawLine = True
            self.scene.elementPreview.show()
        else:
            self.scene.canDrawLine = False
            self.scene.elementPreview.hide()
            self.scene.elementPreview.setLine(QLineF(QPointF(0, 0), QPointF(0, 0)))
            self.scene.mousePoint = QPointF(0, 0)
            self.scene.clickPoint = QPointF(0, 0)

    def close(self) -> bool:
        self.formTableResults.close()
        super().close()


class UVAGraphicsScene(QGraphicsScene):
    form: FormUVATool
    nodes: list[NodeDraw]
    elements: list[ElementDraw]

    def __init__(self, form: FormUVATool):
        super().__init__()
        self.form = form
        self.keyStack = []
        self.canDrawNode = False
        self.canDrawLine = False
        self.isDrawingLine = False
        self.nodePreview = NodePreview(0, 0)
        self.nodePreview.hide()
        self.clickPoint = QPointF(0, 0)
        self.mousePoint = QPointF(0, 0)
        self.elementNode1 = NodeDraw(0, 0)
        self.elementNode2 = NodeDraw(0, 0)
        self.elementPreview = ElementPreview(QLineF(self.clickPoint, self.mousePoint))
        self.elementPreview.hide()

        self.canMoveScene = False

        self.addItem(self.nodePreview)
        self.addItem(self.elementPreview)

        # NODAL FORCES É UMA LISTA DE LISTAS (UMA FORÇA PODE POSSUIR VÁRIOS ITENS)
        self.nodalForces = []
        self.nodes = []
        self.elements = []
        self.gridPoints = []

        self.loadStructure(Structures.modeloBielasETirantes())

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clickPoint.setX(event.scenePos().x())
            self.clickPoint.setY(event.scenePos().y())
            if self.canDrawNode:
                existingNode = self.verifyExistingNode(event)
                if existingNode == None:
                    node = NodeDraw(event.scenePos().x(), event.scenePos().y())
                    self.drawNode(node)
                    print('Nodes:')
                    for i in range(len(self.nodes)):
                        print(i, ' ', self.nodes[i])
                else:
                    self.clickPoint.setX(existingNode.x)
                    self.clickPoint.setY(existingNode.y)
                    self.elementPreview.setLine(QLineF(self.clickPoint, self.mousePoint))

            if self.canDrawLine:
                if self.isDrawingLine:
                    self.isDrawingLine = False
                    self.elementPreview.hide()
                    self.elementNode2 = NodeDraw(self.clickPoint.x(), self.clickPoint.y())
                    node = self.verifyExistingNode(event)
                    if node != None:
                        self.elementNode2 = node
                    element = ElementDraw(self.elementNode1, self.elementNode2, 1, 1, 1)
                    if self.verifyExistingElement(element) == None:
                        self.drawElement(element)
                        print('Elements:')
                        for i in range(len(self.elements)):
                            print(i, " ", self.elements[i])
                else:
                    self.isDrawingLine = True
                    self.elementPreview.setLine(QLineF(self.clickPoint, self.mousePoint))
                    self.elementPreview.show()
                    self.elementNode1 = NodeDraw(self.clickPoint.x(), self.clickPoint.y())
                    node = self.verifyExistingNode(event)
                    if node != None:
                        self.elementNode1 = node

        if event.button() == Qt.MouseButton.MiddleButton:
            self.canMoveScene = True

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        for item in self.items():
            if item.hasFocus():
                if isinstance(item, ElementItem):
                    item.setSelected(True)
                    for element in self.elements:
                        if element.getItem() == item:
                            self.form.area.setText(str(element.area))
                            self.form.momentInertia.setText(str(element.moment_inertia))
                            self.form.youngModulus.setText(str(element.young_modulus))
                            self.form.ChangeValues.hide()
                            self.form.ElementParameters.show()
                else:
                    isNode = isinstance(item, NodeItem)
                    isRoller = isinstance(item, RollerItem)
                    isPinned = isinstance(item, PinnedItem)
                    isFixed = isinstance(item, FixedItem)
                    isMiddleRinge = isinstance(item, MiddleRingeItem)
                    isSemiFixed = isinstance(item, SemiFixedItem)
                    if isNode or isRoller or isPinned or isFixed or isMiddleRinge or isSemiFixed:
                        item.setSelected(True)
                        for node in self.nodes:
                            if node.getItem() == item:
                                self.form.fx.setText(str(node.getNodalForce().fx))
                                self.form.fy.setText(str(node.getNodalForce().fy))
                                self.form.m.setText(str(node.getNodalForce().m))
                                self.form.p.setText(str(node.getP()))
                                if node.getSupport() == Apoio.sem_suporte:
                                    self.form.semApoio.setChecked(True)
                                elif node.getSupport() == Apoio.primeiro_genero:
                                    self.form.primeiroGenero.setChecked(True)
                                elif node.getSupport() == Apoio.segundo_genero:
                                    self.form.segundoGenero.setChecked(True)
                                elif node.getSupport() == Apoio.terceiro_genero:
                                    self.form.terceiroGenero.setChecked(True)
                                elif node.getSupport() == Apoio.semi_rigido:
                                    self.form.semiRigido.setChecked(True)
                                self.form.ElementParameters.hide()
                                self.form.ChangeValues.show()
            else:
                item.setSelected(False)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(event)
        node = self.verifyExistingNode(event)
        if node == None:
            self.nodePreview.setPos(event.scenePos().x(), event.scenePos().y())
            self.mousePoint.setX(event.scenePos().x())
            self.mousePoint.setY(event.scenePos().y())
        else:
            self.mousePoint.setX(node.x)
            self.mousePoint.setY(node.y)

        if self.isDrawingLine:
            self.elementPreview.setLine(QLineF(self.clickPoint, self.mousePoint))

        # FUNÇÃO COM BUG
        if self.canMoveScene:
            # print(self.form.GraphicsView.sceneRect())
            self.form.GraphicsView.setSceneRect(event.scenePos().x() * 0.5, event.scenePos().y() * 0.5, 1, 1)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.MiddleButton:
            self.canMoveScene = False
        self.form.GraphicsView.viewport().setCursor(Qt.CursorShape.ArrowCursor)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if not self.keyStack.__contains__(event.key()):
            self.keyStack.insert(0, event.key())
        if self.keyStack.__contains__(Qt.Key.Key_Control) and self.keyStack.__contains__(Qt.Key.Key_Z):
            if len(self.items()) > 0:
                self.removeItem(self.items()[0])
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

    def drawElement(self, element: ElementDraw) -> None:
        self.addItem(element.getItem())
        self.elements.insert(0, element)

    def verifyExistingNode(self, event: QGraphicsSceneMouseEvent) -> NodeDraw:
        if self.canDrawNode:
            for node in self.nodes:
                x1 = node.x
                y1 = node.y
                x2 = event.scenePos().x()
                y2 = event.scenePos().y()
                pointDist = math.sqrt(math.pow((y2 - y1), 2) + math.pow((x2 - x1), 2))
                if pointDist <= node.getDiameter():
                    self.nodePreview.hide()
                    return node
                else:
                    self.nodePreview.show()

    def verifyExistingElement(self, element: ElementDraw) -> ElementDraw:
        for e in self.elements:
            if e == element:
                return e

    def fitStructure(self) -> None:
        try:
            x = self.nodes[0].x
            y = self.nodes[0].y
            for node in self.nodes:
                if node.x > x:
                    x = node.x
                if node.y > y:
                    y = node.y
            print(f'Changing view to {x*10} {y*10}')
            self.form.GraphicsView.setSceneRect(x*10/2, -y*10/2, 1, 1)
        except:
            print("Ocurred an error while trying to fit structure")

    def loadStructure(self, structure: Structures):
        try:
            nodes = structure[0]
            elements = structure[1]
            nodes.append(NodeDraw(200))
            for node in nodes:
                self.drawNode(node)
            for element in elements:
                self.drawElement(element)
        except Exception as e:
            msg = "Ocurred an error whyle trying to load the writed structure.\nSkipping the load.\Error: " + str(e)
            QMessageBox.warning(self.form, "Warning", msg)
            print(msg)
