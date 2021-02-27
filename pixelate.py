from PIL import Image
from tqdm import trange

import os
import imageio
import numpy as np


def pixelate(input_name, pixel_size):
    img = Image.open(
        "./images/pre/{input_name}".format(input_name=input_name))
    img = img.resize(
        (int(img.size[0] // pixel_size), int(img.size[1] // pixel_size)),
        Image.NEAREST
    )

    img = img.resize(
        (int(img.size[0] * pixel_size), int(img.size[1] * pixel_size)),
        Image.NEAREST
    )

    return img
    #img.save("./images/filtered/{pixel_size}/{input_name}.jpg".format(pixel_size=pixel_size, input_name=input_name))
    # img.show()
    # return True


LENGTH = np.pi
x = np.arange(0, LENGTH, 0.025)
Fs = LENGTH
LOWER_BOUND, UPPER_BOUND = 6, 10


def exec(file_name):
    frames = []
    fxn = (UPPER_BOUND - LOWER_BOUND) * np.sin(x)
    max_in = 0
    for i in range(len(fxn)):
        if fxn[i + 1] < fxn[i]:
            max_in = i
            break

    depo = fxn[1:max_in + 1] + [LOWER_BOUND] * max_in
    fxn = np.concatenate((depo, depo[::-1][1::]))

    for i in trange(len(fxn), desc="{file_name} Process".format(file_name=file_name)):
        frames.append(pixelate(file_name, fxn[i]))

    imageio.mimsave("./images/filtered/" + file_name +
                    ".gif", frames, "GIF")


files = [file for file in os.listdir(
    "./images/pre") if not ".DS_Store" in file]
for i in trange(len(files), desc="Pixelated"):
    exec(files[i])
