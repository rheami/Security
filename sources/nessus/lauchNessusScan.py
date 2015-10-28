#!/usr/bin/python
import sys
sys.path.append('../')
from nessrest import ness6rest

import getpass
user = getpass._raw_input('User: ')
password = getpass.getpass()

# Logins
scan = ness6rest.Scanner(url="https://127.0.0.1:8834",login=user,password=password, insecure=True)
#scan = ness6rest.Scanner(url="https://nessusscanner:8834", login="username", password="password")

#creds = [credentials.WindowsPassword(username="administrator", password="foobar"),
#         credentials.WindowsPassword(username="administrator", password="barfoo"),
#         credentials.SshPassword(username="nessususer", password="foobar")]

#scan.policy_add_creds(credentials=creds)

# Build policies
#scan.upload(upload_file="file.audit")
#scan._policy_add_audit(category="Windows", filename="file.audit")
scan.policy_add(name="basic", plugins="21156")

#Launch scans
scan.scan_add(targets="192.168.0.101", name="firstscan")
#scan.scan_add(targets="192.168.0.101", name="web")
scan.scan_run()