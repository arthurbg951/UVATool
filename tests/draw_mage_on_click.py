# from PyQt5.QtWidgets import QApplication, QWidget, QLabel
# from PyQt5.QtGui import QIcon, QFont, QPixmap, QMovie
# import sys


# class Window(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.setGeometry(200,200, 700, 400)
#         self.setWindowTitle("Draw Image")
#         # self.setWindowIcon(QIcon('images/python.png'))


#         label = QLabel(self)
#         pixmap = QPixmap('src\\UVATool_UI\\icons\\apoio_primeiro_genero.png')
#         label.setPixmap(pixmap)


# app = QApplication(sys.argv)
# window = Window()
# window.show()
# sys.exit(app.exec())

from ast import IsNot
from turtle import begin_fill
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QFont, QMouseEvent, QPixmap, QPainter, QPen, QImage, QPaintEvent
from PyQt5.QtCore import Qt, QPoint, QRect
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 700, 400)
        self.setWindowTitle("Python Drawing Icons")
        # self.begin, self.destination = QPoint(), QPoint()

        self.mousePosition = QPoint()
        self.image = QImage(
            "src\\UVATool_UI\\icons\\apoio_primeiro_genero.png")

        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.GlobalColor.transparent)

        self.click_count = 0

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.pix)

        # Imagem sem problemas
        # rect = QRect(QPoint(0,0), self.image.size())
        # painter.drawImage(rect, self.image)
        # if not self.begin.isNull() and not self.destination.isNull():
        if not self.mousePosition.isNull():
            # rect = QRect(self.begin, self.destination)
            rect = QRect(self.mousePosition, self.image.size())
            painter.drawImage(rect, self.image)

    def mousePressEvent(self, event: QMouseEvent):
        self.click_count += 1
        print(self.click_count)
        if event.buttons() & Qt.MouseButton.LeftButton:
            # print(event.pos())
            # self.begin = event.pos()

            # self.begin = QPoint(event.pos().x(), event.pos().y())
            # self.destination = QPoint(
            #     event.pos().x() + 32, event.pos().y() + 32)

            # print(self.begin, self.destination)
            self.mousePosition = QPoint(
                event.pos().x() - 16, event.pos().y() - 5)
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() & Qt.MouseButton.LeftButton:
            # print(event.pos())
            # self.begin = QPoint(event.pos().x() - 16, event.pos().y())
            # self.destination = QPoint(
            #     event.pos().x() + 16, event.pos().y() + 32)

            # Ponta do triangulo
            # self.begin = QPoint(event.pos().x() - 16, event.pos().y() - 5)
            # self.destination = QPoint(
            #     event.pos().x() + 16, event.pos().y() + 32)

            # Ponto (0,0) da imagem
            # self.begin = QPoint(event.pos().x(), event.pos().y())
            # self.destination = QPoint(
            #     event.pos().x() + 32, event.pos().y() + 32)

            # self.destination = event.pos()
            self.mousePosition = QPoint(
                event.pos().x() - 16, event.pos().y() - 5)
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.MouseButton.LeftButton:
            rect = QPoint(
                event.pos().x() - 16, event.pos().y() - 5)
            painter = QPainter(self.pix)
            painter.drawImage(rect, self.image)
            self.update()


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
