import os
from PIL import Image
import utils
from natsort import natsorted
import cv2

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

def cattify(input_img):

    file_name = os.path.basename(input_img)
    img = Image.open(input_img)
    img = resize_img(img)
    namex = os.path.splitext(file_name)[0]

    images_path = './data/'
    img.save(images_path + f'ACM-{namex}-0.png')
    iteration = 0
    done = False
    while not done:
        print(f"Iteration {iteration}")
        canvas = Image.new(img.mode, (img.width, img.height))
        for x in range(canvas.width):
            for y in range(canvas.height):
                nx = (2 * x + y) % canvas.width
                ny = (x + y) % canvas.height

                canvas.putpixel((nx, canvas.height-ny-1), img.getpixel((x, canvas.height-y-1)))
        iteration += 1

        new_image = images_path + f'ACM-{namex}-{iteration}.png'
        canvas.save(new_image)
        img = Image.open(new_image)


        if utils.images_the_same(images_path + f'ACM-{namex}-0.png', new_image):
            done = True



cattify('SAMPLE_IMAGES/cat.jpg')