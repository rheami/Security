#!/user/bin/env python
# coding=utf-8
import sys
import os

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, SLOT
from diff_user.user_generator import generateur
from diff_user.diff_user2 import Diff_user2
from parseNMap.parseNmap import NMapScan
from parseNessus.parseNessus import Nessus
from diffFiles.diffFiles import DiffFiles


class MyDialog(QtGui.QDialog):
    def __init__(self, parent, default_dir="."):
        super(QtGui.QDialog, self).__init__(parent)

        self.fname = ""
        self.fname2 = ""
        self.default_dir = default_dir

        self.sentby = parent.sender().text()

        self.setWindowTitle(u'rapport(dossier) à comparer')
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()

    def create_widgets(self):
        self.btnopenscan = QtGui.QPushButton('choisir rapport original')
        self.fenetrescan1 = QtGui.QTextEdit(self)
        self.btnopenscan2 = QtGui.QPushButton('choisir rapport nouveau')
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

        if self.sentby == 'NMap':
            self.showDialog()

        if self.sentby == 'Nessus':
            self.showDialog()

        if self.sentby == 'Executables':
            self.showOpenFolderDialog()

    def showDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', self.default_dir)

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

    def showOpenFolderDialog(self):
        dir = QtGui.QFileDialog.getExistingDirectory(self, 'Select Directory', self.default_dir)

        try:
            if self.sender() is self.btnopenscan:
                self.fenetrescan1.append(str(dir))
                self.fname = str(dir) + "/"
            else:
                self.fenetrescan2.append(str(dir))
                self.fname2 = str(dir) + "/"
        except IOError as e:
            pass



class Form(QtGui.QWidget):

    def __init__(self):
        super(QtGui.QWidget, self).__init__()

        self.diff_type = None

        self.nmap_report = None

        self.nessus_report = None

        self.hash_report = None

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
        self.btnuser = QtGui.QPushButton('Utilisateurs', self)

        self.btnnessus = QtGui.QPushButton('Nessus', self)

        self.buttonHachage = QtGui.QPushButton('Executables', self)
        self.buttonAHachage = QtGui.QPushButton('.exe 1')
        self.buttonBHachage = QtGui.QPushButton('.exe 2')
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
        buttonLayout.addWidget(self.buttonAHachage)
        buttonLayout.addWidget(self.buttonBHachage)
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
        gauche.addWidget(self.btnuser)
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
        self.buttonDiffHostnmap.clicked.connect(self.show_diff_nmap)

        self.buttonAnessus.clicked.connect(self.showANessus)
        self.buttonBnessus.clicked.connect(self.showBNessus)
        self.buttonDiffHostnessus.clicked.connect(self.show_diff_nessus)

        self.btnnmap.clicked.connect(self.lancerNMap)
        self.btnnessus.clicked.connect(self.lancerNessus)
        self.buttonHachage.clicked.connect(self.lancerHachage)
        self.btnuser.clicked.connect(self.show_user)

        self.buttonAHachage.clicked.connect(self.showA_hash)
        self.buttonBHachage.clicked.connect(self.showB_hash)
        self.buttonExeResult.clicked.connect(self.show_diff_hash)

    def exe1(self):
        self.browser.clear()
    # todo

    def exe2(self):
        self.browser.clear()
    # todo

    def show_diff_hash(self):
        try:
            self.diff_type = self.hash_report
            if self.diff_type is None:
                return
            self.show_diff()
            severity = self.getIndiceOfChange()
            self.afficherImage(severity)
        except AttributeError as e:
            pass

    def show_diff_user(self):
        try:
            self.diff_type = self.user_report
            if self.diff_type is None:
                return
            self.show_diff()
            severity = self.getIndiceOfChange()
            self.afficherImage(severity)
        except AttributeError as e:
            pass

    def show_diff_nessus(self):
        try:
            self.diff_type = self.nessus_report
            if self.diff_type is None:
                return
            self.show_diff()
            severity = int(self.getMaxSeverity())
            self.afficherImage(severity)
        except AttributeError as e:
            pass

    def show_diff_nmap(self):
        try:
            self.diff_type = self.nmap_report
            if self.diff_type is None:
                return
            self.show_diff()
            severity = self.getIndiceOfChange()
            self.afficherImage(severity)
        except AttributeError as e:
            pass

    def getIndiceOfChange(self):
        severity = len(self.diff_type.get_removed()) + len(self.diff_type.get_changed()) + len(self.diff_type.get_added())
        return severity

    def show_diff(self):
        try:
            self.browser.clear()
            self.showRemoved()
            self.showAdded()
            self.showChanged()
        except AttributeError as e:
            pass

    def showRemoved(self):
        self.browser.append("<h2>removed :</h2>")
        self.showList(self.diff_type.get_removed())

    def showAdded(self):
        self.browser.append("<h2>added :</h2>")
        self.showList(self.diff_type.get_added())

    def showChanged(self):
        self.browser.append("<h2>changed :</h2>")
        self.showList(self.diff_type.get_changed())

    def showList(self, info_dict):
        for key in info_dict:
            self.browser.append("{0} : {1}".format(key, info_dict[key]))

    def showANmap(self):
        try:
            self.browser.clear()
            self.showList(self.nmap_report.getInfoA())
        except AttributeError as e:
            pass

    def showBNmap(self):
        try:
            self.browser.clear()
            self.showList(self.nmap_report.getInfoB())
        except AttributeError as e:
            pass

    def showANessus(self):
        try:
            self.browser.clear()
            self.showList(self.nessus_report.getInfoA())
        except AttributeError as e:
            pass

    def showBNessus(self):
        try:
            self.browser.clear()
            self.showList(self.nessus_report.getInfoB())
        except AttributeError as e:
            pass

    def showA_hash(self):
        try:
            self.browser.clear()
            self.showList(self.hash_report.getInfoA())
        except AttributeError as e:
            pass

    def showB_hash(self):
        try:
            self.browser.clear()
            self.showList(self.hash_report.getInfoB())
        except AttributeError as e:
            pass

    def getMaxSeverity(self):
        try:
            return self.diff_type.getMaxSeverity()
        except AttributeError as e:
            print(e)

    def lancerNessus(self):
        try:
            start_dir = "./scanNessus"

            dialog = MyDialog(self, start_dir)
            dialog.exec_()

            self.nessusfileA = dialog.fname
            self.nessusfileB = dialog.fname2

            self.diff_type = self.nessus_report = Nessus(self.nessusfileA, self.nessusfileB)
            self.show_diff_nessus()
        except AttributeError as e:
            print(e)

    def show_user(self):
        try:
            start_dir = "./source"

            generateur()
            dialog = MyDialog(self, start_dir)
            dialog.exec_()
            userA = dialog.fname
            userB = dialog.fname2

            self.diff_type =self.user_report= Diff_user2(userA,userB)
            self.show_diff_user()
        except AttributeError as e:
            print(e)

    def lancerHachage(self):
        try:
            start_dir = "./diffFiles"

            dialog = MyDialog(self, start_dir)
            dialog.exec_()

            exe_scanA = dialog.fname
            exe_scanB = dialog.fname2

            self.diff_type = self.hash_report = DiffFiles(exe_scanA, exe_scanB)
            self.show_diff_hash()

        except AttributeError as e:
            print(e)

    def lancerNMap(self):
        try:
            start_dir = "./scanNMap"

            dialog = MyDialog(self, start_dir)
            dialog.exec_()

            self.nmap_scan_fileA = dialog.fname
            self.nmap_scan_fileB = dialog.fname2

            self.diff_type = self.nmap_report = NMapScan(self.nmap_scan_fileA, self.nmap_scan_fileB)
            self.show_diff_nmap()
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
