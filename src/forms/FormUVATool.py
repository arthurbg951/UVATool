from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QMainWindow,
    QAction,
    QGraphicsScene,
    QGraphicsSceneMouseEvent,
    QDialog,
    QToolBar,
)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPixmap, QPen, QPolygonF, QBrush
from PyQt5 import uic
from libs.UVATool import *
from libs.Drawings import *
from forms.FormDraw import FormDraw


class FormUVATool(QMainWindow):

    first_class_support: QAction
    second_class_support: QAction
    tird_class_support: QAction
    semi_rigid_class_support: QAction
    elementClass: QAction
    separator: QAction
    actionDraw: QAction
    actionProcess: QAction

    actionNew: QAction
    actionOpen: QAction
    actionSave: QAction
    actionExport: QAction
    actionExt: QAction

    toolBarLoadings: QToolBar
    nodalForces: QAction

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/FormUVATool.ui", self)

        self.dockWidgetResults.hide()
        self.lineEditSuportAngulation.setEnabled(False)
        self.first_class_support.triggered.connect(self.primeiro_genero)
        self.second_class_support.triggered.connect(self.segundo_genero)
        self.tird_class_support.triggered.connect(self.terceiro_genero)
        self.semi_rigid_class_support.triggered.connect(self.semi_rigido)
        self.elementClass.triggered.connect(self.elementClassToggle)
        self.checkBoxGrid.clicked.connect(self.activateGrid)
        self.actionProcess.triggered.connect(self.actionProcessClicked)

        self.actionDraw.triggered.connect(self.showDrawForm)

        self.canvas = Canvas()
        self.defaults = Defaults()
        self.elementPoint1 = None
        self.elementPoint2 = None

        self.comboBoxResultOptions.addItem("Nodes")
        self.comboBoxResultOptions.addItem("Elements")

        self.graphicsScene = QGraphicsScene()
        self.graphicsScene.mousePressEvent = self.mousePressEventScene
        self.graphicsScene.setSceneRect(0, 0, 1,  1)
        self.graphicsScene.mousePressEvent = self.mousePressEventScene
        self.graphicsViewCanvas.setScene(self.graphicsScene)

    def showDrawForm(self):
        drawForm = FormDraw()
        drawForm.setCanvas(self.canvas)
        drawForm.fillNodeListStructure()
        drawForm.fillElementListStructure()
        drawForm.setGraphicsScene(self.graphicsScene)
        drawForm.show()
        drawForm.exec()

    # def showResultsForm(self):
    #     resultsForm = QtWidgets.QDialog()
    #     ui = Ui_ResultForm()
    #     ui.setupUi(resultsForm)
    #     resultsForm.show()
    #     resultsForm.exec()

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
        # imagem.setFlag(
        #  QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

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
            line = self.graphicsScene.addLine(
                p1.x(), p1.y(), p2.x(), p2.y(), QPen(Qt.GlobalColor.black, 2))
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
        if apoio == None:
            self.tird_class_support.toggle()
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
