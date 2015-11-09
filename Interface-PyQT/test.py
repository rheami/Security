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
from PyQt4.QtGui import (QApplication, QDialog, QTextBrowser, QVBoxLayout, QPushButton)
from libnessus.parser import NessusParser


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.nessusfile = "./xp_27.nessus"
        self.nessus_rapport = NessusParser.parse_fromfile(self.nessusfile)
        self.create_widgets()
        self.layout_widgets()
        self.create_connections()
        self.setWindowTitle("Vunerabilite trouvees par Nessus")

    def create_widgets(self):
        self.browser = QTextBrowser()
        self.nessusButton = QPushButton("Parse &Nessus file")

    def layout_widgets(self):
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.nessusButton)
        self.setLayout(layout)

    def create_connections(self):
        self.nessusButton.clicked.connect(self.updateUi)

    def updateUi(self):
        # for host in nrp.hosts: # si plusieurs hosts
        host = self.nessus_rapport.hosts[0]
        vulnList = host.get_report_items
        for report_item in vulnList:
            self.browser.append("port {0} : <b>{1}</b> <b> service {2}</b><b>severity {3}</b> ".format(report_item.port, report_item.protocol, report_item.service, report_item.severity))
            if report_item.severity != "0":
                self.browser.append("{0} = <b>{1}</b>".format("risk", report_item.get_vuln_risk))

"""         afficher les details sur selection de une vulnerabilite seulement et dans une autre vue
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
