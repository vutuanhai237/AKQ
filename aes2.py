from PIL import Image
from Crypto.Cipher import AES
from kyber import Kyber512
from aes import decryptImage
from Crypto.Util.Padding import pad, unpad
filename = "tree.png"
format = "png"
pk, sk = Kyber512.keygen()
c, key = Kyber512.enc(pk)
# AES requires that plaintexts be a multiple of 16, so we have to pad the data
padding_size = 0
def spad(data):
    padding_size = 16-len(data)%16
    print(padding_size)
    data = pad(data,padding_size)
    # return data + b"\x00"*(16-len(data)%16)
    return data
def sunpad(data):
    print(padding_size)
    data = unpad(data,padding_size)
    #return data - b"\x00"*(padding_size)
    return data
# Maps the RGB
def convert_to_RGB(data):
    r, g, b = tuple(map(lambda d: [data[i] for i in range(0,len(data)) if i % 3 == d], [0, 1, 2]))
    pixels = tuple(zip(r,g,b))
    return pixels

def process_image(filename, filename_out, mode):
    # Opens image and converts it to RGB format for PIL
    im = Image.open(filename)
    data = im.convert("RGB").tobytes()

    # Since we will pad the data to satisfy AES's multiple-of-16 requirement, we will store the original data length and "unpad" it later.
    original = len(data)

    # Encrypts using desired AES mode (we'll set it to gcm by default)
    if mode == 'en':
        new = convert_to_RGB(aes_gcm_encrypt(key, (data))[:original])
    else:
        new = convert_to_RGB(aes_gcm_decrypt(key, (data))[:original])
    # Create a new PIL Image object and save the old image data into the new image.
    im2 = Image.new(im.mode, im.size)
    im2.putdata(new)

    #Save image
    im2.save(filename_out, format)

def aes_gcm_encrypt(key, data, mode=AES.MODE_GCM):
    aes = AES.new(key, mode)
    new_data = aes.encrypt(data)
    return new_data
def aes_gcm_decrypt(key, data, mode=AES.MODE_GCM):
    aes = AES.new(key, mode)
    new_data = aes.decrypt(data)
    return new_data

process_image("tree.png", 'en.png', mode = 'en')
process_image('en.png', 'de.png',mode = 'de')