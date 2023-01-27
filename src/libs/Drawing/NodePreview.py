from PyQt5.QtWidgets import (
    QGraphicsEllipseItem,

)
from PyQt5.QtCore import (
    Qt,
    QPointF,
    QRectF,
)
from PyQt5.QtGui import (
    QPen,
    QBrush,
)

class NodePreview(QGraphicsEllipseItem):
    def __init__(self, x: float, y: float):
        __diameter = 10
        self.__x = x
        self.__y = y
        self.__pos = QPointF(self.__x, self.__y)
        super().__init__(QRectF(x - __diameter/2, y - __diameter/2, __diameter, __diameter))
        self.setPen(QPen(Qt.GlobalColor.black, 1))
        self.setBrush(QBrush(Qt.GlobalColor.gray, Qt.BrushStyle.SolidPattern))
        self.setZValue(1)
        # self.setAcceptHoverEvents(True)

    def setSelected(self, selected: bool) -> None:
        super().setSelected(False)

    def scenePos(self) -> QPointF:
        return self.__pos
