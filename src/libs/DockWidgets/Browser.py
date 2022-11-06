from PyQt5.QtWidgets import (
    QDockWidget,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QWidget,
    QSpacerItem,
    QSizePolicy,
    QGraphicsScene,
    QMessageBox,
)

from PyQt5.QtCore import QObject, QThread, pyqtSignal
from libs.Drawing import *
from PyQt5 import QtCore, QtGui, QtWidgets
from time import sleep


class Browser(QDockWidget):

    CreateNode: QPushButton

    def __init__(self, scene: QGraphicsScene) -> None:
        super().__init__()
        self.scene = scene
        self.nodes: list[NodeDraw] = self.scene.nodes
        self.elements: list[ElementDraw] = self.scene.elements
        self.dockWidget = self
        self.setWindowTitle("Browser")
        self.setFeatures(self.DockWidgetFeature.DockWidgetClosable)

        self.dockWidget.setMaximumSize(QtCore.QSize(250, 524287))
        self.dockWidget.setBaseSize(QtCore.QSize(120, 0))
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.dockWidgetContents)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.listWidget = QtWidgets.QListWidget(self.tab)
        self.listWidget.setMinimumSize(QtCore.QSize(100, 0))
        self.listWidget.setObjectName("listWidget")

        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setMaximumSize(QtCore.QSize(35, 35))
        self.pushButton.setText("")
        self.pushButton.setDisabled(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(25, 25))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setMaximumSize(QtCore.QSize(35, 35))
        self.pushButton_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/erase.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setDisabled(True)
        self.horizontalLayout.addWidget(self.pushButton_2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        self.pushButton_3.setMaximumSize(QtCore.QSize(35, 35))
        self.pushButton_3.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setDisabled(True)
        self.horizontalLayout.addWidget(self.pushButton_3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.tab)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Nodes")
        self.comboBox.addItem("Elements")
        # self.comboBox.currentIndexChanged.connect(self.setItens)
        self.comboBox.currentIndexChanged.connect(self.runLongTask)
        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "Data")
        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")
        self.tabWidget.addTab(self.widget, "Analysis")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.dockWidget.setWidget(self.dockWidgetContents)

        # self.setItens()
        self.runLongTask()

    def setItens(self):
        self.listWidget.clear()
        if self.comboBox.currentText() == "Nodes":
            for index in range(len(self.nodes)):
                self.listWidget.addItem(f"id:{index+1} - coord:({self.nodes[index].x}, {self.nodes[index].y})")
        if self.comboBox.currentText() == "Elements":
            for index in range(len(self.elements)):
                self.listWidget.addItem(f"id:{index+1} - nodes:({self.nodes.index(self.elements[index].node1) + 1} -> {self.nodes.index(self.elements[index].node2) + 1})")

    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        self.worker.setFunction(self.setItens)
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Step 6: Start the thread
        self.thread.start()


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        """Long-running task."""
        self.function()
        self.finished.emit()

    def setFunction(self, function):
        self.function = function


"""
EXEMPLO UTILIZAÇÃO LISTWIDGET COM CLICK

from PyQt5.QtWidgets import *
import sys

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)
        self.listwidget = QListWidget()
        self.listwidget.insertItem(0, "Red")
        self.listwidget.insertItem(1, "Orange")
        self.listwidget.insertItem(2, "Blue")
        self.listwidget.insertItem(3, "White")
        self.listwidget.insertItem(4, "Green")
        self.listwidget.clicked.connect(self.clicked)
        layout.addWidget(self.listwidget)

    def clicked(self, qmodelindex):
        item = self.listwidget.currentItem()
        print(item.text())

app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())
"""
