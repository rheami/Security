#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
from __future__ import absolute_import

import argparse
import sys
from libnmap.parser import NmapParser

class NMapScan(object):
    def __init__(self, fileA, fileB):

        try:
            scan_a = NmapParser.parse_fromfile(fileA)
            scan_b = NmapParser.parse_fromfile(fileB)
        except IOError as e:
            print((sys.stderr, u"Can't open file: %s" % str(e)))
            sys.exit(EXIT_ERROR)

        self.host_a = scan_a.hosts[0]
        self.host_b = scan_b.hosts[0]

        self.diff = self.host_a.diff(self.host_b)

    def getInfoA(self):
        services = self.host_a.services
        return self.get_services_info(services)

    def getInfoB(self):
        services = self.host_b.services
        return self.get_services_info(services)

    def get_services_info(self, services):
        return {x.port: "protocol= {}, service= {}, state= {}".format(
                x.protocol,
                x.service,
                x.state
                ) for x in services}

    def get_service_info_by_id(self, service_id, host):
        x = host.get_service_byid(service_id)
        s = "{}".format(x.port), \
            " protocol= {}, service= {}, state= {}".format(
            x.port,
            x.protocol,
            x.service,
            x.state
        )
        return s

    def get_added(self):
        services = self.host_b.services
        added = self.get_diff_added(self.host_a, self.host_b, self.diff.added())
        return added

    def get_removed(self):
        services = self.host_b.services
        removed = self.get_diff_removed(self.host_a, self.host_b, self.diff.removed())
        return removed

    def get_changed(self):
        changed = self.get_diff_changed(self.host_a, self.host_b, self.diff.changed())
        return changed

    def get_diff_added(self, obj1, obj2, added):
        infolist = {}
        for akey in added:
            nested = nested_obj(akey)
            if nested is not None:
                if nested[0] == 'NmapService':
                    s = self.get_service_info_by_id(nested[1], obj1)
                    infolist[s[0]] = s[1]
        return infolist

    def get_diff_removed(self, obj1, obj2, removed):
        infolist = {}
        for rkey in removed:
            nested = nested_obj(rkey)
            if nested is not None:
                if nested[0] == 'NmapService':
                    s = self.get_service_info_by_id(nested[1], obj2)
                    infolist[s[0]] = s[1]
        return infolist

    def get_diff_changed(self, obj1, obj2, changes):
        infolist = {}
        for mkey in changes:
            nested = nested_obj(mkey)
            if nested is not None:
                if nested[0] == 'NmapService':
                    subobj1 = obj1.get_service_byid(nested[1])
                    subobj2 = obj2.get_service_byid(nested[1])
                    infolist = self.get_subchanged(subobj1, subobj2)
            else:
                s = "protocol= {}, service= {}, state= {}".format(
                    obj1.protocol,
                    obj1.service,
                    obj1.state)
                infolist[obj1.port] = "{} <h4> change : {}: {} => {} </h4>".format(s, mkey,
                                                     getattr(obj2, mkey),
                                                     getattr(obj1, mkey))
        return infolist

    def get_subchanged(self, obj1, obj2):
        ndiff = obj1.diff(obj2)
        subchanged = self.get_diff_changed(obj1, obj2, ndiff.changed())
        return subchanged


def nested_obj(objname):
    rval = None
    splitted = objname.split("::")
    if len(splitted) == 2:
        rval = splitted
    return rval


EXIT_EQUAL = 0
EXIT_DIFFERENT = 1
EXIT_ERROR = 2


def usage_error(msg):
    print(u"%s: %s" % (sys.argv[0], msg), file=sys.stderr)
    sys.exit(EXIT_ERROR)


def main():

 # parse args
    parser = argparse.ArgumentParser(
    description='This script parse nmap scan file (XML)..')
    parser.add_argument('--firstscan',
                    default="./scans/scanXP-150419-102915.xml",
                    help="path to a nmap xml")
    parser.add_argument('--secondscan',
                    default="./scans/scanXP-modified.xml",
                    help="path to a nmap xml")
    args = parser.parse_args()

    nm = NMapScan(args.firstscan, args.secondscan)
    print("infoa", nm.getInfoA())
    print("infob", nm.getInfoB())
    print("changed : ", nm.get_changed())
    print("added : ", nm.get_added())
    print("removed : ", nm.get_removed())

    return


# Catch uncaught exceptions so they can produce an exit code of 2 (EXIT_ERROR),
# not 1 like they would by default.
def excepthook(type, value, tb):
    sys.__excepthook__(type, value, tb)
    sys.exit(EXIT_ERROR)

if __name__ == "__main__":
    sys.excepthook = excepthook
    sys.exit(main())