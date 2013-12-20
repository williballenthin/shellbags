#!/usr/bin/python

import os
import sys

from Registry import Registry

# from http://stackoverflow.com/a/9806045/87207
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentparentdir = os.path.dirname(parentdir)
sys.path.append(parentparentdir)
from ShellItems import SHITEMLIST
sys.path.pop()


def test(filename):
    r = Registry.Registry(filename)
    k = r.open("Local Settings\\Software\\Microsoft\\Windows\\Shell\\BagMRU\\1\\0\\0")
    v = k.value("0")

    l = SHITEMLIST(v.value(), 0, False)
    for item in l.items():
        print item.name()


def main():
    import sys
    hive = sys.argv[1]

    import hashlib
    m = hashlib.md5()
    with open(hive, 'rb') as f:
        m.update(f.read())
    if m.hexdigest() != "a83c09811f508399e1a23f674897da69":
        print "Please use the UsrClass hive with MD5 a83c09811f508399e1a23f674897da69"
        sys.exit(-1)

    test(hive)


if __name__ == "__main__":
    main()
