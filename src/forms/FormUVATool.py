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
    QFileDialog
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
from UVATool.Colors import to_red
from UVATool.Enums import *
from UVATool.Exceptions import *
from libs.Drawing import *
from libs.DockWidgets.CreateNode import CreateNode
from libs.DockWidgets.Browser import Browser
from libs.UVAGraphicsScene import UVAGraphicsScene
from forms.FormTableResults import FormTableResults
import traceback
from time import sleep
import os


class FormUVATool(QMainWindow):

    GraphicsView: QGraphicsView
    scene: UVAGraphicsScene

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

    actionStructureFile_py: QAction

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
        self.actionStructureFile_py.triggered.connect(self.loadStructureFile)

        self.p.textChanged.connect(self.pValueChanged)

        self.ChangeValues.visibilityChanged.connect(self.ChangeValuesClose)

        # self.GraphicsView.DragMode(1)

        self.calc = None
        self.totalScale: float = 1

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
                print(to_red(traceback.format_exc()))

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
            analise = Analise.viaMinimaNormaEuclidiana
            print("         Via Mínima Norma Euclidiana          ")

        else:
            analise = Analise.viaRigidezAnalitica
            print("            Via Rigidez Analítica             ")

        print("----------------------------------------------")
        has_error = False
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
            has_error = True
            QMessageBox.warning(self, "Warning", str(e))
            print(to_red(traceback.format_exc()))

        print("----------------------------------------------")
        print()
        if not has_error:
            QMessageBox.warning(self, "Success", "A solution was founded.")

    def showTableReultsForm(self):
        try:
            self.formTableResults = FormTableResults(self.calc)
            self.formTableResults.showMaximized()
        except Exception as e:
            QMessageBox.warning(self, "Form Table Results Error", str(e))
            print(to_red(traceback.format_exc()))

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

    def loadStructureFile(self) -> None:
        file_filter = 'Python File (*.py)'
        response = QFileDialog.getOpenFileName(parent=self, caption='Select a python file with a StructureFile defined',
                                               directory=f"{os.getcwd()}/exemples", filter=file_filter, initialFilter=file_filter)
        file_name = response[0]
        print(f"File loaded {file_name}")
        try:
            if file_name != "":
                file = StructureFile(file_name, verbose=True)
                # ONLY GET THE FRIST STRUCTURE IN THE FILE
                structure = file.getStructure()[0]
                if len(file.getStructure()) > 1:
                    raise Exception("This file contains multiple structures.\nTry another file or edit source code.")
                self.scene.loadStructure(structure)
                self.update()
        except Exception as e:
            msg = ("Ocurred an error whyle trying to load the StructureFile.\n" + "Skipping the load.\n" + "Verify terminal for more informations\n" + "Error: " + str(e))
            QMessageBox.warning(self, "Warning", msg)
            print(to_red(traceback.format_exc()))

    def update(self) -> None:
        super().update()
        # UPDATE STRUCTURE LIST
        self.browser.updateStructureList()
