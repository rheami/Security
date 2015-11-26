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
from bs4 import BeautifulSoup


class MyDialog(QtGui.QDialog):
    def __init__(self, parent):

        super(MyDialog, self).__init__(parent)
        self.fname = ""
        self.fname2 = ""
        self.number = 1
        self.setWindowTitle('Scans a comparer')
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()

        self.show()

    def create_widgets(self):
        self.btnopenscan = QtGui.QPushButton('ouvrir scan1')
        self.fenetrescan1 = QtGui.QTextEdit(self)
        self.btnopenscan2 = QtGui.QPushButton('ouvrir scan2')
        self.fenetrescan2 = QtGui.QTextEdit(self)
        self.boutoncomparer = QtGui.QPushButton('comparer')
        self.boutonannuler = QtGui.QPushButton('annuler')
        self.boitescan1 = QtGui.QGroupBox('')
        self.boitescan2 = QtGui.QGroupBox('')


    def layout_widgets(self):
        self.resize(300, 300)
        self.boutonLayout = QtGui.QVBoxLayout()
        self.verti1 = QtGui.QVBoxLayout()
        self.verti1.addWidget(self.btnopenscan)
        self.verti1.addWidget(self.fenetrescan1)
        self.boitescan1.setLayout(self.verti1)
        self.verti2 = QtGui.QVBoxLayout()
        self.verti2.addWidget(self.btnopenscan2)
        self.verti2.addWidget(self.fenetrescan2)
        self.boitescan2.setLayout(self.verti2)
        self.horiz = QtGui.QHBoxLayout()
        self.horiz.addWidget(self.boutoncomparer)
        self.horiz.addWidget(self.boutonannuler)
        self.boutonLayout.addWidget(self.boitescan1)
        self.boutonLayout.addWidget(self.boitescan2)
        self.boutonLayout.addLayout(self.horiz)
        self.setLayout(self.boutonLayout)

        self.boitescan1.setStyleSheet("""
        .QGroupBox {
            border: 0px;
            border-radius: 2px;
            background-color: rgb(248, 248, 248);
            }
        """)

        self.boitescan2.setStyleSheet("""
        .QGroupBox {
            border: 0px;
            border-radius: 2px;
            background-color: rgb(248, 248, 248);
            }
        """)

    def create_connections(self):
        #   self.boutoncomparer.clicked.connect(self.comparer)
        self.boutonannuler.clicked.connect(self.annuler)
        self.btnopenscan.clicked.connect(self.ouvririnterface)
        self.btnopenscan2.clicked.connect(self.ouvririnterface2)
        self.boutoncomparer.clicked.connect(self.comparer)

    def comparer(self,number):


        if self.parent().parent().nmapounessus== 1:

            self.parent().scan = Nessus(self.fname,self.fname2)
            self.parent().showDiffHost()
        else:
         self.parent().scan =  NMapScan(str(self.fname),str(self.fname2))
         self.parent().showDiffHost()

        self.close()

    def annuler(self):
        self.close()

    def ouvririnterface(self):
        self.showDialog(self.parent().number)

    def ouvririnterface2(self):
        self.showDialog2(self.parent().number)

    def showDialog(self, number):
        print self.parent().number
        if self.parent().number == 0:
            self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                './scanNMap')
        else:
            self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                './scanNessus')

        f = open(self.fname, 'r')
        self.fenetrescan1.append(str(self.fname))
        print self.fname


    def showDialog2(self, number):
        if self.parent().number == 0:

            self.fname2 = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                './scanNMap')
        else:
            self.fname2 = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                './scanNessus')

        f = open(self.fname2, 'r')
        self.fenetrescan2.append(str(self.fname2))

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
        self.number = 0

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

        self.boiteresultats.setStyleSheet("""
        .QGroupBox {
            border: 1px solid black;
            color: gray;
            border-radius: 2px;
            background-color: rgb(248, 248, 248);
            }
        """)

        self.boitelancement.setStyleSheet("""
        .QGroupBox {
            border: 1px solid black;
            border-radius: 2px;
            background-color: rgb(248, 248, 248);
            }
        """)

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
        self.number = 1
        self.parent().nmapounessus = 1
        self.dialogTextBrowser = MyDialog(self)
        self.dialogTextBrowser.exec_()

        self.scan = self.nessus_scan

        self.afficherImage(self.scan.getMaxSeverity())


    def lancerNMap(self):
        self.number = 0

        self.dialogTextBrowser = MyDialog(self)
        self.dialogTextBrowser.exec_()

    def afficherImage(self, number):
        if number == 0:
            self.imagepx = QtGui.QPixmap('./greencheck2.png').scaled(180, 180)
            self.boiteresultats.setStyleSheet("""
            .QGroupBox {
                border: 1px solid black;
                color: green;
                border-radius: 2px;
                background-color: rgb(240, 247, 234);
                }
            """)
        elif number == 1:
            self.imagepx = QtGui.QPixmap('./bluecheck.png').scaled(180, 180)
            self.boiteresultats.setStyleSheet("""
            .QGroupBox {
                border: 1px solid black;
                color: blue;
                border-radius: 2px;
                background-color: rgb(234, 239, 247);
                }
            """)
        elif number == 2:
            self.imagepx = QtGui.QPixmap('./yellowcheck.png').scaled(180, 180)
            self.boiteresultats.setStyleSheet("""
            .QGroupBox {
                border: 1px solid black;
                color: rgb(190, 201, 118);
                border-radius: 2px;
                background-color: rgb(245, 247, 234);
                }
            """)
        elif number == 3:
            self.imagepx = QtGui.QPixmap('./orangecheck.png').scaled(180, 180)
            self.boiteresultats.setStyleSheet("""
            .QGroupBox {
                border: 1px solid black;
                color: orange;
                border-radius: 2px;
                background-color: rgb(245, 237, 220);
                }
            """)
        else:
            self.imagepx = QtGui.QPixmap('./redcheck.png').scaled(180, 180)
            self.boiteresultats.setStyleSheet("""
            .QGroupBox {
                border: 1px solid black;
                color: red;
                border-radius: 2px;
                background-color: rgb(254, 230, 226);
                }
            """)

        self.image.setPixmap(self.imagepx)

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.nmapounessus = 0
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
        self.nmap = QtGui.QAction('&NMap', self)
        self.nessus = QtGui.QAction('&Nessus', self)
        self.exe = QtGui.QAction('&.exe', self)
        self.fenetre = Form(self)

    def layoutwidget(self):

        self.setCentralWidget(self.fenetre)

        self.setStyle(QtGui.QStyleFactory.create("plastique"))

        self.extractAction.setShortcut('Ctrl+Q')
        self.extractAction.setStatusTip('Fermeture')
        self.nmap.setShortcut('Ctrl+M')
        self.nmap.setStatusTip('NMap')
        self.nessus.setShortcut('Ctrl+N')
        self.nessus.setStatusTip('Nessus')
        self.exe.setShortcut('Ctrl+E')
        self.exe.setStatusTip('.exe')
        fileMenu = self.mainmenu.addMenu('&Fichier')
        fileMenu.addAction(self.extractAction)
        fileMenu.addAction(self.nmap)
        fileMenu.addAction(self.nessus)
        fileMenu.addAction(self.exe)


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