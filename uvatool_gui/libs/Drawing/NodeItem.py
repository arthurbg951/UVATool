from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsSceneHoverEvent,
    QGraphicsRectItem,

)
from PyQt5.QtCore import (
    Qt,
    QPointF,
    QRectF,
)
from PyQt5.QtGui import (
    QPen,
    QBrush,
    QKeyEvent,
)

class NodeItem(QGraphicsRectItem):
    # ESSE ITEM REPRESENTA O NÓ PADRÃO
    def __init__(self, rec: QRectF):
        super().__init__(rec)
        self.__x = rec.x()
        self.__y = rec.y()
        self.__pos = QPointF(self.__x, self.__y)
        self.setPen(QPen(Qt.GlobalColor.black, 1))
        self.setBrush(QBrush(Qt.GlobalColor.black, Qt.BrushStyle.SolidPattern))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setZValue(1)
        self.setFocus()
        self.setAcceptHoverEvents(True)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            if self.isSelected():
                print('Botão deletar não implementado')
        if event.key() == Qt.Key.Key_Escape:
            self.setSelected(False)

    def setColor(self, color: Qt.GlobalColor):
        self.setBrush(QBrush(color))

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.setFocus()

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.clearFocus()

    def setSelected(self, selected: bool) -> None:
        if selected:
            self.setColor(Qt.GlobalColor.red)
        else:
            self.setColor(Qt.GlobalColor.black)

    def isSelected(self) -> bool:
        if self.brush() == QBrush(Qt.GlobalColor.red):
            return True
        else:
            return False

    def scenePos(self) -> QPointF:
        return self.__pos

    def x(self):
        return self.__x * 10

    def y(self):
        return - self.__y * 10
