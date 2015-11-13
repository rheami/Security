#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from math import *
import sys
from PyQt4.QtGui import (QApplication, QDialog, QTextBrowser, QVBoxLayout, QPushButton, QHBoxLayout)
from parseNmap import NMapScan

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        scanap_scan_file="./scans/scan-origin.xml"
        scanap_scan_file2="./scans/scan-212247-101415.xml"
        self.scan = NMapScan(scanap_scan_file, scanap_scan_file2)

        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        self.setFixedHeight(600)
        self.setFixedWidth(800)
        self.setWindowTitle("ports ouverts nmap scan")

    def create_widgets(self):
        self.browser = QTextBrowser()
        self.buttonA = QPushButton("show A")
        self.buttonB = QPushButton("show B")
        self.buttonDiffHost = QPushButton("Show diff")

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
        self.browser.append("removed : {0}:".format(self.scan.get_removed()))
        self.browser.append("added : {0} ".format(self.scan.get_added()))
        self.browser.append("changed : {0}".format(self.scan.get_changed()))
        self.browser.append("unchanged : {0}".format(self.scan.get_unchanged()))

    def showA(self):
        self.browser.clear()
        infoList = self.scan.getInfoA()
        for key in infoList:
            self.browser.append("{0} : {1}".format(key, infoList[key]))

    def showB(self):
        self.browser.clear()
        infoList = self.scan.getInfoB()
        for key in infoList:
            self.browser.append("{0} : {1}".format(key, infoList[key]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()