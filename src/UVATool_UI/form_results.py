# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form_results.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ResultForm(object):
    def setupUi(self, ResultForm):
        ResultForm.setObjectName("ResultForm")
        ResultForm.resize(435, 362)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/table.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ResultForm.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(ResultForm)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QtWidgets.QTableView(ResultForm)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 1)

        self.retranslateUi(ResultForm)
        QtCore.QMetaObject.connectSlotsByName(ResultForm)

    def retranslateUi(self, ResultForm):
        _translate = QtCore.QCoreApplication.translate
        ResultForm.setWindowTitle(_translate("ResultForm", "Results"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ResultForm = QtWidgets.QDialog()
    ui = Ui_ResultForm()
    ui.setupUi(ResultForm)
    ResultForm.show()
    sys.exit(app.exec_())