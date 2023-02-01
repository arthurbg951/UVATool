from PyQt5.QtWidgets import (
    QGraphicsSceneHoverEvent,
    QGraphicsLineItem,

)
from PyQt5.QtCore import (
    Qt,
)
from PyQt5.QtGui import (
    QPen,
    QColor,
)
from UVATool import Element

class ElementItem(QGraphicsLineItem):
    def __init__(self, line: QGraphicsLineItem) -> None:
        super().__init__()
        self.setPen(line.pen())
        self.setLine(line.line())
        self.setAcceptHoverEvents(True)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Element):
            return NotImplemented
        return self.element == __o.element

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        # self.setPen(QPen(self.pen().color(), 4, self.pen().style()))
        # self.setFocus()
        pass

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        # self.setPen(QPen(self.pen().color(), 2, self.pen().style()))
        # self.clearFocus()
        pass

    def hasFocus(self) -> bool:
        if self.pen().width() == 4:
            return True
        else:
            return False

    def setSelected(self, selected: bool) -> None:
        width = self.pen().width()
        style = self.pen().style()
        if selected:
            self.setPen(QPen(Qt.GlobalColor.red, width, style))
        else:
            self.setPen(QPen(Qt.GlobalColor.gray, width, style))

    def setColor(self, color: QColor):
        # line = QPen(color, self.pen().width(), self.pen().style())
        # self.setPen(line)
        self.pen().setColor(Qt.GlobalColor.red)

    def isSelected(self) -> bool:
        if self.pen().color() == Qt.GlobalColor.red:
            return True
        else:
            return False
