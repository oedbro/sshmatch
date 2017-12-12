#!/usr/bin/python3

import sys
import os

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat import backends
from cryptography.hazmat.primitives import serialization

# Debug output
debug = True

# Settings
PublicExponent = 65537
Keysize = 2048

def generator(keyType, numberOfKeys):
    # The function that generates x keys
    for key in range(int(numberOfKeys)):
        if debug:
            print(key)
        private_key =\
        rsa.generate_private_key(PublicExponent,Keysize,\
                backends.default_backend())
        if keyType == "pem":
            # Private key
            pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption())
            keyFile = open(str(key) + ".pem", "wb")
            keyFile.write(pem)
            keyFile.close()
            # Public key
            public_key = private_key.public_key()
            pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)
            keyFile = open(str(key) + ".pub.pem", "wb")
            keyFile.write(pem)
            keyFile.close()
        if keyType == "ssh":
            # Private key
            ssh = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption())
            keyFile = open(str(key), "wb")
            keyFile.write(ssh)
            keyFile.close()
            # Public key
            public_key = private_key.public_key()
            ssh = public_key.public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH)
            keyFile = open(str(key) + ".pub", "wb")
            keyFile.write(ssh)
            keyFile.close()



if __name__ == "__main__":
    if len(sys.argv) == 3:
        if(debug):
            print("Generating")
        generator(sys.argv[1], sys.argv[2])
    else:
        print("Usage generator keytype numberOfKeys")
