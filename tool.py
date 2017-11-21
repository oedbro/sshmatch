#!/usr/bin/python3

import sys
import os

debug = True

def main(pubpath, privpath):
    publist = os.listdir(pubpath)
    privlist = os.listdir(privpath)
    if debug:
        print(publist)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Usage tool.py pubpath privpath\n")

        print("where pubpath is the path to a folder containing \npublic keys\
 and privpath is the path to a folder \ncontaining private keys.")
