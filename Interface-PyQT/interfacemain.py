import sys
from PyQt4 import QtGui, QtCore

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

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&Fichier')
        fileMenu.addAction(extractAction)



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

        self.styleChoice = QtGui.QLabel('Windows', self)


        self.show()


    def download(self):
        self.completed = 0

        while self.completed < 100:
            self.completed += 0.0005
            self.progress.setValue(self.completed)

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

