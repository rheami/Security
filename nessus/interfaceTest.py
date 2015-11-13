#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *
import os
import sys
from math import *
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal as Signal
from PyQt4.QtGui import (QApplication, QDialog, QTextBrowser, QVBoxLayout, QPushButton, QHBoxLayout)
from parseNessus import Nessus

# todo not usable now : try to adapt to new parseNessus.py when fininished

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        nessusfile = "./scan/xp_27.nessus"
        nessusfileB = "./scan/xp_27B.nessus"
        self.ne = Nessus(nessusfile, nessusfileB)

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
        self.browser.append("removed : {0}:".format(self.ne.get_removed()))
        self.browser.append("added : {0} ".format(self.ne.get_added()))
        self.browser.append("changed : {0}".format(self.ne.get_changed()))
        self.browser.append("unchanged : {0}".format(self.ne.get_unchanged()))

    def showA(self):
        self.browser.clear()
        vulnList = self.ne.get_VulnsA()
        for item in vulnList:
            self.browser.append(item)

    def showB(self):
        self.browser.clear()
        vulnList = self.ne.get_VulnsB()
        for item in vulnList:
            self.browser.append(item)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()