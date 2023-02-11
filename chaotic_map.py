import os
from PIL import Image
import utils
from natsort import natsorted
import cv2
import random

def images_the_same(image1, image2):
    """
    :param image1: path of image1
    :param image2: path of image2
    :return: True if images are the same, False if images are not the same
    """
    im1 = cv2.imread(image1)
    im2 = cv2.imread(image2)

    if im1.shape != im2.shape:
        return False

    difference = cv2.subtract(im1, im2)
    b, g, r = cv2.split(difference)

    if(cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0
        and cv2.countNonZero(r) == 0):
        return True
    return False

def resize_img(img) -> Image:
    min_size = min(img.size)
    imageBoxSize = 200 # maximum width of image placeholder

    if min_size >= imageBoxSize:
        resized_im = img.resize((imageBoxSize,imageBoxSize)) # arnold's cat map must be square
    else:
        resized_im = img.resize((min_size,min_size))

    return resized_im

def encode(path, save_path):

    file_name = os.path.basename(path)
    img = Image.open(path)
    img = resize_img(img)
    namex = os.path.splitext(file_name)[0]

    images_path = './images/'
    img.save(images_path + f'{namex}-0.png')
    iteration = 0
    done = False
    while not done:
        canvas = Image.new(img.mode, (img.width, img.height))
        for x in range(canvas.width):
            for y in range(canvas.height):
                nx = (2 * x + y) % canvas.width
                ny = (x + y) % canvas.height
                canvas.putpixel((nx, canvas.height-ny-1), img.getpixel((x, canvas.height-y-1)))
        iteration += 1
        new_image = images_path + f'{namex}-{iteration}.png'
        canvas.save(new_image)
        img = Image.open(new_image)
        if images_the_same(images_path + f'{namex}-0.png', new_image):
            done = True
    index = random.randint(int(iteration/4), int(3*iteration/4))
    for i in range(0, iteration + 1):
        if i != index:
            os.remove(images_path + f'{namex}-{i}.png')
    os.rename(f'./images/{namex}-{index}.png', save_path)
    return iteration - index

def decode(path, save_path, iteration):
    file_name = os.path.basename(path)
    img = Image.open(path)
    img = resize_img(img)
    namex = os.path.splitext(file_name)[0]
    
    for i in range(0, iteration):
        canvas = Image.new(img.mode, (img.width, img.height))
        for x in range(canvas.width):
            for y in range(canvas.height):
                nx = (2 * x + y) % canvas.width
                ny = (x + y) % canvas.height
                canvas.putpixel((nx, canvas.height-ny-1), img.getpixel((x, canvas.height-y-1)))
        new_image = f'./images/{namex}-{i}.png'
        canvas.save(new_image)
        img = Image.open(new_image)
    for i in range(0, iteration - 1):
            os.remove(f'./images/{namex}-{i}.png')
    os.rename(f'./images/{namex}-{iteration - 1}.png',save_path)
    return img
# iteration = cattify('images/cat.jpg')
# print(iteration)
# decode('./data/cat_map.png', './data/cat_unmap.png', iteration)
