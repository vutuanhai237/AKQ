from kyber import Kyber512
import os, cv2, numpy as np
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
KEYSIZE = 16
BLKSIZE = 16

def generateKeyOrInitVector(size):
    return os.urandom(size)

def encryptImage(path, save_path, key):
    # with open(path, "rb") as file:
    #     bytedata = file.read()
    #     aescipher = AES.new(key, AES.MODE_ECB)
    #     ct = aescipher.encrypt(pad(bytedata, BLKSIZE))
    #     # fill new file with cipher text
    #     with open(save_path, "wb") as newfile:
    #         newfile.write(ct)
    image = cv2.imread(path)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_image = cipher.encrypt(image.tobytes())
    encrypted_image = np.frombuffer(encrypted_image, dtype=np.uint8)
    encrypted_image = np.reshape(encrypted_image, image.shape)
    cv2.imwrite(save_path, encrypted_image)
    return encrypted_image

def decryptImage(path, save_path, key):
    # with open(path, "rb") as file:
    #     bytedata = file.read()
    #     # get AES in CBC mode and unpad back to original size
    #     aescipher = AES.new(key, AES.MODE_ECB)
    #     ct = aescipher.decrypt(bytedata)
    #     ctunpad = unpad(ct, BLKSIZE)
    #     # fill new file with decrypted data (should be original image)
    #     with open(save_path, "wb") as oldfile:
    #         oldfile.write(ctunpad)
    encrypted_image = cv2.imread(path)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_image = cipher.decrypt(encrypted_image.tobytes())
    decrypted_image = np.frombuffer(decrypted_image, dtype=np.uint8)
    decrypted_image = np.reshape(decrypted_image, encrypted_image.shape)
    cv2.imwrite(save_path, decrypted_image)
    return decrypted_image

# pk = open("./key/pk_cat.txt", "rb").read()
# c, key = Kyber512.enc(pk)
# print(key)
# encryptImage('./images/lenna100.png', './images/lenna100_en.png', key)
# decryptImage('./images/lenna100_en.png', './images/lenna100_de.png', key)