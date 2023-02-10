from kyber import Kyber512
import os
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
KEYSIZE = 16
BLKSIZE = 16
filename = "tree.png"
# encrypted_so_not_funny.png
newfilename = "encrypted_so_not_" + filename
# decrypted_so_funny.png
oldfilename = "decrypted_so_" + filename


# generate keys and initialization vector randomly (pseudorandom)
def generateKeyOrInitVector(size):
    return os.urandom(size)


# use the key and vector to encrypt and decrypt using AES
def encryptImage(filename, key):
    with open(filename, "rb") as file:
        bytedata = file.read()
        # use AES algorithm in CBC mode and pad to fit full block
        aescipher = AES.new(key, AES.MODE_ECB)
        ct = aescipher.encrypt(pad(bytedata, BLKSIZE))
        # fill new file with cipher text
        with open(newfilename, "wb") as newfile:
            newfile.write(ct)


# now reverse for decryption
def decryptImage(filename, key):
    with open(filename, "rb") as file:
        bytedata = file.read()
        # get AES in CBC mode and unpad back to original size
        aescipher = AES.new(key, AES.MODE_ECB)
        ct = aescipher.decrypt(bytedata)
        ctunpad = unpad(ct, BLKSIZE)
        # fill new file with decrypted data (should be original image)
        with open(oldfilename, "wb") as oldfile:
            oldfile.write(ctunpad)


# set up key and vector, and call the encryption and decryption functions

pk, sk = Kyber512.keygen()
c, key = Kyber512.enc(pk)
# encryptImage(filenameinput, key, initVector)
encryptImage(filename, key)
decryptImage(newfilename, key)
