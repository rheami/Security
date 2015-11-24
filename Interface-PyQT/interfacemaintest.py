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
        nmap_scan_fileA="./scanNMap/scan-115007-102615.xml"
        nmap_scan_fileB="./scanNMap/scan-144848-101915.xml"
        self.nmap_scan = NMapScan(nmap_scan_fileA, nmap_scan_fileB)

        nessusfileA = "./scanNessus/xp_27.nessus"
        nessusfileB = "./scanNessus/xp_27B.nessus"
        self.nessus_scan = Nessus(nessusfileA, nessusfileB)

        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        self.setFixedHeight(500)
        self.setFixedWidth(1200)
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
        self.btnnmap = QtGui.QPushButton('NMap', self)
        self.btnnessus = QtGui.QPushButton('Nessus', self)
        self.image = QtGui.QLabel()
        self.imagepx = QtGui.QPixmap('./000Lock.png').scaled(180, 180)
        self.image.setPixmap(self.imagepx)
        self.buttonHachage = QtGui.QPushButton('Executables', self)
        self.buttonExe1 = QtGui.QPushButton('.exe 1')
        self.buttonExe2 = QtGui.QPushButton('.exe 2')
        self.buttonExeResult = QtGui.QPushButton('.exe resultat')


    def layout_widgets(self):

        self.setStyle(QtGui.QStyleFactory.create("plastique"))

        self.boitelancement.setFixedSize(200, 480)
        self.boiteresultats.setFixedSize(200, 480)

        self.btnnessus.setToolTip('Inspection et analyse des vulnerabilites')
        self.btnnessus.setStatusTip('Inspection et analyse des vulnerabilites')

        self.btnnmap.setToolTip('Inspection et analyse des ports')
        self.btnnmap.setStatusTip('Inspection et analyse des ports')


        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(self.buttonExe1)
        buttonLayout.addWidget(self.buttonExe2)
        buttonLayout.addWidget(self.buttonExeResult)
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
        gauche.addWidget(self.buttonHachage)
        self.boitelancement.setLayout(gauche)
        results = QtGui.QVBoxLayout()
        results.addWidget(self.image)
        self.boiteresultats.setLayout(results)
        tout = QtGui.QHBoxLayout()
        tout.addWidget(self.boitelancement)
        tout.addLayout(layout)
        tout.addWidget(self.boiteresultats)
        self.setLayout(tout)

    def create_connections(self):
        self.buttonAnmap.clicked.connect(self.showANmap)
        self.buttonBnmap.clicked.connect(self.showBNmap)
        self.buttonDiffHostnmap.clicked.connect(self.showDiffHostNMap)
        self.buttonAnessus.clicked.connect(self.showANessus)
        self.buttonBnessus.clicked.connect(self.showBNessus)
        self.buttonDiffHostnessus.clicked.connect(self.showDiffHostNessus)
        self.btnnmap.clicked.connect(self.download)
        self.btnnessus.clicked.connect(self.lancerNessus)
        self.buttonExe1.clicked.connect(self.exe1)
        self.buttonExe2.clicked.connect(self.exe2)
        self.buttonExeResult.clicked.connect(self.exeResults)

    def exe1(self):
        self.browser.clear()
    # todo

    def exe2(self):
        self.browser.clear()
    # todo

    def exeResults(self):
        self.browser.clear()
    # todo

    def showDiffHostNessus(self):
        self.scan = self.nessus_scan
        self.showDiffHost()

    def showDiffHostNMap(self):
        self.scan = self.nmap_scan
        self.showDiffHost()

    def showDiffHost(self):
        self.browser.clear()
        self.showRemoved()
        self.showAdded()
        self.showChanged()
        #self.showUnchanged()

    def showRemoved(self):
        self.browser.append("removed :")
        self.showList(self.scan.get_removed())

    def showAdded(self):
        self.browser.append("added :")
        self.showList(self.scan.get_added())

    def showChanged(self):
        self.browser.append("changed :")
        self.showList(self.scan.get_changed())

    def showUnchanged(self):
        self.browser.append("unchanged :")
        self.showList(self.scan.get_unchanged())

    def showList(self, info_dict):
        for key in info_dict:
            self.browser.append("{0} : {1}".format(key, info_dict[key]))

    def showANmap(self):
        self.scan = self.nmap_scan
        self.browser.clear()
        self.showList(self.scan.getInfoA())

    def showBNmap(self):
        self.scan = self.nmap_scan
        self.browser.clear()
        self.showList(self.scan.getInfoB())

    def showANessus(self):
        self.scan = self.nessus_scan
        self.browser.clear()
        self.showList(self.scan.getInfoA())

    def showBNessus(self):
        self.scan = self.nessus_scan
        self.browser.clear()
        self.showList(self.scan.getInfoB())

    def download(self):

        self.lancerNMap()
        # todo selection entre nmap et nessus

    def lancerNessus(self):
        self.dialogTextBrowser = MyDialog(self)
        self.dialogTextBrowser.exec_()

        self.scan = self.nessus_scan

        self.afficherImage(self.scan.getMaxSeverity())

    def lancerNMap(self):
        self.dialogTextBrowser = MyDialog(self)
        self.dialogTextBrowser.exec_()

    def afficherImage(self, number):
        if number == 0:
            self.imagepx = QtGui.QPixmap('./greencheck2.png').scaled(180, 180)
        elif number == 1:
            self.imagepx = QtGui.QPixmap('./bluecheck.png').scaled(180, 180)
        elif number == 2:
            self.imagepx = QtGui.QPixmap('./yellowcheck.png').scaled(180, 180)
        elif number == 3:
            self.imagepx = QtGui.QPixmap('./orangecheck.png').scaled(180, 180)
        else:
            self.imagepx = QtGui.QPixmap('./redcheck.png').scaled(180, 180)

        self.image.setPixmap(self.imagepx)

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