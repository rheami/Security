#!/usr/bin/env python
import os
from libnessus.parser import NessusParser

import glob
import argparse

from datetime import datetime

fdir = os.path.dirname(os.path.realpath(__file__))

# parse args
parser = argparse.ArgumentParser(
    description='This script parse .nessus file (XML)..')
parser.add_argument('--filename',
                    default="./xp_27.nessus",
                    help="path to a nessusV2 xml")
args = parser.parse_args()

nessusfile = args.filename

def dumpclean(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print (k)
                dumpclean(v)
            else:
                print ('%s : %s' % (k, v))
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v)
            else:
                print (v)
    else:
        print (obj)

print("file to parse: %s" % nessusfile)

try:
    nrp = NessusParser.parse_fromfile(nessusfile)
except:
    print("file cannot be imported : %s" % nessusfile)

for host in nrp.hosts:
    #print ("Information du serveur :")
    #dumpclean(host.get_host_properties)
    print ("Vulnerabilite trouvees :")
    VulnList = host.get_report_items
    for report_item in VulnList: 
        print (report_item.port, report_item.protocol, report_item.service)
        print (report_item.plugin_id, report_item.plugin_name)
        print (report_item.get_vuln_xref)
        print (report_item.get_vuln_info)
        print (report_item.get_vuln_risk)
        print (report_item.description)
        

