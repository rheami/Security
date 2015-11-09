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
from libnessus.parser import NessusParser
from libnessus.objects.dictdiffer import DictDiffer

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.nessusfile = "./xp_27.nessus"
        self.nessusfileB = "./xp_27.nessus"
        self.nessus_rapportA = NessusParser.parse_fromfile(self.nessusfile)
        self.nessus_rapportB = NessusParser.parse_fromfile(self.nessusfileB)

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
        self.buttonDiff = QPushButton("Show diff")

    def layout_widgets(self):
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.buttonA)
        buttonLayout.addWidget(self.buttonB)
        buttonLayout.addWidget(self.buttonDiff)
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def create_connections(self):
        self.buttonA.clicked.connect(self.showA)
        self.buttonB.clicked.connect(self.showB)
        self.buttonDiff.clicked.connect(self.showDiff)

    def showDiff(self):
        self.browser.clear()
        a = {'a': 1, 'b': 1, 'c': 0}
        b = {'a': 1, 'b': 2, 'd': 0}
        self.d = DictDiffer(b, a)
        self.diff = DictDiffer(b, a)
        self.browser.append("added : <b>{0}</b> ".format(self.diff.added()))
        self.browser.append("removed : <b>{0}</b> ".format(self.diff.removed()))
        self.browser.append("changed : <b>{0}</b> ".format(self.diff.changed()))


    def showB(self):
        self.browser.clear()
        # for host in nrp.hosts: # si plusieurs hosts
        host = self.nessus_rapportB.hosts[0]
        vulnList = host.get_report_items
        for report_item in vulnList:
            self.browser.append("port {0} : <b>{1}</b> <b> service {2}</b><b>severity {3}</b> ".format(report_item.port, report_item.protocol, report_item.service, report_item.severity))
            if report_item.severity != "0":
                self.browser.append("{0} = <b>{1}</b>".format("risk", report_item.get_vuln_risk))

    def showA(self):
        self.browser.clear()
        # for host in nrp.hosts: # si plusieurs hosts
        host = self.nessus_rapportA.hosts[0]
        vulnList = host.get_report_items
        for report_item in vulnList:
            self.browser.append("port {0} : <b>{1}</b> <b> service {2}</b><b>severity {3}</b> ".format(report_item.port, report_item.protocol, report_item.service, report_item.severity))
            if report_item.severity != "0":
                self.browser.append("{0} = <b>{1}</b>".format("risk", report_item.get_vuln_risk))

"""
        afficher les details sur selection de une vulnerabilite seulement et dans une autre vue
            self.browser.append("{0} = <b>{1}</b>".format(report_item.plugin_id, report_item.plugin_name))
            self.browser.append("{0} = <b>{1}</b>".format("xref", report_item.get_vuln_xref))
            self.browser.append("{0} = <b>{1}</b>".format("info", report_item.get_vuln_info))
            self.browser.append("{0} = <b>{1}</b>".format("description", report_item.get_vuln_description))
"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()
