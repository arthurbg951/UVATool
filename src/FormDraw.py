from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QDialog,
    QAction,
    QGraphicsScene,
    QGraphicsSceneMouseEvent
)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPixmap, QPen
from PyQt5 import uic
from libs.UVATool import *
from libs.Drawings import *


class FormDraw(QDialog):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("FormDraw.ui", self)

        self.canvas = Canvas()
        self.graphicsScene = QGraphicsScene()
        self.lineEditNodeRotation.setEnabled(False)
        self.lineEditNodeRotation_2.setEnabled(False)
        self.listViewNodeStructure.clicked.connect(
            self.listViewNodeStructureClicked)
        self.listViewNodeStructure.doubleClicked.connect(
            self.listViewNodeStructureDoubleClicked)
        self.listViewElementStructure.clicked.connect(
            self.listViewElementStructureClicked)
        self.pushButtonNodeDraw.clicked.connect(self.pushButtonNodeDrawClicked)
        self.pushButton_2.clicked.connect(self.pushButtonElementDrawClicked)

    def fillNodeListStructure(self):
        if self.canvas is not None:
            # print("Entrei no fill nodes")
            for node in self.canvas.nodes:
                item = "{0}, {1}".format(
                    str(node).split(",")[0], str(node).split(",")[1])
                self.listViewNodeStructure.addItem(item)
        else:
            print('nodes:CANVAS NÃO INSERIDO CORRETAMENTE PELO UVATOOL')

    def fillElementListStructure(self):
        if self.canvas is not None:
            # print("Entrei no fill elements")
            for element in self.canvas.elements:
                item = "{0}; {1}".format(
                    str(element).split(";")[0], str(element).split(";")[1])
                self.listViewElementStructure.addItem(item)
        else:
            print('elements:CANVAS NÃO INSERIDO CORRETAMENTE PELO UVATOOL')

    def setCanvas(self, canvas: Canvas):
        self.canvas = canvas

    def setGraphicsScene(self, scene: QGraphicsScene):
        self.graphicsScene = scene

    def listViewNodeStructureClicked(self):
        node = self.listViewNodeStructure.currentItem()
        nodeText = node.text().replace(" ", "")
        xCoord = nodeText.split(",")[0]
        yCoord = nodeText.split(",")[1]
        listPos = self.listViewNodeStructure.indexFromItem(node).row()
        apoio = self.canvas.nodes[listPos].apoio
        self.lineEditNodeX.setText(xCoord)
        self.lineEditNodeY.setText(yCoord)
        if apoio == Apoio.primeiro_genero:
            self.radioButtonFirstClass.setChecked(True)
        elif apoio == Apoio.segundo_genero:
            self.radioButtonSecondClass.setChecked(True)
        elif apoio == Apoio.terceiro_genero:
            self.radioButtonTirdClass.setChecked(True)
        elif apoio == Apoio.semi_rigido:
            self.radioButtonSemiRigidClass.setChecked(True)
        self.pushButtonNodeDraw.setText("Edit")
        # Teste de implementação para trocar cor dos icones quando estão selecionados
        # nodeTest = Node(float(xCoord)-self.correcaoClickImage()
        #                 [0], float(yCoord)-self.correcaoClickImage()[1])
        # for node in self.canvas.drawnElements:
        #     if node == nodeTest:
        #         self.graphicsScene.removeItem(node)
        #         mask = node.createMaskFromColor(
        #             QtGui.QColor('black'), QtCore.Qt.MaskOutColor)
        #         node.fill((QtGui.QColor('red')))
        #         node.setMask(mask)
        #         self.graphicsScene.addPixmap(node)

    def listViewNodeStructureDoubleClicked(self):
        node = self.listViewNodeStructure.currentItem()
        nodeText = node.text().replace(" ", "")
        xCoord = nodeText.split(",")[0]
        yCoord = nodeText.split(",")[1]
        # Acho q não precisa disso.. Verificar as possibilidades
        # listPos = self.listViewNodeStructure.indexFromItem(node).row()
        # apoio = self.canvas.nodes[listPos].apoio
        # node = Node(xCoord, yCoord)
        # node.apoio = apoio
        # print(node)
        # self.verifyElementTexts()

        fistX = self.lineEditFistNodeX.text()
        fistY = self.lineEditFistNodeY.text()
        secondX = self.lineEditSecondNodeX.text()
        secondY = self.lineEditSecondNodeY.text()

        if fistX == "" and fistY == "":
            self.lineEditFistNodeX.setText(xCoord)
            self.lineEditFistNodeY.setText(yCoord)
        elif secondX == "" and secondY == "":
            self.lineEditSecondNodeX.setText(xCoord)
            self.lineEditSecondNodeY.setText(yCoord)

    def listViewElementStructureClicked(self):
        structure = self.listViewElementStructure.currentItem()
        structureText = structure.text().replace(
            "Node1=", "").replace("Node2=", "").replace(" ", "")
        node1X = float(structureText.split(";")[0].split(",")[0])
        node1Y = float(structureText.split(";")[0].split(",")[1])
        node2X = float(structureText.split(";")[1].split(",")[0])
        node2Y = float(structureText.split(";")[1].split(",")[1])
        self.lineEditFistNodeX.setText(str(node1X))
        self.lineEditFistNodeY.setText(str(node1Y))
        self.lineEditSecondNodeX.setText(str(node2X))
        self.lineEditSecondNodeY.setText(str(node2Y))
        node1 = Node(node1X, node1Y)
        node2 = Node(node2X, node2Y)
        element = Element(node1, node2)
        self.pushButton_2.setText("Edit")

    def verifyNodeTexts(self):
        try:
            float(self.lineEditNodeX.text())
            float(self.lineEditNodeY.text())
            # Descomentar quando for implementar rotação
            # float(self.lineEditNodeRotation.text())
        except:
            raise RuntimeError(
                "Os textos dos nodes foram escritos de forma errada!")

    def verifyElementTexts(self):
        try:
            t1 = self.lineEditFistNodeX.text()
            if t1 != "":
                float(t1)
            t2 = self.lineEditFistNodeY.text()
            if t2 != "":
                float(t2)
            t3 = self.lineEditSecondNodeX.text()
            if t3 != "":
                float(t3)
            t4 = self.lineEditSecondNodeY.text()
            if t4 != "":
                float(t4)
        except:
            raise RuntimeError(
                "Os textos do elemento foram escritos de forma errada!")

    def verifySuportChecked(self) -> Apoio:
        apoio = None
        if self.radioButtonFirstClass.isChecked():
            apoio = Apoio.primeiroGenero
        elif self.radioButtonSecondClass.isChecked():
            apoio = Apoio.segundo_genero
        elif self.radioButtonTirdClass.isChecked():
            apoio = Apoio.terceiroGenero
        elif self.radioButtonSemiRigidClass.isChecked():
            apoio = Apoio.semiRigido
        return apoio

    def imageReturn(self) -> str:
        apoio = self.verifySuportChecked()
        imagem = None
        if apoio == Apoio.primeiroGenero:
            imagem = "icons/apoio_primeiro_genero.png"
        elif apoio == Apoio.segundo_genero:
            imagem = "icons/apoio_segundo_genero.png"
        elif apoio == Apoio.terceiroGenero:
            imagem = "icons/apoio_terceiro_genero.png"
        elif apoio == Apoio.semiRigido:
            imagem = "icons/apoio_semi_rigido.png"
        return imagem

    def correcaoClickImage(self):
        apoio = self.verifySuportChecked()
        correcaoClickImagem = []
        if apoio == Apoio.primeiroGenero:
            correcaoClickImagem = [16, 5]
        elif apoio == Apoio.segundo_genero:
            correcaoClickImagem = [17, 7]
        elif apoio == Apoio.terceiroGenero:
            correcaoClickImagem = [17, 14]
        elif apoio == Apoio.semiRigido:
            correcaoClickImagem = [15, 12]
        return correcaoClickImagem

    def pushButtonNodeDrawClicked(self):
        self.verifyNodeTexts()
        x = float(self.lineEditNodeX.text())
        y = float(self.lineEditNodeY.text())
        self.pushButtonNodeDraw.setText("Draw")
        self.lineEditNodeX.setText("")
        self.lineEditNodeY.setText("")
        self.lineEditNodeRotation.setText("")
        node = Node(x, y)
        node.apoio = self.verifySuportChecked()
        self.drawSupport(node)
        item = "{0}, {1}".format(
            str(node).split(",")[0], str(node).split(",")[1])
        self.listViewNodeStructure.addItem(item)

    def pushButtonElementDrawClicked(self):
        self.verifyElementTexts()
        fistX = float(self.lineEditFistNodeX.text())
        fistY = float(self.lineEditFistNodeY.text())
        secondX = float(self.lineEditSecondNodeX.text())
        secondY = float(self.lineEditSecondNodeY.text())
        self.lineEditFistNodeX.setText("")
        self.lineEditFistNodeY.setText("")
        self.lineEditSecondNodeX.setText("")
        self.lineEditSecondNodeY.setText("")
        node1 = Node(fistX, fistY)
        node2 = Node(secondX, secondY)
        element = Element(node1, node2)
        self.drawElement(node1, node2)
        item = "{0}; {1}".format(
            str(element).split(";")[0], str(element).split(";")[1])
        self.listViewElementStructure.addItem(item)

    def drawSupport(self, node: Node):
        if node.apoio == None:
            raise RuntimeError("node não possui apoio para desenhar")
        imagem = self.imageReturn()
        if imagem == None or imagem == "":
            raise RuntimeError("node não possui imagem para desenhar")
        pixMap = QPixmap(imagem)
        imagem = self.graphicsScene.addPixmap(pixMap)
        point = None
        point = QPointF(
            node.x - self.correcaoClickImage()[0], node.y - self.correcaoClickImage()[1])
        imagem.setPos(point)
        self.canvas.nodes.append(node)
        self.canvas.drawnNodes.append(imagem)

    def drawElement(self, node1: Node, node2: Node) -> None:
        test1 = False
        test2 = False
        for node in self.canvas.nodes:
            if node == node1:
                test1 = True
            if node == node2:
                test2 = True
        if test1 and test2:
            element = Element(node1, node2)
            line = self.graphicsScene.addLine(
                node1.x, node1.y, node2.x, node2.y, QPen(Qt.GlobalColor.black, 2))
            self.canvas.elements.append(element)
            self.canvas.drawnElements.append(line)
        else:
            raise RuntimeError(
                'Os nodes selecionados para desenhar não foram inseridos no canvas corretamente!')
