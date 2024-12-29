from PyQt5.QtWidgets import (
    QGraphicsEllipseItem,

)
from PyQt5.QtCore import (
    QPointF,
)


class Point(QPointF, QGraphicsEllipseItem):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)