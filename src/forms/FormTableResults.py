from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMainWindow,
    QMessageBox,
    QDialog
)
from PyQt5.QtCore import (
    Qt,
    QPointF,
    QLineF,
    QEvent
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
    QWheelEvent
)
from libs.UVATool import *
from PyQt5 import uic


class FormTableResults(QWidget):
    equilibriumTable: QTableWidget
    frameStiffnessTable: QTableWidget
    globalFrameStiffnessTable: QTableWidget
    nodalForcesVector: QTableWidget
    nodalDisplacementVector: QTableWidget
    nodalDeformationsVector: QTableWidget
    InternalForcesVector: QTableWidget

    def __init__(self, process: Process) -> None:
        super().__init__()
        uic.loadUi("ui/FormTableResults.ui", self)
        # super().show()
        super().showMaximized()

        # Equilibrium
        equilibrium = process.getEquilibriumMatrix()
        self.equilibriumTable.setRowCount(equilibrium.shape[0])
        self.equilibriumTable.setColumnCount(equilibrium.shape[1])
        try:
            for i in range(equilibrium.shape[0]):
                for j in range(equilibrium.shape[1]):
                    content = QTableWidgetItem("{0:.2f}".format(equilibrium[i, j]))
                    content.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.equilibriumTable.setItem(i, j, content)
            self.equilibriumTable.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.warning(self, "Equilibrium Warning", str(e))

        # Frame Stiffness
        frameStiffness = process.getFrameStiffness()
        self.frameStiffnessTable.setRowCount(frameStiffness.shape[0])
        self.frameStiffnessTable.setColumnCount(frameStiffness.shape[1])
        try:
            for i in range(frameStiffness.shape[0]):
                for j in range(frameStiffness.shape[1]):
                    content = QTableWidgetItem("{0:.2f}".format(frameStiffness[i, j]))
                    content.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.frameStiffnessTable.setItem(i, j, content)
            self.frameStiffnessTable.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.warning(self, "Frame Stiffness Warning", str(e))

        # Global Frame Stiffness
        globalFrameStiffnessTable = process.getGlobalFrameStiffness()
        self.globalFrameStiffnessTable.setRowCount(globalFrameStiffnessTable.shape[0])
        self.globalFrameStiffnessTable.setColumnCount(globalFrameStiffnessTable.shape[1])
        try:
            for i in range(globalFrameStiffnessTable.shape[0]):
                for j in range(globalFrameStiffnessTable.shape[1]):
                    content = QTableWidgetItem("{0:.2f}".format(globalFrameStiffnessTable[i, j]))
                    content.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.globalFrameStiffnessTable.setItem(i, j, content)
            self.globalFrameStiffnessTable.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.warning(self, "Global Frame Stiffness Warning", str(e))

        # Nodal Forces
        nodalForcesVector = process.getNodalForces()
        self.nodalForcesVector.setRowCount(nodalForcesVector.shape[0])
        self.nodalForcesVector.setColumnCount(1)
        try:
            for i in range(nodalForcesVector.shape[0]):
                content = QTableWidgetItem("{0:.2f}".format(nodalForcesVector[i]))
                content.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.nodalForcesVector.setItem(i, 0, content)
            self.nodalForcesVector.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.warning(self, "Nodal Forces Warning", str(e))

        # Nodal Displacement
        nodalDisplacementVector = process.getNodalDisplacement()
        self.nodalDisplacementVector.setRowCount(nodalDisplacementVector.shape[0])
        self.nodalDisplacementVector.setColumnCount(1)
        try:
            for i in range(nodalDisplacementVector.shape[0]):
                content = QTableWidgetItem("{0:.2f}".format(nodalDisplacementVector[i]))
                content.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.nodalDisplacementVector.setItem(i, 0, content)
            self.nodalDisplacementVector.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.warning(self, "Nodal Displacement Warning", str(e))

        # Nodal Deformations
        nodalDeformationsVector = process.getDeformations()
        self.nodalDeformationsVector.setRowCount(nodalDeformationsVector.shape[0])
        self.nodalDeformationsVector.setColumnCount(1)
        try:
            for i in range(nodalDeformationsVector.shape[0]):
                content = QTableWidgetItem("{0:.2f}".format(nodalDeformationsVector[i]))
                content.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.nodalDeformationsVector.setItem(i, 0, content)
            self.nodalDeformationsVector.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.warning(self, "Nodal Deformations Warning", str(e))

        # Internal Forces
        InternalForcesVector = process.getInternalForces()
        self.InternalForcesVector.setRowCount(InternalForcesVector.shape[0])
        self.InternalForcesVector.setColumnCount(1)
        try:
            for i in range(InternalForcesVector.shape[0]):
                content = QTableWidgetItem("{0:.2f}".format(InternalForcesVector[i]))
                content.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.InternalForcesVector.setItem(i, 0, content)
            self.InternalForcesVector.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.warning(self, "Internal Forces Warning", str(e))

        # self.resize(equilibriumTable.width(), equilibriumTable.height())
