#!/user/bin/env python
# coding=utf-8
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL, SLOT
import subprocess
import compareScan2
import pickle


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.resize(950, 450)
        self.setWindowTitle('Detecteur de vulnerabilites')
        self.setWindowIcon(QtGui.QIcon('logo.png'))

        self.createwidget()
        self.layoutwidget()
        self.createconnection()

    def createwidget(self):
        self.progress = QtGui.QProgressBar(self)
        self.statusBar()

        self.mainmenu = self.menuBar()

        self.btnlancer = QtGui.QPushButton('Lancer NMap', self)
        self.btnnessus = QtGui.QPushButton('Lancer Nessus', self)
        self.extractAction = QtGui.QAction('&Quitter', self)
        self.boitetexte = QtGui.QTextEdit(self)

    def layoutwidget(self):
        self.setStyle(QtGui.QStyleFactory.create("plastique"))

        self.progress.setGeometry(50, 380, 200, 15)

        self.extractAction.setShortcut('Ctrl+Q')
        self.extractAction.setStatusTip('Fermeture')
        fileMenu = self.mainmenu.addMenu('&Fichier')
        fileMenu.addAction(self.extractAction)

        self.btnnessus.setToolTip('Inspection et analyse des vuln') # érabilité')
        self.btnnessus.move(50, 100)
        self.btnnessus.resize(100, 50)
        self.btnnessus.setStatusTip('Inspection et analyse des vuln') # érabilité')

        self.btnlancer.setToolTip('Inspection et analyse des ports')
        self.btnlancer.move(50, 50)
        self.btnlancer.resize(100, 50)
        self.btnlancer.setStatusTip('Inspection et analyse des ports')

        self.boitetexte.setGeometry(QtCore.QRect(330, 50, 270, 350))
        self.boitetexte.setObjectName("Resultats NMap")

    def createconnection(self):
        self.extractAction.triggered.connect(self.close_application)
        self.btnlancer.clicked.connect(self.download)
        # todo transformé les appels de fonction via des bouton en signals
        #self.connect(self.btnnessus, SIGNAL("clicked()"), self.lancerNessus())

    def download(self):
        completed = 0

        while completed < 100:
            completed += 0.00015
            self.progress.setValue(completed)

        self.lancerNMap()
        # todo selection entre nmap et nessus

    def lancerNessus(self):
        pass
        # todo lancer le script nessus via le bouton

    def lancerNMap(self):
        compareScan2.main('scan-115007-102615.xml', 'scan-144848-101915.xml')

        text = open('resultatsnmap.txt').read()
        self.boitetexte.setPlainText(text)

    def closeEvent(self, event):
        event.ignore()
        self.close_application()

    def close_application(self):
        choice = QtGui.QMessageBox.question(self, 'Quitter',
                                            'Etes-vous certain de vouloir quitter?',
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print('Fin normale du programme')
            sys.exit()
        else:
            pass


def main():
    app = QtGui.QApplication(sys.argv)
    gui = Window()
    gui.show()
    app.exec_()

main()

