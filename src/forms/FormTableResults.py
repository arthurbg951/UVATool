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
    process: Process

    def __init__(self) -> None:
        super().__init__()

    def show(self) -> None:
        hbox = QVBoxLayout()
        equilibrium = self.process.getEquilibriumMatrix()
        table = QTableWidget(equilibrium.shape[0], equilibrium.shape[1])
        try:
            for i in range(equilibrium.shape[0]):
                for j in range(equilibrium.shape[1]):
                    content = QTableWidgetItem(str(equilibrium[i, j]))
                    table.setItem(i, j, content)
            table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.warning(self, "Warning", str(e))
        hbox.addWidget(table)
        self.setLayout(hbox)
        self.resize(table.size())
        super().show()

    def setProcess(self, process):
        self.process = process
