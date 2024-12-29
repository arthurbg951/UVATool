from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsSceneHoverEvent,
    QGraphicsPixmapItem,

)
from PyQt5.QtCore import (
    Qt,
    QPointF,
)
from PyQt5.QtGui import (
    QKeyEvent,
    QColor,
    QPixmap,
)

class FixedItem(QGraphicsPixmapItem):
    # REPRESENTA O APOIO DE TERCEIRO GENERO
    def __init__(self, x: float, y: float):
        super().__init__(QPixmap("icons/apoio_terceiro_genero.png"))
        self.__x = x - 16
        self.__y = y - 15
        self.__pos = QPointF(self.__x, self.__y)
        self.setPos(QPointF(self.__x, self.__y))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setZValue(1)
        self.setFocus()
        self.setAcceptHoverEvents(True)
        self.__isSelected = False

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            if self.isSelected():
                print('Botão deletar não implementado')
        if event.key() == Qt.Key.Key_Escape:
            self.setSelected(False)

    def setColor(self, color: QColor):
        tmp = self.pixmap().toImage()
        for y in range(tmp.height()):
            for x in range(tmp.width()):
                color.setAlpha(tmp.pixelColor(x, y).alpha())
                tmp.setPixelColor(x, y, color)
        self.setPixmap(QPixmap.fromImage(tmp))

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.setFocus()

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.clearFocus()

    def setSelected(self, selected: bool) -> None:
        if selected:
            self.setColor(QColor(255, 0, 0))
            self.__isSelected = True
        else:
            self.setColor(QColor(0, 0, 0))
            self.__isSelected = False

    def isSelected(self) -> bool:
        if self.__isSelected:
            return True
        else:
            return False

    def scenePos(self) -> QPointF:
        return self.__pos

    def x(self):
        return self.__x * 10

    def y(self):
        return - self.__y * 10

