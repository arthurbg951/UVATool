from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QGraphicsScene, QHBoxLayout, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QGraphicsView, QGraphicsItem, QGraphicsSceneMouseEvent
from PyQt5.QtGui import QIcon, QPen, QPixmap, QMouseEvent, QBrush
from PyQt5.QtCore import Qt, QSize, QPointF, QPoint
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 800, 800)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setMinimumSize(QSize(32, 32))
        self.pushButton_2.setMaximumSize(QSize(32, 32))
        self.pushButton_2.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(
            "./src/UVATool_UI/icons/apoio_primeiro_genero.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QSize(32, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.primeiroGenero)
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setMinimumSize(QSize(32, 32))
        self.pushButton_3.setMaximumSize(QSize(32, 32))
        self.pushButton_3.setText("")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(
            "./src/UVATool_UI/icons/apoio_segundo_genero.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_3.setIcon(icon1)
        self.pushButton_3.setIconSize(QSize(32, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.segundoGenero)
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setMinimumSize(QSize(32, 32))
        self.pushButton_4.setMaximumSize(QSize(32, 32))
        self.pushButton_4.setText("")
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(
            "./src/UVATool_UI/icons/apoio_terceiro_genero.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_4.setIcon(icon2)
        self.pushButton_4.setIconSize(QSize(32, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.terceiroGenero)
        self.verticalLayout.addWidget(self.pushButton_4)
        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setMinimumSize(QSize(32, 32))
        self.pushButton_5.setMaximumSize(QSize(32, 32))
        self.pushButton_5.setText("")
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(
            "./src/UVATool_UI/icons/apoio_semi_rigido.png"), QIcon.Normal, QIcon.Off)
        self.pushButton_5.setIcon(icon3)
        self.pushButton_5.setIconSize(QSize(32, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.semiRigido)
        self.verticalLayout.addWidget(self.pushButton_5)
        spacerItem = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.graphicsScene = QGraphicsScene()
        self.graphicsScene.mousePressEvent = self.mousePressEventScene
        self.graphicsView = QGraphicsView(
            self.graphicsScene, self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setGeometry(0, 0, 800, 800)

        self.horizontalLayout.addWidget(self.graphicsView)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.pushButton_2)
        self.hbox.addWidget(self.pushButton_3)
        self.hbox.addWidget(self.pushButton_4)
        self.hbox.addWidget(self.pushButton_5)
        self.hbox.addWidget(self.graphicsView)

        self.image = "./src/UVATool_UI/icons/apoio_primeiro_genero.png"
        self.correcaoClickImagem = [16, 5]

        self.gridActive = False
        if self.gridActive:
            for i in range(-50, 50, 1):
                for j in range(-50, 50, 1):
                    self.graphicsScene.addEllipse(i*10, j * 10, 1, 1, QPen(
                        Qt.GlobalColor.black), QBrush(Qt.BrushStyle.SolidPattern))

        self.graphicsScene.setSceneRect(0, 0, 100,  100)

        self.setLayout(self.hbox)

        self.click_count = 0

    # def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
    #     print(event.pos())
    #     # print(self.graphicsView.mapToScene(event.pos()))
    #     print(event.scenePos())
    #     pixMap = QPixmap("./src/UVATool_UI/icons/apoio_primeiro_genero.png")
    #     imagem = self.graphicsScene.addPixmap(pixMap)
    #     # imagem.setPos(QPointF(event.pos().x() - self.graphicsView.pos().x(), event.pos().y() - self.graphicsView.pos().y()))
    #     # imagem.setPos(self.graphicsView.mapToScene(event.pos()))
    #     imagem.setPos(event.scenePos())
    #     imagem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

    def mousePressEventScene(self, event: QGraphicsSceneMouseEvent):
        x = event.scenePos().x() 
        y = event.scenePos().y() 
        print(x, y)

        # xString = x[0]+x[1]+
        pixMap = QPixmap(self.image)
        imagem = self.graphicsScene.addPixmap(pixMap)
        point = None
        if self.gridActive:
            xString = int(str(x)[:-2])
            yString = int(str(y)[:-2])

            if xString % 10 < 5:
                xString = xString - xString % 10
            else:
                xString = xString + (10-xString % 10)

            if yString % 10 < 5:
                yString = yString - yString % 10
            else:
                yString = yString + (10-yString % 10)
            print('VALORES DE X E Y ALTERADOS')
            print(xString, yString)
            point = QPointF(float(xString), float(yString))
        else:
            point = QPointF(
                x - self.correcaoClickImagem[0], y - self.correcaoClickImagem[1])
        imagem.setPos(point)
        imagem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

    def primeiroGenero(self):
        self.image = "./src/UVATool_UI/icons/apoio_primeiro_genero.png"
        self.correcaoClickImagem = [16, 5]

    def segundoGenero(self):
        self.image = "./src/UVATool_UI/icons/apoio_segundo_genero.png"
        self.correcaoClickImagem = [17, 7]

    def terceiroGenero(self):
        self.image = "./src/UVATool_UI/icons/apoio_terceiro_genero.png"
        self.correcaoClickImagem = [17, 14]

    def semiRigido(self):
        self.image = "./src/UVATool_UI/icons/apoio_semi_rigido.png"
        self.correcaoClickImagem = [15, 12]


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
