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
    QHBoxLayout,
    QTableView,
    QMessageBox
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
from PyQt5 import uic
from libs.UVATool import *
from libs.Drawing import *


class FormTableResults(QMainWindow):
    calc: Process

    def __init__(self, parent) -> None:
        super().__init__(parent)

        hbox = QHBoxLayout()
        table = QTableView()

        try:
            table.setLineWidth(equilibrium.shape[0])
            equilibrium = self.calc.getEquilibriumMatrix()
        except:
            raise Exception("Equilibrium Matrix not Defined")

        hbox.addWidget(table)
        self.setLayout(hbox)

    def setProcess(self, process: Process):
        self.calc = process
