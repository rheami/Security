import sys
from PyQt4 import QtGui, QtCore
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

        self.btnlancer = QtGui.QPushButton('Lancer la recherche de vulnerabilites', self)
        self.extractAction = QtGui.QAction('&Quitter', self)
        self.boitetexte = QtGui.QTextEdit(self)

    def layoutwidget(self):
        self.extractAction.setShortcut('Ctrl+Q')
        self.extractAction.setStatusTip('Fermeture')
        fileMenu = self.mainmenu.addMenu('&Fichier')
        fileMenu.addAction(self.extractAction)

        self.progress.setGeometry(50, 380, 200, 15)

        self.btnlancer.setToolTip('Lancer la recherche')
        self.btnlancer.move(50, 50)
        self.btnlancer.resize(200, 270)
        self.btnlancer.setStatusTip('Recherche de vulnerabilites')

        self.boitetexte.setGeometry(QtCore.QRect(330, 50, 270, 350))
        self.boitetexte.setObjectName("Resultats NMap")

    def createconnection(self):
        self.extractAction.triggered.connect(self.close_application)
        self.btnlancer.clicked.connect(self.download)

    def download(self):
        completed = 0

        while completed < 100:
            completed += 0.00015
            self.progress.setValue(completed)

        self.lancerNMap()

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

