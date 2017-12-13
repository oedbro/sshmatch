#!/usr/bin/python3

import sys
import os
import time
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
    matches = 0
    if debug:
        print("content of publist " + str(publist))
        print("content of privlist " + str(privlist))
 
    for pub in publist: 
        with open(pubpath + '/' + pub, 'rb') as pubfile:
            pubdata = pubfile.read()
            pubfile.close()
            if debug:
                print("pubdata " + str(pubdata))
        try: 
            pubkey = serialization.load_ssh_public_key(pubdata,\
                backends.default_backend())
        except:
            try:
                pubkey = serialization.load_pem_public_key(pubdata,\
                    backends.default_backend())
            except:
                print("Wrong keytype on " + pub)
                continue

        if debug:
            print("pubkey: " + str(pub))

        pad= padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()),\
                algorithm=hashes.SHA1(),\
                label=None)
        
        for priv in privlist: 
            with open(privpath + '/' + priv, 'rb') as privfile:
                privdata = privfile.read()
                privfile.close()
                if debug:
                    print("privdata " + str(privdata))
            try:
                privkey = serialization.load_pem_private_key(privdata,\
                    None, backends.default_backend())
            except:
                print("Wrong keytype on " + priv)
                privlist.remove(priv)
                continue
            if debug:
                print("privkey: " + str(privkey))
    
            msg = pubkey.encrypt(b"True", pad) 
    
            try:
                privkey.decrypt(msg, pad)
                print("Match: " + pubpath + "/" + pub + " " + privpath +\
                    "/" + priv)
                matches += 1
            except ValueError:
                pass
    print("Total number of matches: " + str(matches))
    print("Nr of public keys: " + str(len(publist)))
    print("Nr of private keys: " + str(len(privlist)))





if __name__ == "__main__":
    if len(sys.argv) == 3:
        start_time = time.time()
        main(sys.argv[1], sys.argv[2])
        print("Runtime: " + str(time.time() - start_time) + " seconds")
    else:
        print("Usage tool.py pubpath privpath\n")

        print("where pubpath is the path to a folder containing \npublic keys\
 and privpath is the path to a folder \ncontaining private keys.")
