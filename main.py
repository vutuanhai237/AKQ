from aes import encryptImage, decryptImage
from chaotic_map import encode, decode
from kyber import Kyber512
import os

def gen_key():
    pk, sk = Kyber512.keygen()
    with open("./key/pk.txt", "wb") as binary_file:
        binary_file.write(pk)
    with open("./key/sk.txt", "wb") as binary_file:
        binary_file.write(sk)

def encrypt_image(path, save_path, pk_path, mode):
    pk = open(pk_path, "rb").read()
    c, key = Kyber512.enc(pk)
    with open("./key/c.txt", "wb") as binary_file:
        binary_file.write(c)
    if mode == 'normal':
        encryptImage(path, save_path, key)
        return c
    if mode == 'chaotic':
        new_path = os.path.splitext(path)[0]
        new_path += '_map.png'
        print(new_path)
        iteration = encode(path, new_path)
        encryptImage(new_path, save_path, key)
        return c, iteration

def decrypt_image(path, save_path, sk_path, c_path, iteration, mode):
    sk = open(sk_path, "rb").read()
    c = open(c_path, "rb").read()
    key = Kyber512.dec(c, sk)
    if mode == 'normal':
        decryptImage(path, save_path, key)
        return
    if mode == 'chaotic':
        decryptImage(path, save_path, key)
        decode(save_path, save_path, iteration)
        return

c, iteration = encrypt_image('./images/cat.jpg', './images/cat_en.png', './key/pk.txt', 'chaotic')

decrypt_image('./images/cat_en.png', './images/cat_de.png', './key/sk.txt', './key/c.txt', iteration, 'chaotic')
