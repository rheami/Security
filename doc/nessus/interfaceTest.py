#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from math import *
import sys
from PyQt4.QtGui import (QApplication, QDialog, QTextBrowser, QVBoxLayout, QPushButton, QHBoxLayout)
from parseNessus import Nessus

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        nessusfileB = "./RapportsNessus/rapport-1_c9lthb.nessus"
        nessusfileA = "./RapportsNessus/rapport-3_gdjv7m.nessus"
        self.scan = Nessus(nessusfileA, nessusfileB)

        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        self.setFixedHeight(600)
        self.setFixedWidth(800)
        self.setWindowTitle("Vulnerabilite trouvees par Nessus")

    def create_widgets(self):
        self.browser = QTextBrowser()
        self.buttonA = QPushButton("show A")
        self.buttonB = QPushButton("show B")
        self.buttonDiffHost = QPushButton("Show diff host")

    def layout_widgets(self):
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.buttonA)
        buttonLayout.addWidget(self.buttonB)
        buttonLayout.addWidget(self.buttonDiffHost)
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def create_connections(self):
        self.buttonA.clicked.connect(self.showA)
        self.buttonB.clicked.connect(self.showB)
        self.buttonDiffHost.clicked.connect(self.showDiffHost)

    def showDiffHost(self):
        self.browser.clear()
        self.showRemoved()
        self.showAdded()
        self.showChanged()
        self.showUnchanged()

    def showList(self, info_dict):
            for key in info_dict:
                 self.browser.append("{0} : {1}".format(key, info_dict[key]))

    def showRemoved(self):
        self.browser.append("<h2>removed :</h2>")
        self.showList(self.scan.get_removed())

    def showAdded(self):
        self.browser.append("<h2>added :</h2>")
        self.showList(self.scan.get_added())

    def showChanged(self):
        self.browser.append("<h2>changed :</h2>")
        i = len(self.scan.get_added())
        severity = self.scan.getMaxSeverity()
        self.browser.append("<h2>added = {}</h2>".format(i))
        self.showList(self.scan.get_changed())
        self.browser.append("<h2>max = {}</h2>".format(severity))

    def showUnchanged(self):
        self.browser.append("<h2>unchanged :</h2>")
        self.showList(self.scan.get_unchanged())

    def showA(self):
        self.browser.clear()
        self.showList(self.scan.getInfoA())

    def showB(self):
        self.browser.clear()
        self.showList(self.scan.getInfoB())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()