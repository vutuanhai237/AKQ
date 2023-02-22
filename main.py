from aes import encryptImage, decryptImage
from chaotic_map import encode, decode
from kyber import Kyber512
import os
import json
def gen_key(name):
    pk, sk = Kyber512.keygen()
    with open(f"./key/pk_{name}.txt", "wb") as binary_file:
        binary_file.write(pk)
    with open(f"./key/sk_{name}.txt", "wb") as binary_file:
        binary_file.write(sk)

def encrypt_image(path, save_path, mode):
    name = os.path.basename(path).split(".")[0]
    gen_key(name)
    pk = open(f"./key/pk_{name}.txt", "rb").read()
    c, key = Kyber512.enc(pk)
    with open(f"./key/c_{name}.txt", "wb") as binary_file:
        binary_file.write(c)
    if mode == 'normal':
        encryptImage(path, save_path, key)
        return
    if mode == 'chaotic':
        period = encode(path, f"{name}_map.png")
        encryptImage(f"{name}_map.png", save_path, key)
        json_file = {
            "name": name,
            "c": f"./key/c_{name}.txt",
            "period": period,
            "path": save_path
        }
        
        json_object = json.dumps(json_file, indent=4)
        with open(f"./database/{name}.json", "w") as outfile:
            outfile.write(json_object)
        return

def decrypt_image(save_path, mode):
    data = json.load(open('./database/tree.json'))
    name = data['name']
    sk = open(f"./key/sk_{name}.txt", "rb").read()
    c = open(data['c'], "rb").read()
    key = Kyber512.dec(c, sk)
    path = data['path']
    if mode == 'normal':
        decryptImage(path, save_path, key)
        return
    if mode == 'chaotic':
        decryptImage(path, save_path, key)
        decode(save_path, save_path, data['period'])
        return
    return

name = 'tree'
# c, iteration = encrypt_image('./images/' + name + '.png', './images/' + name + '_en.png', './key/pk.txt', 'chaotic')
# encrypt_image(f'./images/{name}.png', f'./images/{name}_en.png', 'chaotic')

decrypt_image(f'./images/{name}_de.png','chaotic')
