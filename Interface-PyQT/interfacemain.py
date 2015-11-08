import sys
from PyQt4 import QtGui, QtCore
import subprocess
import compareScan2

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

        win = QtGui.QAction('&Windows', self)
        win.setStatusTip('Changement de style vers Windows')
        win.triggered.connect(self.style_choice)

        plastique = QtGui.QAction('&Plastique', self)
        plastique.setStatusTip('Changement de style vers Plastique')
        plastique.triggered.connect(self.style_choice)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&Fichier')
        fileMenu.addAction(extractAction)
        styleMenu = mainMenu.addMenu('&Style')
        styleMenu.addAction(win)
        styleMenu.addAction(plastique)


        self.home()

    def home(self):

        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(50, 380, 233, 15)

        self.btnlancer = QtGui.QPushButton('Lancer la recherche de vulnerabilites', self)
        self.btnlancer.setToolTip('Lancer la recherche')
        self.btnlancer.move(50, 50)
        self.btnlancer.resize(200, 270)
        self.btnlancer.clicked.connect(self.download)

        self.styleChoice = QtGui.QLabel('Windows Vista', self)

        menuDeroulant = QtGui.QComboBox(self)
        menuDeroulant.addItem('motif')
        menuDeroulant.addItem('Windows')
        menuDeroulant.addItem('cde')
        menuDeroulant.addItem('Plastique')
        menuDeroulant.addItem('Cleanlooks')
        menuDeroulant.addItem('windowsvista')

        menuDeroulant.move(450, 250)
        self.styleChoice.move(450, 250)
        menuDeroulant.activated[str].connect(self.style_choice)

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
        fichier = open('try1.txt', 'r')
        fichier.read()
        fichier.close()

        text=open('try1.txt').read()

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

