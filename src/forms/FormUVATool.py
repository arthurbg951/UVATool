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
            print(str(e))

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

        self.addItem(self.nodePreview)
        self.addItem(self.elementPreview)

        self.nodes = []
        self.elements = []
        self.gridPoints = []

        # self.edificio3Andares()
        # self.balanco()
        # self.porticosSucessivos()
        self.modelotcc()

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

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        for item in self.items():
            if item.hasFocus():
                if isinstance(item, NodeItem):
                    item.setColor(Qt.GlobalColor.red)
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
                if isinstance(item, ElementItem):
                    item.setColor(Qt.GlobalColor.red)
                    for element in self.elements:
                        if element.getItem() == item:
                            self.form.area.setText(str(element.area))
                            self.form.momentInertia.setText(str(element.moment_inertia))
                            self.form.youngModulus.setText(str(element.young_modulus))
                            self.form.ChangeValues.hide()
                            self.form.ElementParameters.show()
            else:
                if isinstance(item, NodeItem):
                    item.setColor(Qt.GlobalColor.gray)
                if isinstance(item, ElementItem):
                    item.setColor(Qt.GlobalColor.gray)

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

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        self.form.GraphicsView.viewport().setCursor(Qt.CursorShape.ArrowCursor)

    def drawNode(self, node: NodeDraw):
        self.addItem(node.getItem())
        self.nodes.insert(0, node)

    def drawElement(self, element: ElementDraw):
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

    def verifyExistingElement(self, element: ElementDraw):
        for e in self.elements:
            if e == element:
                return e

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

    def fitStructure(self):
        x = self.nodes[0].x
        y = self.nodes[0].y
        for node in self.nodes:
            if node.x > x:
                x = node.x
            if node.y > y:
                y = node.y
        print(f'Changing view to {x*10} {y*10}')
        self.form.GraphicsView.setSceneRect(x*10/2, -y*10/2, 1, 1)

    def edificio3Andares(self):
        secao = Rectangle(0.12, 0.01)
        area = secao.area
        inercia = secao.inertia
        young = 200e9
        n1 = NodeDraw(0, -0)
        n2 = NodeDraw(150, -0)
        n3 = NodeDraw(0, -30)
        n4 = NodeDraw(150, -30)
        n5 = NodeDraw(0, -60)
        n6 = NodeDraw(150, -60)
        n7 = NodeDraw(0, -90)
        n8 = NodeDraw(150, -90)
        print(n2.x, n2.y, n2.getItem().x(), n2.getItem().y())
        n1.setSupport(Apoio.segundo_genero)
        n2.setSupport(Apoio.primeiro_genero)
        n3.setNodalForce(NodalForce(-100, 0, 0))
        n5.setNodalForce(NodalForce(-100, 0, 0))
        n7.setNodalForce(NodalForce(-100, 0, 0))
        e1 = ElementDraw(n1, n3, area, inercia, young)
        e2 = ElementDraw(n2, n4, area, inercia, young)
        e3 = ElementDraw(n3, n4, area, inercia, young)
        e4 = ElementDraw(n3, n5, area, inercia, young)
        e5 = ElementDraw(n4, n6, area, inercia, young)
        e6 = ElementDraw(n5, n6, area, inercia, young)
        e7 = ElementDraw(n5, n7, area, inercia, young)
        e8 = ElementDraw(n6, n8, area, inercia, young)
        e9 = ElementDraw(n7, n8, area, inercia, young)
        nodes = [n1, n2, n3, n4, n5, n6, n7, n8]
        elements = [e1, e2, e3, e4, e5, e6, e7, e8, e9]

        for node in nodes:
            self.drawNode(node)
        for element in elements:
            self.drawElement(element)

    def balanco(self):
        n1 = NodeDraw(0, 0)
        n2 = NodeDraw(100, 0)
        n1.setSupport(Support.fixed)
        n2.setNodalForce(NodalForce(0, 10, 0))
        e1 = ElementDraw(n1, n2, 1, 1, 1)
        nodes = [n1, n2]
        elements = [e1]
        for node in nodes:
            self.drawNode(node)
        for element in elements:
            self.drawElement(element)

    def porticosSucessivos(self):
        nodes = []
        elements = []

        rec = Rectangle(0.012, 0.001)
        area = rec.area
        inercia = rec.inertia

        n1 = NodeDraw(0, 0)
        n1.setSupport(Apoio.terceiro_genero)
        n2 = NodeDraw(0, 10)
        n3 = NodeDraw(10, 10)
        n4 = NodeDraw(10, 0)
        n4.setSupport(Apoio.terceiro_genero)

        e1 = ElementDraw(n1, n2, area, inercia, 1)
        e2 = ElementDraw(n2, n3, area, inercia, 1)
        e3 = ElementDraw(n3, n4, area, inercia, 1)

        nodes.append(n1)
        nodes.append(n2)
        nodes.append(n3)
        nodes.append(n4)

        elements.append(e1)
        elements.append(e2)
        elements.append(e3)

        for i in range(2, 100, 1):
            n2, n3 = NodeDraw(0, -i*10), NodeDraw(1*10, -i*10)

            e1 = ElementDraw(nodes[len(nodes)-4], n2, area, inercia, 1)
            e2 = ElementDraw(n2, n3, area, inercia, 1)
            e3 = ElementDraw(n3, nodes[len(nodes)-1], area, inercia, 1)

            nodes.append(n2)
            nodes.append(n3)
            elements.append(e1)
            elements.append(e2)
            elements.append(e3)

        nodes[len(nodes)-2].setNodalForce(NodalForce(100, 0, 0))

        for node in nodes:
            self.drawNode(node)
        for element in elements:
            self.drawElement(element)

    def modelotcc(self):

        secao = Rectangle(0.20, 0.40)
        area = secao.area
        inercia = secao.inertia
        young = 25e9

        n1 = NodeDraw(0, -0)
        n2 = NodeDraw(400, -0)
        n3 = NodeDraw(0, -150)
        n4 = NodeDraw(100, -150)
        n5 = NodeDraw(300, -150)
        n6 = NodeDraw(400, -150)
        n7 = NodeDraw(0, -300)
        n8 = NodeDraw(400, -300)

        print(n2.x, n2.y, n2.getItem().x(), n2.getItem().y())

        n1.setSupport(Apoio.terceiro_genero)
        n2.setSupport(Apoio.terceiro_genero)
        n7.setSupport(Apoio.terceiro_genero)
        n8.setSupport(Apoio.terceiro_genero)

        n3.setP(1)
        n6.setP(1)

        n4.setNodalForce(NodalForce(-100e3, 0, 0))
        n5.setNodalForce(NodalForce(-100e3, 0, 0))

        e1 = ElementDraw(n1, n3, area, inercia, young)
        e2 = ElementDraw(n3, n4, area, inercia, young)
        e3 = ElementDraw(n4, n5, area, inercia, young)
        e4 = ElementDraw(n5, n6, area, inercia, young)
        e5 = ElementDraw(n2, n6, area, inercia, young)
        e6 = ElementDraw(n3, n7, area, inercia, young)
        e7 = ElementDraw(n6, n8, area, inercia, young)

        nodes = [n1, n2, n3, n4, n5, n6, n7, n8]
        elements = [e1, e2, e3, e4, e5, e6, e7]

        for node in nodes:
            self.drawNode(node)
        for element in elements:
            self.drawElement(element)


'''
    ###############################################
        Funções Desabilitadas momentaneamente
    ###############################################

    def showDrawForm(self):
        drawForm = FormDraw()
        drawForm.setCanvas(self.canvas)
        drawForm.fillNodeListStructure()
        drawForm.fillElementListStructure()
        drawForm.setGraphicsScene(self.graphicsScene)
        drawForm.show()
        drawForm.exec()

    def showResultsForm(self):
        resultsForm = QtWidgets.QDialog()
        ui = Ui_ResultForm()
        ui.setupUi(resultsForm)
        resultsForm.show()
        resultsForm.exec()

    def mousePressEventScene(self, event: QGraphicsSceneMouseEvent):
        if Qt.MouseButton.LeftButton == event.button():
            x = event.scenePos().x()
            y = event.scenePos().y()
            self.lineEditXCanvas.setText(str(x))
            self.lineEditYCanvas.setText(str(y))
            if self.verifySuportChecked() is not None:
                self.drawSupport(x, y)

            if self.elementClass.isChecked():
                self.drawElement(x, y)
            else:
                self.elementPoint1 = None
                self.elementPoint2 = None
            if self.nodalForces.isChecked():
                self.drawNodalForce(event.scenePos(), 90)

        if Qt.MouseButton.MiddleButton == event.button():
            print("MiddleButtonClick não implementado!")


    def mouseMoveEventScene(self, event: QGraphicsSceneMouseEvent):
        x = event.pos().x()
        y = event.pos().y()
        self.lineEditXCanvas.setText(str(x))
        self.lineEditYCanvas.setText(str(y))
        self.update()

    def drawSupport(self, x: float, y: float):
        pixMap = QPixmap(self.imageReturn())
        imagem = self.graphicsScene.addPixmap(pixMap)
        point = None
        if self.canvas.grid.isActive:
            xString = int(str(x)[:-2])
            yString = int(str(y)[:-2])
            # print(xString, yString)
            if xString % 10 < 5:
                xString = xString - xString % 10
            else:
                xString = xString + (10-xString % 10)

            if yString % 10 < 5:
                yString = yString - yString % 10
            else:
                yString = yString + (10-yString % 10)
            point = QPointF(float(xString), float(yString))
        else:
            pointToDraw = QPointF(x - self.correcaoClickImage()[0], y - self.correcaoClickImage()[1])
            point = QPointF(x, y)
            imagem.setPos(pointToDraw)
            node = Node(point.x(), point.y())
            node.apoio = self.verifySuportChecked()
            self.canvas.nodes.append(node)
            self.canvas.drawnNodes.append(imagem)
        # Seta o item(imagem) desenhado para movimentar
        imagem.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

    def drawNodalForce(self, pos: QPointF, ang: int):
        value = 5
        brush = QBrush(Qt.GlobalColor.black, Qt.BrushStyle.SolidPattern)
        pen = QPen(Qt.GlobalColor.black, 2)

        if ang == 0 or ang == 360:
            x1 = pos.x() + value
            y1 = pos.y() + value * 2
            x2 = pos.x() + value
            y2 = pos.y() - value * 2
            xline = pos.x() + value * 6
            yline = pos.y()
        elif ang == 90:
            x1 = pos.x() - value
            y1 = pos.y() - value * 2
            x2 = pos.x() + value
            y2 = pos.y() - value * 2
            xline = pos.x()
            yline = pos.y() - value * 6
        elif ang == 180:
            x1 = pos.x() - value
            y1 = pos.y() - value * 2
            x2 = pos.x() - value
            y2 = pos.y() + value * 2
            xline = pos.x() - value * 6
            yline = pos.y()
        elif ang == 270:
            x1 = pos.x() + value
            y1 = pos.y() + value * 2
            x2 = pos.x() - value
            y2 = pos.y() + value * 2
            xline = pos.x()
            yline = pos.y() + value * 6
        point1 = pos
        point2 = QPointF(x1, y1)
        point3 = QPointF(x2, y2)
        triangle = QPolygonF([point1, point2, point3])

        try:
            self.graphicsScene.addPolygon(triangle, pen, brush)
            self.graphicsScene.addLine(pos.x(), pos.y(), xline, yline, pen)
        except:
            pass

    def verifySuportChecked(self) -> Apoio:
        apoio = None
        if self.first_class_support.isChecked():
            apoio = Apoio.primeiro_genero
        if self.second_class_support.isChecked():
            apoio = Apoio.segundo_genero
        if self.tird_class_support.isChecked():
            apoio = Apoio.terceiro_genero
        if self.semi_rigid_class_support.isChecked():
            apoio = Apoio.semi_rigido
        return apoio

    def imageReturn(self) -> str:
        apoio = self.verifySuportChecked()
        imagem = None
        if apoio == Apoio.primeiro_genero:
            imagem = "icons/apoio_primeiro_genero.png"
        elif apoio == Apoio.segundo_genero:
            imagem = "icons/apoio_segundo_genero.png"
        elif apoio == Apoio.terceiro_genero:
            imagem = "icons/apoio_terceiro_genero.png"
        elif apoio == Apoio.semi_rigido:
            imagem = "icons/apoio_semi_rigido.png"
        return imagem

    def correcaoClickImage(self) -> list:
        apoio = self.verifySuportChecked()
        correcaoClickImagem = []
        if apoio == Apoio.primeiro_genero:
            correcaoClickImagem = [16, 5]
        elif apoio == Apoio.segundo_genero:
            correcaoClickImagem = [17, 7]
        elif apoio == Apoio.terceiro_genero:
            correcaoClickImagem = [17, 14]
        elif apoio == Apoio.semi_rigido:
            correcaoClickImagem = [15, 12]
        return correcaoClickImagem

    def drawElement(self, x: float, y: float) -> None:
        # print(x, y)
        if self.elementPoint1 == None:
            self.elementPoint1 = QPointF(x, y)
            # print('p1 setado')
        else:
            self.elementPoint2 = QPointF(x, y)
            # print('p2 setado')
        teste1 = self.elementPoint1 is not None
        teste2 = self.elementPoint2 is not None
        if teste1 and teste2:
            p1 = self.elementPoint1
            p2 = self.elementPoint2
            node1 = Node(p1.x(), p1.y())
            node2 = Node(p2.x(), p2.y())
            element = Element(node1, node2, 1, 1, 1)
            pen = QPen(Qt.GlobalColor.black, 2)
            brush = QBrush(Qt.GlobalColor.gray, Qt.BrushStyle.SolidPattern)
            line = self.graphicsScene.addLine(p1.x(), p1.y(), p2.x(), p2.y(), pen)
            dnd1 = self.graphicsScene.addEllipse(p1.x(), p1.y(), 9, 9, pen, brush)
            dnd2 = self.graphicsScene.addEllipse(p2.x(), p2.y(), 9, 9, pen, brush)
            self.canvas.elements.append(element)
            self.canvas.drawnElements.append(line)
            self.elementPoint1 = None
            self.elementPoint2 = None

    def primeiro_genero(self):
        if self.first_class_support.isChecked():
            if self.semi_rigid_class_support.isChecked():
                self.semi_rigid_class_support.toggle()
            elif self.second_class_support.isChecked():
                self.second_class_support.toggle()
            elif self.tird_class_support.isChecked():
                self.tird_class_support.toggle()

    def segundo_genero(self):
        if self.second_class_support.isChecked():
            if self.first_class_support.isChecked():
                self.first_class_support.toggle()
            elif self.tird_class_support.isChecked():
                self.tird_class_support.toggle()
            elif self.semi_rigid_class_support.isChecked():
                self.semi_rigid_class_support.toggle()

    def terceiro_genero(self):
        if self.tird_class_support.isChecked():
            if self.first_class_support.isChecked():
                self.first_class_support.toggle()
            elif self.second_class_support.isChecked():
                self.second_class_support.toggle()
            elif self.semi_rigid_class_support.isChecked():
                self.semi_rigid_class_support.toggle()

    def semi_rigido(self):
        if self.semi_rigid_class_support.isChecked():
            if self.first_class_support.isChecked():
                self.first_class_support.toggle()
            elif self.second_class_support.isChecked():
                self.second_class_support.toggle()
            elif self.tird_class_support.isChecked():
                self.tird_class_support.toggle()

    def elementClassToggle(self):
        apoio = self.verifySuportChecked()
        if not self.elementClass.isChecked():
            if self.semi_rigid_class_support.isChecked():
                self.semi_rigid_class_support.toggle()
            elif self.first_class_support.isChecked():
                self.first_class_support.toggle()
            elif self.second_class_support.isChecked():
                self.second_class_support.toggle()
            elif self.tird_class_support.isChecked():
                self.tird_class_support.toggle()
            elif self.semi_rigid_class_support.isChecked():
                self.semi_rigid_class_support.toggle()

    # def disableButton(self, button: QtWidgets.QAction):
    #     first =
    #     second
    #     tird
    #     rigid
    #     element

    def activateGrid(self):
        if self.checkBoxGrid.isChecked():
            self.lineEditXGrid.setEnabled(True)
            self.lineEditYGrid.setEnabled(True)
            self.checkBoxGridSnap.setEnabled(True)
            self.drawGrid()
        else:
            self.lineEditXGrid.setEnabled(False)
            self.lineEditXGrid.setText("")
            self.lineEditYGrid.setEnabled(False)
            self.lineEditYGrid.setText("")
            self.checkBoxGridSnap.setEnabled(False)
            self.removeGrid()

    def drawGrid(self):
        self.canvas.grid.isActive = True
        xLength = int(self.graphicsViewCanvas.size().width()/20)
        yLength = int(self.graphicsViewCanvas.size().height()/20)
        for i in range(-xLength, xLength, 1):
            for j in range(-yLength, yLength, 1):
                self.canvas.grid.points.append(self.graphicsScene.addEllipse(i*10, j * 10, 1, 1, QPen(Qt.GlobalColor.black)))
        # self.canvas.grid.points.append(self.graphicsScene.addEllipse(
        #     0, 0, 1, 1, QtGui.QPen(QtCore.Qt.GlobalColor.black)))

    def removeGrid(self):
        for point in self.canvas.grid.points:
            self.graphicsScene.removeItem(point)
        self.canvas.grid.points = []
        self.canvas.grid.isActive = False

    def actionProcessClicked(self):
        print('Execução dos cálculos não implementado!')
        if self.dockWidgetResults.isHidden():
            self.dockWidgetResults.show()
        else:
            self.dockWidgetResults.hide()
'''
