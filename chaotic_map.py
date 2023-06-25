import os
from PIL import Image
import utils
from natsort import natsorted
import cv2, numpy as np
import random
from shutil import move

def resize_img(img) -> Image:

    resized_im = img.resize((100,100))

    return resized_im

def arnold_cat_map(image):
    height, width, _ = image.shape
    mapped_image = np.zeros_like(image)

    for i in range(height):
        for j in range(width):
            new_i = (2 * i + j) % height
            new_j = (i + j) % width
            mapped_image[new_i, new_j] = image[i, j]

    return mapped_image

def multi_arnold_cat_map(image, times):
    for _ in range(times):
        image = arnold_cat_map(image)
    return image

def find_period_arnold_cat_map(image):
    original_image = image.copy()
    period = 0
    while True:
        image = arnold_cat_map(image)
        period += 1
        if np.array_equal(image, original_image):
            return period
        if period > 1000:
            return 0

def random_map(path, save_path) -> int:
    image = cv2.imread(path)
    period = find_period_arnold_cat_map(image)
    p_dot = np.random.randint(int(period / 4), int(3 * period / 4))
    image = multi_arnold_cat_map(image, p_dot)
    cv2.imwrite(save_path, image)
    return period - p_dot

def specific_map(path, save_path, times) -> int:
    image = cv2.imread(path)
    image = multi_arnold_cat_map(image, times)
    cv2.imwrite(save_path, image)
    return

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

# pdot = random_map('./images/lenna.png', './images/lenna_map.png')
# specific_map('./images/lenna_map.png', './images/lenna_unmap.png', pdot)
p = find_period_arnold_cat_map(cv2.imread('./images/lenna512.png'))
print(p)