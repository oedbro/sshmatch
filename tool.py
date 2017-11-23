#!/usr/bin/python3

import sys
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat import backends
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
#from OpenSSL import crypto

debug = True

def main(pubpath, privpath):
    publist = os.listdir(pubpath)
    privlist = os.listdir(privpath)
    if debug:
        print("content of publist " + str(publist))
    
    with open(pubpath + '/' + publist[0], 'rb') as pubfile:
        pubdata = pubfile.read()
        if debug:
            print("pubdata " + str(pubdata))
    # pubkey = crypto.load_publickey(crypto.FILETYPE_PEM, pubdata)
    pubkey = serialization.load_ssh_public_key(pubdata,\
            backends.default_backend()) 
    if debug:
        print("pubkey: " + str(pubkey))
    
    with open(privpath + '/' + privlist[0], 'rb') as privfile:
        privdata = privfile.read()
        if debug:
            print("privdata " + str(privdata))
    # pubkey = crypto.load_publickey(crypto.FILETYPE_PEM, pubdata)
    privkey = serialization.load_pem_private_key(privdata,\
            None, backends.default_backend()) 
    if debug:
        print("privkey: " + str(privkey))
    
    #testkey = privkey.public_key()
    #if debug:
    #    print("testkey: " + str(testkey))
   
    pad= padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()),\
            algorithm=hashes.SHA1(),\
            label=None)
    msg = pubkey.encrypt(b"True", pad)
    
    
    if privkey.decrypt(msg, pad) == b"True":
        print("YAY")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Usage tool.py pubpath privpath\n")

        print("where pubpath is the path to a folder containing \npublic keys\
 and privpath is the path to a folder \ncontaining private keys.")
