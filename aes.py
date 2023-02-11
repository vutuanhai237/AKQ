from kyber import Kyber512
import os
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
KEYSIZE = 16
BLKSIZE = 16

def generateKeyOrInitVector(size):
    return os.urandom(size)

def encryptImage(path, save_path, key):
    with open(path, "rb") as file:
        bytedata = file.read()
        aescipher = AES.new(key, AES.MODE_ECB)
        ct = aescipher.encrypt(pad(bytedata, BLKSIZE))
        # fill new file with cipher text
        with open(save_path, "wb") as newfile:
            newfile.write(ct)


# now reverse for decryption
def decryptImage(path, save_path, key):
    with open(path, "rb") as file:
        bytedata = file.read()
        # get AES in CBC mode and unpad back to original size
        aescipher = AES.new(key, AES.MODE_ECB)
        ct = aescipher.decrypt(bytedata)
        ctunpad = unpad(ct, BLKSIZE)
        # fill new file with decrypted data (should be original image)
        with open(save_path, "wb") as oldfile:
            oldfile.write(ctunpad)

pk = open("./key/pk.txt", "rb").read()
c, key = Kyber512.enc(pk)
encryptImage('./images/tree.png', './tree_en.png', key)
decryptImage('./tree_en.png', './tree_de.png', key)