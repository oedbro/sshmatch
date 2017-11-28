#!/usr/bin/python3

import sys
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat import backends
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# set to true for debug output
debug = False

def main(pubpath, privpath):
    # generate a list of the keys to test
    publist = os.listdir(pubpath)
    privlist = os.listdir(privpath)
    if debug:
        print("content of publist " + str(publist))
        print("content of privlist " + str(privlist))
 
    for pub in publist: 
        with open(pubpath + '/' + pub, 'rb') as pubfile:
            pubdata = pubfile.read()
            if debug:
                print("pubdata " + str(pubdata))
        pubkey = serialization.load_ssh_public_key(pubdata,\
                backends.default_backend()) 
        if debug:
            print("pubkey: " + str(pub))


        pad= padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()),\
                algorithm=hashes.SHA1(),\
                label=None)
        
        for priv in privlist: 
            with open(privpath + '/' + priv, 'rb') as privfile:
                privdata = privfile.read()
                if debug:
                    print("privdata " + str(privdata))
            privkey = serialization.load_pem_private_key(privdata,\
                    None, backends.default_backend()) 
            if debug:
                print("privkey: " + str(privkey))
    
            msg = pubkey.encrypt(b"True", pad) 
    
            try:
                if privkey.decrypt(msg, pad) == b"True":
                    print("Match: " + pubpath + "/" + pub + " " + privpath +\
                    "/" + priv)
            except ValueError:
                pass

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Usage tool.py pubpath privpath\n")

        print("where pubpath is the path to a folder containing \npublic keys\
 and privpath is the path to a folder \ncontaining private keys.")
