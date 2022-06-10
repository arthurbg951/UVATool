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


class FormTableResults(QWidget):

    def __init__(self, process: Process) -> None:
        super().__init__()
        hbox = QVBoxLayout()
        equilibrium = process.getEquilibriumMatrix()
        equilibriumTable = QTableWidget(equilibrium.shape[0], equilibrium.shape[1])
        try:
            for i in range(equilibrium.shape[0]):
                for j in range(equilibrium.shape[1]):
                    content = QTableWidgetItem(str(equilibrium[i, j]))
                    equilibriumTable.setItem(i, j, content)
            equilibriumTable.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.warning(self, "Warning", str(e))
        # frameStiffness = process.getFrameStiffness()
        # frameStiffnessTable = QTableWidget(frameStiffness.shape[0], frameStiffness.shape[1])
        # try:
        #     for i in range(frameStiffness.shape[0]):
        #         for j in range(frameStiffness.shape[1]):
        #             content = QTableWidgetItem(str(frameStiffness[i, j]))
        #             frameStiffnessTable.setItem(i, j, content)
        #     frameStiffnessTable.resizeColumnsToContents()
        # except Exception as e:
        #     QMessageBox.warning(self, "Warning", str(e))

        hbox.addWidget(equilibriumTable)
        # hbox.addWidget(frameStiffnessTable)
        self.setLayout(hbox)
        self.resize(equilibriumTable.width(), equilibriumTable.height())
        super().showMaximized()
