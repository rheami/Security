import sys
from PyQt4 import QtGui, QtCore
import subprocess

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

        btnquitter = QtGui.QPushButton('Quitter', self)
        btnquitter.setToolTip('Quitter')
        btnquitter.clicked.connect(self.close_application)
        btnquitter.resize(btnquitter.sizeHint())
        btnquitter.move(50, 350)

        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(150, 415, 650, 20)

        self.btnlancer = QtGui.QPushButton('Lancer la recherche de vulnerabilites', self)
        self.btnlancer.setToolTip('Lancer la recherche')
        self.btnlancer.move(50, 50)
        self.btnlancer.resize(200, 100)
        self.btnlancer.clicked.connect(self.download)

        self.styleChoice = QtGui.QLabel('Windows Vista', self)

        menuDeroulant = QtGui.QComboBox(self)
        menuDeroulant.addItem('motif')
        menuDeroulant.addItem('Windows')
        menuDeroulant.addItem('cde')
        menuDeroulant.addItem('Plastique')
        menuDeroulant.addItem('Cleanlooks')
        menuDeroulant.addItem('windowsvista')

        menuDeroulant.move(50, 250)
        self.styleChoice.move(50, 250)
        menuDeroulant.activated[str].connect(self.style_choice)

        self.show()

    def style_choice(self, text):
        self.styleChoice.setText(text)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(text))

    def download(self):
        self.completed = 0

        while self.completed < 100:
            self.completed += 0.0005
            self.progress.setValue(self.completed)

        self.lancerNMap()

    def lancerNMap(self):
        self.btnlancer.clicked.connect(lambda:self.run('C:\Users\Caroline\Desktop\Caro\s-curit-inm5001\s-curit-inm5001\sources\compareScan.py'))

    def run(self, path):
        scan1 = 'C:\Users\Caroline\Desktop\Caro\s-curit-inm5001\s-curit-inm5001\sources\scan-115007-102615.xml'
        scan2 = 'C:\Users\Caroline\Desktop\Caro\s-curit-inm5001\s-curit-inm5001\sources\scan-144848-101915.xml'
        subprocess.call(['pythonw', path, scan1, scan2])

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

