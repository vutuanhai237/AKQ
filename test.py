import os
from PIL import Image
import utils
from natsort import natsorted
def cattify(input_img):

        file_name = os.path.basename(input_img)
        img = Image.open(input_img)
        namex = os.path.splitext(file_name)[0]
        for i in range(0, 20):
            canvas = Image.new(img.mode, (img.width, img.height))
            for x in range(canvas.width):
                for y in range(canvas.height):
                    nx = (2 * x + y) % canvas.width
                    ny = (x + y) % canvas.height

                    canvas.putpixel((nx, canvas.height-ny-1), img.getpixel((x, canvas.height-y-1)))

        canvas.save('a.png')

cattify('SAMPLE_IMAGES/cat.jpg')