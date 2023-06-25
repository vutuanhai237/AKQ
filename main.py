import aes
import chaotic_map
from kyber import Kyber512
import os, json, time, numpy as np
def gen_key(name):
    pk, sk = Kyber512.keygen()
    with open(f"./key/pk_{name}.txt", "wb") as binary_file:
        binary_file.write(pk)
    with open(f"./key/sk_{name}.txt", "wb") as binary_file:
        binary_file.write(sk)

def encrypt_image(path, save_path, mode):
    name = os.path.basename(path).split(".")[0]
    pk = open(f"./key/pk_{name}.txt", "rb").read()
    c, key = Kyber512.enc(pk)
    with open(f"./key/c_{name}.txt", "wb") as binary_file:
        binary_file.write(c)
    if mode == 'normal':
        aes.encryptImage(path, save_path, key)
        return
    if mode == 'chaotic':
        p_hat = chaotic_map.random_map(path, f"{name}_map.png")
        print(p_hat)
        aes.encryptImage(f"{name}_map.png", save_path, key)
        json_file = {
            "name": name,
            "c": f"./key/c_{name}.txt",
            "period": p_hat,
            "path": save_path
        }
        
        json_object = json.dumps(json_file, indent=4)
        with open(f"./database/{name}.json", "w") as outfile:
            outfile.write(json_object)
        return

def decrypt_image(name, save_path, mode):
    data = json.load(open(f'./database/{name}.json'))
    sk = open(f"./key/sk_{name}.txt", "rb").read()
    c = open(data['c'], "rb").read()
    key = Kyber512.dec(c, sk)
    path = data['path']
    if mode == 'normal':
        aes.decryptImage(path, save_path, key)
        return
    if mode == 'chaotic':
        aes.decryptImage(path, save_path, key)
        chaotic_map.specific_map(save_path, save_path, data['period'])
        return
    return

name = 'lenna512'
#gen_key(name)
#encrypt_image(f'./images/{name}.png', f'./images/{name}_en.png', 'chaotic')
#decrypt_image(name, f'./images/{name}_de.png','chaotic')

gen, en, de = [], [], []

for _ in range(0, 2):
    start_time = time.time()
    gen_key(name)
    gen.append(time.time() - start_time)
    print(1)
    start_time = time.time()
    encrypt_image(f'./images/{name}.png', f'./images/{name}_en.png', 'chaotic')
    en.append(time.time() - start_time)
    print(1)
    start_time = time.time()
    decrypt_image(name, f'./images/{name}_de.png','chaotic')
    de.append(time.time() - start_time)

gen = np.asarray(gen)
en = np.asarray(en)
de = np.asarray(de)
print(f'{np.round(np.average(gen), 4)} $\pm$ {np.round(np.std(gen), 4)} & {np.round(np.average(en), 4)} $\pm$ {np.round(np.std(en), 4)} & {np.round(np.average(de), 4)} $\pm$ {np.round(np.std(de), 4)}')
# print(np.average(gen))
# print(np.std(gen))
# print(np.average(en))
# print(np.std(en))
# print(np.average(de))
# print(np.std(de))