__author__ = 'michel'

import ness6rest
import credentials

scan = ness6rest.Scanner(url="https://127.0.0.1:8834", login="michel", password="HdN1tsxqF9FH", insecure=True)
creds = [credentials.WindowsPassword(username="administrator", password="foobar")