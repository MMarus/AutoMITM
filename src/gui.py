# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mitm.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import logging

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class QPlainTextEditLoggerHandler(logging.Handler):
    def __init__(self, element):
        logging.Handler.__init__(self)
        self.widget = QtGui.QPlainTextEdit(element)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendHtml(msg)




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(640, 480)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 631, 431))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton = QtGui.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_2.setEnabled(False)
        self.gridLayout.addWidget(self.pushButton_2, 1, 2, 1, 1)
        self.H1 = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Asana Math"))
        font.setPointSize(26)
        self.H1.setFont(font)
        self.H1.setTextFormat(QtCore.Qt.AutoText)
        self.H1.setAlignment(QtCore.Qt.AlignCenter)
        self.H1.setObjectName(_fromUtf8("H1"))
        self.gridLayout.addWidget(self.H1, 0, 0, 1, 3)
        self.pushButton_3 = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 3, 1, 1, 1)


        #self.plainTextEdit = QtGui.QPlainTextEdit(self.layoutWidget)

        self.plainTextEdit2 = QPlainTextEditLoggerHandler(self.layoutWidget)

        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Asana Math"))
        self.plainTextEdit2.widget.setFont(font)
        self.plainTextEdit2.widget.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);"))
        #self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit2.widget.setObjectName(_fromUtf8("plainTextEdit"))


        #self.gridLayout.addWidget(self.plainTextEdit, 2, 0, 1, 3)
        self.gridLayout.addWidget(self.plainTextEdit2.widget, 2, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(_translate("MainWindow", "Start attack", None))
        self.pushButton_2.setText(_translate("MainWindow", "Stop attack", None))
        self.H1.setText(_translate("MainWindow", "MitM probe", None))
        self.pushButton_3.setText(_translate("MainWindow", "Settings", None))
        #self.plainTextEdit2.widget.setPlainText(_translate("MainWindow", "hoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoihoihohoi", None))


# if __name__ == "__main__":
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     MainWindow = QtGui.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())


class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super(self).__init__()

        self.widget = QtGui.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.textCursor().appendPlainText(msg)

