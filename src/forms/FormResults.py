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


class FormResults(QDialog):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("ui/FormResults.ui", self)
