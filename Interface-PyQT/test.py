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

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.firstscan = "./xp_27.nessus"
        self.secondscan = "./xp_27B.nessus"
        self.ne = Nessus(self.firstscan, self.secondscan)
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        self.setFixedHeight(600)
        self.setFixedWidth(800)
        self.setWindowTitle("Vunerabilite trouvees par Nessus")

    def create_widgets(self):
        self.browser = QTextBrowser()
        self.buttonA = QPushButton("show A")
        self.buttonB = QPushButton("show B")
        self.buttonDiff = QPushButton("Show diff test")
        self.buttonDiffHost = QPushButton("Show diff host")

    def layout_widgets(self):
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.buttonA)
        buttonLayout.addWidget(self.buttonB)
        buttonLayout.addWidget(self.buttonDiff)
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
        diffHost = self.ne.get_diff()
        self.browser.append("added : {0}".format(diffHost['added']))
        self.browser.append("removed : {0}".format(diffHost['removed']))
        self.browser.append("changed : {0}".format(diffHost['changed']))

    def showB(self):
        self.browser.clear()
        # for host in nrp.hosts: # si plusieurs hosts
        host = self.nessus_rapportB.hosts[0]
        vulnList = host.get_report_items
        for report_item in vulnList:
            self.browser.append("port {0} : <b>{1}</b> <b> service {2} </b><b>severity {3}</b> ".format(report_item.port, report_item.protocol, report_item.service, report_item.severity))
            if report_item.severity != "0":
                self.browser.append("{0} = <b>{1}</b>".format("risk", report_item.get_vuln_risk))

    def showA(self):
        self.browser.clear()
        # for host in nrp.hosts: # si plusieurs hosts
        host = self.nessus_rapportA.hosts[0]
        vulnList = host.get_report_items
        for vuln in vulnList:
            self.browser.append("port {0} : <b>{1}</b> <b> service {2} </b><b>severity {3}</b> ".format(vuln.port, vuln.protocol, vuln.service, vuln.severity))
            if vuln.severity != "0":
                self.browser.append("{0} = <b>{1}</b>".format("risk", vuln.get_vuln_risk))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()