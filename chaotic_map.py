import os
from PIL import Image
import utils
from natsort import natsorted
import cv2, numpy as np
import random
from shutil import move
def mse(img1, img2):
    img1 = cv2.imread(img1)
    img2 = cv2.imread(img2)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff**2)
    mse = err/(float(h*w))
    if mse < 5:
        return True
    return False

def images_the_same2(im1, im2) -> bool:
    im1 = cv2.imread(im1)
    im2 = np.array(im2)
    im2 = im2[:, :, ::-1].copy()
    if im1.shape != im2.shape:
        return False

    difference = cv2.subtract(im1, im2)
    b, g, r = cv2.split(difference)

    if(cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0
        and cv2.countNonZero(r) == 0):
        return True
    return False

def images_the_same(image1, image2) -> bool:
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

    resized_im = img.resize((100,100))

    return resized_im

def map(path, save_path) -> int:
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
        if mse(images_path + f'{namex}-0.png', new_image):
            done = True
    print(iteration)
    index = random.randint(int(iteration/4), int(3*iteration/4))
    for i in range(0, iteration + 1):
        if i != index:
            os.remove(images_path + f'{namex}-{i}.png')
    move(f'./images/{namex}-{index}.png', save_path)
    return iteration - index

def unmap(path, save_path, iteration):
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
        if i != iteration - 1:
            img = Image.open(new_image)
    for i in range(0, iteration - 1):
            os.remove(f'./images/{namex}-{i}.png')
    move(f'./images/{namex}-{iteration - 1}.png',save_path)
    return img

# encode('./images/cat.jpg', './images/cat_map.png')
# iteration = cattify('images/cat.jpg')
# print(iteration)
# decode('./data/cat_map.png', './data/cat_unmap.png', iteration)

#print(mse('./images/cat_de.png','./images/cat_de2.png'))