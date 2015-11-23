#!/user/bin/env python
# coding=utf-8
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL, SLOT
import subprocess
import compareScan2
import pickle
from parseNmap import NMapScan
from parseNessus import Nessus

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



    #   self.boutoncomparer.clicked.connect(self.comparer)
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




    def showDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                '/home')

        f = open(fname, 'r')
        self.fenetrescan1.append(fname)
    def showDialog2(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                '/home')

        f = open(fname, 'r')
        self.fenetrescan2.append(fname)

class Form(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        scanap_scan_file="scan-115007-102615.xml"
        scanap_scan_file2="scan-144848-101915.xml"
        self.scan = NMapScan(scanap_scan_file, scanap_scan_file2)

        nessusfile = "xp_27.nessus"
        nessusfileB = "xp_27B.nessus"
        self.ne = Nessus(nessusfile, nessusfileB)

        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        self.setFixedHeight(450)
        self.setFixedWidth(950)
        self.setWindowTitle("ports ouverts nmap scan")

    def create_widgets(self):
        self.boiteresultats = QtGui.QGroupBox('Resultats')
        self.boitelancement = QtGui.QGroupBox('')
        self.browser = QtGui.QTextBrowser()
        self.buttonAnmap = QtGui.QPushButton("Scan 1 Nmap")
        self.buttonBnmap = QtGui.QPushButton("Scan 2 Nmap")
        self.buttonDiffHostnmap = QtGui.QPushButton("Diff Nmap")
        self.buttonAnessus = QtGui.QPushButton("Scan 1 Nessus")
        self.buttonBnessus = QtGui.QPushButton("Scan 2 Nessus")
        self.buttonDiffHostnessus = QtGui.QPushButton("Diff Nessus")
        self.btnnmap = QtGui.QPushButton('Lancer NMap', self)
        self.btnnessus = QtGui.QPushButton('Lancer Nessus', self)

    def layout_widgets(self):

        self.setStyle(QtGui.QStyleFactory.create("plastique"))

        self.boitelancement.setFixedSize(200, 430)
        self.boiteresultats.setFixedSize(200, 430)

        self.btnnessus.setToolTip('Inspection et analyse des vulnerabilites')
        self.btnnessus.setStatusTip('Inspection et analyse des vulnerabilites')

        self.btnnmap.setToolTip('Inspection et analyse des ports')
        self.btnnmap.setStatusTip('Inspection et analyse des ports')


        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.buttonAnmap)
        buttonLayout.addWidget(self.buttonBnmap)
        buttonLayout.addWidget(self.buttonDiffHostnmap)
        buttonLayout.addWidget(self.buttonAnessus)
        buttonLayout.addWidget(self.buttonBnessus)
        buttonLayout.addWidget(self.buttonDiffHostnessus)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addLayout(buttonLayout)
        gauche = QtGui.QVBoxLayout()
        gauche.addWidget(self.btnnmap)
        gauche.addWidget(self.btnnessus)
        self.boitelancement.setLayout(gauche)
        results = QtGui.QVBoxLayout()
        results.addWidget(self.boiteresultats)
        tout = QtGui.QHBoxLayout()
        tout.addWidget(self.boitelancement)
        tout.addLayout(layout)
        tout.addLayout(results)
        self.setLayout(tout)

    def create_connections(self):
        self.buttonAnmap.clicked.connect(self.showANmap)
        self.buttonBnmap.clicked.connect(self.showBNmap)
        self.buttonDiffHostnmap.clicked.connect(self.showDiffHostNmap)
        self.buttonAnessus.clicked.connect(self.showANessus)
        self.buttonBnessus.clicked.connect(self.showBNessus)
        self.buttonDiffHostnessus.clicked.connect(self.showDiffHostNessus)
        self.btnnmap.clicked.connect(self.download)
        self.btnnessus.clicked.connect(self.lancerNessus)

    def showDiffHostNmap(self):
        self.browser.clear()
        self.browser.append("removed : {0}:".format(self.scan.get_removed()))
        self.browser.append("added : {0} ".format(self.scan.get_added()))
        self.browser.append("changed : {0}".format(self.scan.get_changed()))
        self.browser.append("unchanged : {0}".format(self.scan.get_unchanged()))

    def showANmap(self):
        self.browser.clear()
        infoList = self.scan.getInfoA()
        for key in infoList:
            self.browser.append("{0} : {1}".format(key, infoList[key]))

    def showBNmap(self):
        self.browser.clear()
        infoList = self.scan.getInfoB()
        for key in infoList:
            self.browser.append("{0} : {1}".format(key, infoList[key]))

    def showDiffHostNessus(self):
        self.browser.clear()
        self.browser.clear()
        self.browser.append("removed : {0}:".format(self.ne.get_removed()))
        self.browser.append("added : {0} ".format(self.ne.get_added()))
        self.browser.append("changed : {0}".format(self.ne.get_changed()))
        self.browser.append("unchanged : {0}".format(self.ne.get_unchanged()))


    def showANessus(self):
        self.browser.clear()
        self.browser.clear()
        infoList = self.ne.getInfoA()
        for key in infoList:
            self.browser.append("{0} : {1}".format(key, infoList[key]))

    def showBNessus(self):
        self.browser.clear()
        self.browser.clear()
        infoList = self.ne.getInfoB()
        for key in infoList:
            self.browser.append("{0} : {1}".format(key, infoList[key]))

    def download(self):

        self.lancerNMap()
        # todo selection entre nmap et nessus

    def lancerNessus(self):
        self.dialogTextBrowser = MyDialog(self)
        self.dialogTextBrowser.exec_()

    def lancerNMap(self):
        print 'lop'
        self.dialogTextBrowser = MyDialog(self)
        self.dialogTextBrowser.exec_()

       ## text = open('resultatsnmap.txt').read()
       ## self.boitetexte.setPlainText(text)

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
        self.statusBar()
        self.mainmenu = self.menuBar()
        self.extractAction = QtGui.QAction('&Quitter', self)
        self.fenetre = Form(self)

    def layoutwidget(self):

        self.setCentralWidget(self.fenetre)

        self.setStyle(QtGui.QStyleFactory.create("plastique"))

        self.extractAction.setShortcut('Ctrl+Q')
        self.extractAction.setStatusTip('Fermeture')
        fileMenu = self.mainmenu.addMenu('&Fichier')
        fileMenu.addAction(self.extractAction)

        self.fenetre.move(50, 50)

    def createconnection(self):
        self.extractAction.triggered.connect(self.close_application)
        # todo transformé les appels de fonction via des bouton en signals
        #self.connect(self.btnnessus, SIGNAL("clicked()"), self.lancerNessus())

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
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = Window()
    main.show()

    sys.exit(app.exec_())