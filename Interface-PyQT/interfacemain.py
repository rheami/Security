import sys
from PyQt4 import QtGui, QtCore
import subprocess
import compareScan2
import pickle

class Window(QtGui.QMainWindow):

    def closeEvent(self, event):
        event.ignore()
        self.close_application()

    def __init__(self):
        super(Window, self).__init__()
        self.resize(950, 450)
        self.setWindowTitle('Detecteur de vulnerabilites')
        self.setWindowIcon(QtGui.QIcon('logo.png'))

        extractAction = QtGui.QAction('&Quitter', self)
        extractAction.setShortcut('Ctrl+Q')
        extractAction.setStatusTip('Fermeture')
        extractAction.triggered.connect(self.close_application)

        self.styleChoice = QtGui.QLabel('Plastique', self)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&Fichier')
        fileMenu.addAction(extractAction)

        self.home()

    def home(self):

        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(50, 380, 200, 15)

        self.btnlancer = QtGui.QPushButton('Lancer la recherche de vulnerabilites', self)
        self.btnlancer.setToolTip('Lancer la recherche')
        self.btnlancer.move(50, 50)
        self.btnlancer.resize(200, 270)
        self.btnlancer.setStatusTip('Recherche de vulnerabilites')
        self.btnlancer.clicked.connect(self.download)

        self.style_choice('plastique')

        self.boitetexte = QtGui.QTextEdit(self)
        self.boitetexte.setGeometry(QtCore.QRect(330, 50, 270, 350))
        self.boitetexte.setObjectName("Resultats NMap")

        self.show()

    def style_choice(self, text):
        self.styleChoice.setText(text)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(text))

    def download(self):
        self.completed = 0

        while self.completed < 100:
            self.completed += 0.00015
            self.progress.setValue(self.completed)

        self.lancerNMap()

    def lancerNMap(self):
        compareScan2.main('scan-115007-102615.xml', 'scan-144848-101915.xml')

        text = open('resultatsnmap.txt').read()
        self.boitetexte.setPlainText(text)


    def close_application(self):
        choice = QtGui.QMessageBox.question(self, 'Quitter',
                                            'Etes-vous certain de vouloir quitter?',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print('Fin normale du programme')
            sys.exit()
        else:
            pass


def main():

    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

main()

