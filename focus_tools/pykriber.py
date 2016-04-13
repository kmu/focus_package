#!/usr/bin/env python

import os
import sys
import shutil

import subprocess as sp
from subprocess import PIPE, STDOUT

drc = os.path.abspath(os.path.dirname( __file__ )) # get path of program


def clean():
    files = ["symdat", "distdat", "coseq"]
    for f in files:
        if os.path.exists(f):
            os.remove(f)


def setup():
    files = ["symdat", "distdat", "coseq"]
    for f in files:

        src = os.path.join(drc, "..", "resources", f)
        target = os.path.join(os.path.abspath("."), f)

        shutil.copyfile(src, target)


def prepare():
    kriber_exe = os.path.join(drc, "..", "bin", "kriber.x")

    clean()
    setup()

    assert os.path.exists(kriber_exe)
    files = ["symdat", "distdat", "coseq"]
    for f in files:
        assert os.path.exists(f)

    return kriber_exe


def move(fname, target):
    if os.path.exists(target):
        os.remove(target)
    os.rename(fname, target)


def extract_all_keys_from_strudat():
    keys = []
    strudat = open("strudat", "r")

    for line in strudat:
        if line.startswith("*"):
            keys.append(line.strip()[1:])
    return keys


def strudat2cif(args=[], keys=[], rename=True, verbose=True):
    from subprocess import PIPE, STDOUT
    
    if isinstance(keys, str):
        keys = keys.split()

    kriber_exe = prepare()
    
    if not keys:
        keys = extract_all_keys_from_strudat()
    
    for key in keys:
        p = sp.Popen(['kriber', 'reacs'] + args + ['wricif', 'exit'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        out = p.communicate(input=key)

        if out[0]:
            for line in out[0].split("\n"):
                if "ERROR" in line:
                    raise RuntimeError("{}  ->  KRIBER {}".format(key, line))
        if out[1]:
            print out[1]

        move("structure.cif", key+".cif")
        if verbose:
            print " >> Wrote file {}".format(key+".cif")

    clean()


def strudat2dls(args=[], keys=[], verbose=True):
    from subprocess import PIPE, STDOUT
    
    if isinstance(keys, str):
        keys = keys.split()

    kriber_exe = prepare()
    
    if not keys:
        keys = extract_all_keys_from_strudat()

    for key in keys:
        p = sp.Popen(['kriber', 'reacs'] + args + ['wriid', 'exit'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        out = p.communicate(input=key)

        if out[0]:
            for line in out[0].split("\n"):
                if "ERROR" in line:
                    raise RuntimeError("{}  ->  KRIBER {}".format(key, line))
        if out[1]:
            print out[1]

        # move("structure.cif", key+".cif")
        # print " >> Wrote file {}".format(key+".cif")

    clean()


def kriber(args=[]):
    kriber_exe = prepare()
    sp.call([kriber_exe] + args)
    clean()


def strudat2cif_entry():
    strudat2cif(args=sys.argv[1:])


def strudat2cif_entry():
    strudat2cif(keys=sys.argv[1:])


def kriber_entry():
    kriber(args=sys.argv[1:]) 


if __name__ == '__main__':
    run_kriber()
    # strudat2cif()