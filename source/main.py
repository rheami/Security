#!/user/bin/env python
# coding=utf-8
import sys
import os

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, SLOT

from diffFiles import diffFiles
from parseNMap.parseNmap import NMapScan
from parseNessus.parseNessus import Nessus


class MyDialog(QtGui.QDialog):
    def __init__(self, parent):
        super(QtGui.QDialog, self).__init__(parent)

        self.fname = ""
        self.fname2 = ""
        self.setWindowTitle('Scans a comparer')

        self.create_widgets()
        self.layout_widgets()
        self.create_connections()

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
        self.boutonannuler.clicked.connect(self.annuler)
        self.btnopenscan.clicked.connect(self.ouvririnterface)
        self.btnopenscan2.clicked.connect(self.ouvririnterface)
        self.boutoncomparer.clicked.connect(self.comparer)

    def comparer(self):

        if os.path.exists(self.fname) and os.path.exists(self.fname2):
            self.close()
        else:
            pass

    def annuler(self):
        self.close()

    def ouvririnterface(self):
        self.showDialog(self.parent().number)

    def showDialog(self, number):
        print("showDialog", self.sender())
        if number == 0:
            fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', './scanNMap')
        else:
            fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', './scanNessus')
        try:
            f = open(fname, 'r')
            if self.sender() is self.btnopenscan:
                self.fenetrescan1.append(str(fname))
                self.fname = fname
            else:
                self.fenetrescan2.append(str(fname))
                self.fname2 = fname
            f.close()
        except IOError as e:
            print(e)


class Form(QtGui.QWidget):

    def __init__(self):
        super(QtGui.QWidget, self).__init__()

        self.scan = None

        self.nmap_scan_fileA = ""
        self.nmap_scan_fileB = ""
        self.nmap_scan = None

        self.nessusfileA = ""
        self.nessusfileB = ""
        self.nessus_scan = None

        self.exe_scanA = "" # try here
        self.exe_scanB = ""
        self.exe_compare = None

        self.create_widgets()
        self.layout_widgets()
        self.create_connections()

        self.setFixedHeight(500)
        self.setFixedWidth(1200)
        self.setWindowTitle("ports ouverts nmap scan")

        self.number = -1

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

        self.buttonHachage = QtGui.QPushButton('Executables', self)
        self.buttonExe1 = QtGui.QPushButton('.exe 1')
        self.buttonExe2 = QtGui.QPushButton('.exe 2')
        self.buttonExeResult = QtGui.QPushButton('.exe resultat')

        self.image = QtGui.QLabel()
        self.imagepx = QtGui.QPixmap('./images/000Lock.png').scaled(180, 180)
        self.image.setPixmap(self.imagepx)

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
        self.btnnmap.clicked.connect(self.lancerNMap)
        self.btnnessus.clicked.connect(self.lancerNessus)
        self.buttonHachage.clicked.connect(self.lancerHachage)
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
        try:
            self.browser.clear()
        except AttributeError as e:
            pass
    # todo

    def showDiffHostNessus(self):
        try:
            self.scan = self.nessus_scan
            if self.scan is None:
                return
            self.showDiffHost()
            self.afficherImage(self.getMaxSeverity())
        except AttributeError as e:
            pass

    def showDiffHostNMap(self):
        try:
            self.scan = self.nmap_scan
            if self.scan is None:
                return
            self.showDiffHost()
        except AttributeError as e:
            pass

    def showDiffHost(self):
        try:
            self.browser.clear()
            self.showRemoved()
            self.showAdded()
            self.showChanged()
        except AttributeError as e:
            pass

    def showRemoved(self):
        self.browser.append("<h2>removed :</h2>")
        self.showList(self.scan.get_removed())

    def showAdded(self):
        self.browser.append("<h2>added :</h2>")
        self.showList(self.scan.get_added())

    def showChanged(self):
        self.browser.append("<h2>changed :</h2>")
        self.showList(self.scan.get_changed())

    # def showUnchanged(self):
    #     self.browser.append("<h2>unchanged :</h2>")
    #     self.showList(self.scan.get_unchanged())

    def showList(self, info_dict):
        for key in info_dict:
            self.browser.append("{0} : {1}".format(key, info_dict[key]))

    def showANmap(self):
        try:
            self.browser.clear()
            self.showList(self.nmap_scan.getInfoA())
        except AttributeError as e:
            pass

    def showBNmap(self):
        try:
            self.browser.clear()
            self.showList(self.nmap_scan.getInfoB())
        except AttributeError as e:
            pass

    def showANessus(self):
        try:
            self.browser.clear()
            self.showList(self.nessus_scan.getInfoA())
        except AttributeError as e:
            pass

    def showBNessus(self):
        try:
            self.browser.clear()
            self.showList(self.nessus_scan.getInfoB())
        except AttributeError as e:
            pass

    def lancerNessus(self):
        try:
            self.number = 1

            dialog = MyDialog(self)
            dialog.exec_()

            self.nessusfileA = dialog.fname
            self.nessusfileB = dialog.fname2

            self.scan = self.nessus_scan = Nessus(self.nessusfileA, self.nessusfileB)
            self.afficherImage(self.getMaxSeverity())
            self.showDiffHost()
        except AttributeError as e:
            print(e)

    def lancerHachage(self):
        pass

    def getMaxSeverity(self):
        try:
            return self.scan.getMaxSeverity()
        except AttributeError as e:
            print(e)

    def lancerNMap(self):
        try:
            self.number = 0

            dialog = MyDialog(self)
            dialog.exec_()

            self.nmap_scan_fileA = dialog.fname
            self.nmap_scan_fileB = dialog.fname2

            self.scan = self.nmap_scan = NMapScan(self.nmap_scan_fileA, self.nmap_scan_fileB)
            self.showDiffHost()
        except AttributeError as e:
            print(e)

# todo QPixmap erreur null
    def afficherImage(self, severity):
        if severity == 0:
            self.imagepx = QtGui.QPixmap('./images/greencheck2.png').scaled(180, 180)
            self.boiteresultats.setStyleSheet("""
            .QGroupBox {
                border: 1px solid black;
                color: green;
                border-radius: 2px;
                background-color: rgb(240, 247, 234);
                }
            """)
        elif severity == 1:
            self.imagepx = QtGui.QPixmap('./images/bluecheck.png').scaled(180, 180)
            self.boiteresultats.setStyleSheet("""
            .QGroupBox {
                border: 1px solid black;
                color: blue;
                border-radius: 2px;
                background-color: rgb(234, 239, 247);
                }
            """)
        elif severity == 2:
            self.imagepx = QtGui.QPixmap('./images/yellowcheck.png').scaled(180, 180)
            self.boiteresultats.setStyleSheet("""
            .QGroupBox {
                border: 1px solid black;
                color: rgb(190, 201, 118);
                border-radius: 2px;
                background-color: rgb(245, 247, 234);
                }
            """)
        elif severity == 3:
            self.imagepx = QtGui.QPixmap('./images/orangecheck.png').scaled(180, 180)
            self.boiteresultats.setStyleSheet("""
            .QGroupBox {
                border: 1px solid black;
                color: orange;
                border-radius: 2px;
                background-color: rgb(245, 237, 220);
                }
            """)
        else:
            self.imagepx = QtGui.QPixmap('./images/redcheck.png').scaled(180, 180)
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
        super(QtGui.QMainWindow, self).__init__()
        self.resize(950, 450)
        self.setWindowTitle('Detecteur de vulnerabilites')
        self.setWindowIcon(QtGui.QIcon('./images/logo.png'))  # todo
        self.createwidget()
        self.layoutwidget()
        self.createconnection()

    def createwidget(self):
        self.statusBar()
        self.mainmenu = self.menuBar()
        self.extractAction = QtGui.QAction('&Quitter', self)
        self.nmap = QtGui.QAction('&NMap', self)
        self.nessus = QtGui.QAction('&Nessus', self)
        self.exe = QtGui.QAction('&Executable', self)
        self.fenetre = Form()

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

    def closeEvent(self, event):
        self.close_application(event)

    def close_application(self, event):
        choice = QtGui.QMessageBox.question(self, 'Quitter',
                                            'Etes-vous certain de vouloir quitter?',
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if choice == QtGui.QMessageBox.No:
            event.ignore()


class AnalyseVuln(QtGui.QApplication):
    def __init__(self):
        QtGui.QApplication.__init__(self, sys.argv)

        self.connect(self, SIGNAL("lastWindowClosed()"), self, SLOT("quit()"))
        self.setApplicationName("Analyse de Vulnerabilite")

        self.main = Window()
        self.main.show()


if __name__ == "__main__":

    AnalyseVuln().exec_()
