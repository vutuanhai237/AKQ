from kyber import Kyber512
import pathlib

def gen_key():
    pk, sk = Kyber512.keygen()
    with open("./key/pk.txt", "wb") as binary_file:
        binary_file.write(pk)
    with open("./key/sk.txt", "wb") as binary_file:
        binary_file.write(sk)
    
pk = open("./key/pk.txt", "rb").read()
sk = open("./key/sk.txt", "rb").read()
c, key = Kyber512.enc(pk)
_key = Kyber512.dec(c, sk)
print(key[:50], end = '\n')
print(_key[:50])