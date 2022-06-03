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
)
from PyQt5.QtCore import (
    Qt,
    QPointF,
    QLineF,
)
from PyQt5.QtGui import (
    QPixmap,
    QPen,
    QPolygonF,
    QBrush,
    QMouseEvent,
    QKeyEvent,
    QColor,
    QShowEvent
)
from PyQt5 import uic
from libs.UVATool import *
from libs.Drawing import *


class FormUVATool(QMainWindow):

    GraphicsView: QGraphicsView

    DrawingsToolBar: QToolBar
    NodeAction: QAction
    ElementAction: QAction

    ToolsToolBar: QToolBar
    ProcessCalculations: QAction

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

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/FormUVATool.ui", self)

        self.scene = UVAGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 1, 1)
        self.GraphicsView.setScene(self.scene)

        self.ChangeValues.close()
        self.ElementParameters.close()

        self.confirmButton.clicked.connect(self.confirmClicked)
        self.confirmButton_2.clicked.connect(self.confirmClicked_2)
        self.ChangeValues.visibilityChanged.connect(self.ChangeValuesClose)
        self.p.textChanged.connect(self.pValueChanged)
        self.ElementAction.toggled.connect(self.ElementActionTogled)
        self.ProcessCalculations.triggered.connect(self.ProcessCalculationsTriggered)

        self.resize(900, 700)
        self.show()

    def confirmClicked(self):
        for item in self.scene.items():
            if isinstance(item, NodeDraw):
                if item.isSelected():
                    fx = float(self.fx.text())
                    fy = float(self.fy.text())
                    m = float(self.m.text())
                    p = float(self.p.text())
                    item.node.setNodalForce(NodalForce(fx, fy, m))
                    item.node.setP(p)
                    if self.primeiroGenero.isChecked():
                        item.node.setSupport(Apoio.primeiro_genero)
                    elif self.segundoGenero.isChecked():
                        item.node.setSupport(Apoio.segundo_genero)
                    elif self.terceiroGenero.isChecked():
                        item.node.setSupport(Apoio.terceiro_genero)
                    elif self.semiRigido.isChecked():
                        item.node.setSupport(Apoio.semi_rigido)
                    elif self.semApoio.isChecked():
                        item.node.setSupport(Apoio.sem_suporte)

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
        if self.p.text() != "":
            self.semiRigido.setChecked(True)

    def ElementActionTogled(self):
        if self.ElementAction.isChecked():
            print('Element Checked')
        else:
            self.scene.isDrawingLine = False
            itemToRemove = None
            for item in self.scene.items():
                if isinstance(item, ElementDraw):
                    if not item.isDrawed:
                        itemToRemove = item
                        break
            self.scene.removeItem(itemToRemove)

    def ProcessCalculationsTriggered(self):

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

            for item in reversed(self.scene.items()):
                if isinstance(item, NodeDraw):
                    nodes.append(item.node)

                if isinstance(item, ElementDraw):
                    elements.append(item.element)
                    # print("Comprimento do elemento: ", item.element.getLength())

            if len(nodes) == 0 and len(elements) == 0:
                raise Exception("Não existe nenhuma estrutura!")

            calc = Process(nodes, elements, analise)
            plot = Print(calc)
            plot.internalForces()
        except Exception as e:
            print(e.args[0])

        print("----------------------------------------------")
        print()


class UVAGraphicsScene(QGraphicsScene):

    def __init__(self, form: FormUVATool):
        super().__init__()
        self.form = form
        self.isDrawingLine = False
        self.keyStack = []

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            if self.form.ElementAction.isChecked():
                node = NodeDraw(event.scenePos().x(), event.scenePos().y())
                if not self.items().__contains__(node):
                    self.addItem(node)
                for item in self.items():
                    if item.hasFocus():
                        if isinstance(item, NodeDraw):
                            node = item
                            break
                if not self.isDrawingLine:
                    p1 = QPointF(node.scenePos().x(), node.scenePos().y())
                    self.isDrawingLine = True
                    self.elementDraw = ElementDraw(QGraphicsLineItem(QLineF(p1, p1)))
                    self.elementDraw.setPen(QPen(QColor(255, 140, 0), 2, Qt.PenStyle.DashLine))
                    self.elementDraw.setNode1(node)
                    self.addItem(self.elementDraw)
                else:
                    self.elementDraw.setPen(QPen(Qt.GlobalColor.gray, 2, Qt.PenStyle.SolidLine))
                    self.elementDraw.setNode2(node)
                    self.elementDraw.isDrawed = True
                    self.isDrawingLine = False
            elif self.form.NodeAction.isChecked():
                self.createNode(event.scenePos().x(), event.scenePos().y())

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if not self.isDrawingLine:
            self.form.semApoio.setChecked(True)
            self.form.fx.setText("")
            self.form.fy.setText("")
            self.form.m.setText("")
            self.form.p.setText("")
            self.form.area.setText("")
            self.form.momentInertia.setText("")
            self.form.youngModulus.setText("")
            for item in self.items():
                if isinstance(item, ElementDraw):
                    if item.hasFocus():
                        item.setSelected(True)
                        self.form.ChangeValues.close()
                        self.form.ElementParameters.show()
                        self.form.area.setText(str(item.element.area))
                        self.form.momentInertia.setText(str(item.element.moment_inertia))
                        self.form.youngModulus.setText(str(item.element.young_modulus))
                    else:
                        item.setSelected(False)
                elif isinstance(item, NodeDraw):
                    if item.hasFocus():
                        self.form.fx.setText(str(item.node.getNodalForce().fx))
                        self.form.fy.setText(str(item.node.getNodalForce().fy))
                        self.form.m.setText(str(item.node.getNodalForce().m))
                        self.form.p.setText(str(item.node.getP()))
                        if item.node.getSupport() == Apoio.primeiro_genero:
                            self.form.primeiroGenero.setChecked(True)
                        elif item.node.getSupport() == Apoio.segundo_genero:
                            self.form.segundoGenero.setChecked(True)
                        elif item.node.getSupport() == Apoio.terceiro_genero:
                            self.form.terceiroGenero.setChecked(True)
                        elif item.node.getSupport() == Apoio.semi_rigido:
                            self.form.semiRigido.setChecked(True)
                        elif item.node.getSupport() == Apoio.sem_suporte:
                            self.form.semApoio.setChecked(True)
                        self.form.ChangeValues.show()
                        self.form.ElementParameters.close()
                        item.setSelected(True)
                    else:
                        item.setSelected(False)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(event)
        if event.buttons() == Qt.MouseButton.NoButton:
            if self.isDrawingLine:
                self.elementDraw.setLine(QLineF(self.elementDraw.line().p1(), event.scenePos()))

    def createNode(self, x: float, y: float):
        node = NodeDraw(x, y)
        self.addItem(node)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # if event.key() == Qt.Key.Key_P:
        #     if len(self.items()) > 0:
        #         print(self.items()[0].shape())

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
