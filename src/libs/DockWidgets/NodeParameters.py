from PyQt5.QtWidgets import (
    QDockWidget,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QWidget,
    QSpacerItem,
    QSizePolicy,
    QGraphicsScene,
    QMessageBox
)

from PyQt5.QtCore import Qt
from libs.Drawing import *


class NodeParameters(QDockWidget):
    scene: QGraphicsScene

    Coordinates: QGroupBox
    hbox: QHBoxLayout
    xLabel: QLabel
    xInput: QLineEdit
    hbox2: QHBoxLayout
    yLabel: QLabel
    yInput: QLineEdit

    StifnessCoefficient: QGroupBox
    hbox3: QHBoxLayout
    pCoeff: QLabel
    pInput: QLineEdit

    CreateNode: QPushButton

    def __init__(self, scene: QGraphicsScene) -> None:
        super().__init__()
        self.scene = scene
        # QDockWidget - QDockWidget #
        self.setWindowTitle("Node")
        self.setFeatures(self.DockWidgetFeature.DockWidgetClosable)

        # QGroupBox - Coordinates #
        self.Coordinates = QGroupBox("Coordinates", self)

        self.xLabel = QLabel("X", self)
        self.yLabel = QLabel("Y", self)
        self.xInput = QLineEdit(self)
        self.xInput.setPlaceholderText(str("0.00"))
        self.xInput.textEdited.connect(lambda arg, text=None: self.checkInputData(self.xInput))
        self.yInput = QLineEdit(self)
        self.yInput.setPlaceholderText(str("0.00"))
        self.yInput.textEdited.connect(lambda arg, text=None: self.checkInputData(self.yInput))

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.xLabel)
        self.hbox.addWidget(self.xInput)

        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.yLabel)
        self.hbox2.addWidget(self.yInput)

        grid = QGridLayout(self.Coordinates)
        grid.addLayout(self.hbox, 1, 1)
        grid.addLayout(self.hbox2, 2, 1)

        # QGroupBox - Stiffness Coefficient #
        self.StifnessCoefficient = QGroupBox("Stiffness Coefficient", self)

        self.pCoeff = QLabel("P", self)
        self.pInput = QLineEdit(self)
        self.pInput.setPlaceholderText("1")
        self.pInput.textEdited.connect(lambda arg, text=None: self.checkInputData(self.pInput))

        self.hbox3 = QHBoxLayout(self.StifnessCoefficient)
        self.hbox3.addWidget(self.pCoeff)
        self.hbox3.addWidget(self.pInput)

        # QPushButton - CreateNode #
        self.CreateNode = QPushButton("Ok", self)
        self.CreateNode.clicked.connect(self.CreateNodeClicked)

        # QSpacerItem - ESPAÇO EM BRANCO #
        self.Space = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        outGrid = QGridLayout()
        outWidget = QWidget(self)
        outWidget.setLayout(outGrid)
        outGrid.addWidget(self.Coordinates, 1, 1)
        outGrid.addWidget(self.StifnessCoefficient, 2, 1)
        outGrid.addWidget(self.CreateNode, 3, 1)
        outGrid.addItem(self.Space, 4, 1)

        self.setWidget(outWidget)

    def checkInputData(self, input: QLineEdit) -> None:
        # VERIFICA SE A ENTRADA DO INPUT ESTÁ CORRETA (se é numero)
        if not self.checkIsNumber(input.text()):
            if len(input.text()) > 0:
                if input.text()[0] != "-":
                    input.setText(input.text()[0:len(input.text()) - 1])

    def checkIsNumber(self, string: str):
        try:
            float(string)
            return True
        except:
            return False

    def CreateNodeClicked(self):
        if self.xInput.text() == "":
            x = float(self.xInput.placeholderText())
        else:
            x = float(self.xInput.text())
        if self.yInput.text() == "":
            y = float(self.yInput.placeholderText())
        else:
            y = float(self.yInput.text())

        node = self.scene.verifyExistingNode(x, y)
        if node == None:
            try:
                nd = NodeDraw(x, y)
                if self.pInput.text() == "":
                    nd.setP(float(self.pInput.placeholderText()))
                else:
                    nd.setP(float(self.pInput.text()))
                self.scene.drawNode(nd)
            except Exception as e:
                QMessageBox.warning(self, "Warning", str(e))
        else:
            QMessageBox.warning(self, "Warning", f"Already exist a nothe in this place.\nPoint=({x}, {y})")
