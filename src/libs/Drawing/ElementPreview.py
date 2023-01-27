from PyQt5.QtWidgets import (
    QGraphicsLineItem,

)
from PyQt5.QtCore import (
    Qt,
    QLineF,
)
from PyQt5.QtGui import (
    QPen,
    QColor,
)

class ElementPreview(QGraphicsLineItem):
    def __init__(self, line: QLineF):
        super().__init__(line)
        self.setPen(QPen(QColor(255, 140, 0), 2, Qt.PenStyle.DashLine))