#!/user/bin/env python
# coding=utf-8
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL, SLOT
import parseNessus
import parseNmap
# import subprocess
# import compareScan2
# import pickle
# todo ici clean import, reformat class


class MyDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self.resize(350, 350)
        self.btnopenscan = QtGui.QPushButton(self)
        self.btnopenscan.move(50, 50)
        self.btnopenscan.setText('ouvrir scan1')
        self.fenetrescan1 = QtGui.QTextEdit(self)
        self.fenetrescan1.setGeometry(QtCore.QRect(100, 200, 150, 50))
        self.fenetrescan1.move(50,100)
        self.btnopenscan2 = QtGui.QPushButton(self)
        self.btnopenscan2.setText('ouvrir scan2')
        self.btnopenscan2.move(50, 150)
        self.fenetrescan2 = QtGui.QTextEdit(self)
        self.fenetrescan2.setGeometry(QtCore.QRect(50, 250,150, 50))
        self.fenetrescan2.move(50,200)
        self.boutoncomparer = QtGui.QPushButton(self)
        self.boutoncomparer.setText('comparer')
        self.boutoncomparer.move (50,300)
        self.boutonannuler = QtGui.QPushButton(self)
        self.boutonannuler.setText('annuler')
        self.boutonannuler.move (200,300)

        self.boutoncomparer.clicked.connect(self.comparer)
        self.boutonannuler.clicked.connect(self.annuler)
        self.btnopenscan.clicked.connect(self.ouvririnterface)
        self.btnopenscan2.clicked.connect(self.ouvririnterface2)
        self.show()

    def comparer(self):
        pass
        #compare2scans

    def annuler(self):
        self.close()

    def ouvririnterface(self):
        self.showDialog()

    def ouvririnterface2(self):
        self.showDialog2()
    # todo appel de fonction via bar de menu ou bouton import file

    def showDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')

        f = open(fname, 'r')
        self.fenetrescan1.append(fname)
        f.close()
        return fname

    def showDialog2(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')

        f = open(fname, 'r')
        self.fenetrescan2.append(fname)


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.nessusFileA = ""
        self.nessusFileB = ""
        self.NMapFileA = ""
        self.NMapFileB = ""

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
        #self.mainmenu = QtGui.QMenuBar

        self.btnlancer = QtGui.QPushButton('Lancer NMap', self)
        self.btnnessus = QtGui.QPushButton('Lancer Nessus', self)
        #self.openAction = QtGui.QAction('&Open', self)
        self.extractAction = QtGui.QAction('&Quitter', self)
        self.boitetexte = QtGui.QTextBrowser(self)

    def layoutwidget(self):
        self.setStyle(QtGui.QStyleFactory.create("plastique"))

        self.progress.setGeometry(50, 380, 200, 15)

        self.apropos.setShortcut('Ctrl+H')
        self.apropos.setStatusTip('A Propos')
        self.extractAction.setShortcut('Ctrl+Q')
        self.extractAction.setStatusTip('Fermeture')
        self.ouvrirNmapmenu.setShortcut('Ctrl+N')
        self.ouvrirNmapmenu.setStatusTip('Lancer un Scan avec NMap')
        self.ouvrirNessusmenu.setShortcut('Ctrl+W')
        self.ouvrirNessusmenu.setStatusTip('Lancer un Scan avec Nessus')
        fileMenu = self.mainmenu.addMenu('&Fichier')
        AideMenu = self.mainmenu.addMenu('&Aide')

        AideMenu.addAction(self.apropos)
        fileMenu.addAction(self.extractAction)
        fileMenu.addAction(self.ouvrirNmapmenu)
        fileMenu.addAction(self.ouvrirNessusmenu)

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
        #todo faire en sorte que le myDialog devienne un openfile dialog
        #self.openAction.triggered.connect(self.close_application)
        self.extractAction.triggered.connect(self.close_application)
        self.ouvrirNmapmenu.triggered.connect(self.lancerNMap)
        self.ouvrirNessusmenu.triggered.connect(self.lancerNessus)
        self.apropos.triggered.connect(self.InterfaceApropos)
        self.btnlancer.clicked.connect(self.download)
        self.btnnessus.clicked.connect(self.lancerNessus)
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
        self.dialogTextBrowser = MyDialog(self)
        self.dialogTextBrowser.exec_()
        
    def InterfaceApropos(self):
        propos = QtGui.QMessageBox.about(self, 'A Propos',
            'Travail realise par les CHAMPS!  WOOHOO!!!')

    def lancerNMap(self):
        print 'lop'
        self.dialogTextBrowser = MyDialog(self)
        self.dialogTextBrowser.exec_()
    # todo rework appel de fonction et link de script
       ## text = open('resultatsnmap.txt').read()
       ## self.boitetexte.setPlainText(text)

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


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = Window()
    main.show()

    sys.exit(app.exec_())

