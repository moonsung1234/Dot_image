
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageGrab as Ig
import pyautogui as pg
import mouse
import time

def get_clicked_position() :
    while True :
        if mouse.is_pressed("left") :
            return mouse.get_position()

def get_colors_arr(position) :
    return_arr = []

    for y in range(position[1], position[1] + 27 + 1, 27) :
        for x in range(position[0], position[0] + 27 * 10, 27) :
            return_arr.append([
                (x, y),
                screen.getpixel((x, y))
            ])

    return return_arr

def get_similar_rgb_position(screen, arr, rgb) :
    r, g, b = rgb

    return sorted(arr, key=lambda color : abs(color[1][0]-r)+abs(color[1][1]-g)+abs(color[1][2]-b))[0]

image = cv2.imread("./images/apple.jpg", cv2.IMREAD_COLOR)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
result_image = []

block_size = 5

for row in range(block_size, len(image_rgb) + 1, block_size) :
    row_arr = []

    for col in range(block_size, len(image_rgb[0]) + 1, block_size) :
        block = image_rgb[row-block_size:row, col-block_size:col].flatten().reshape(block_size ** 2, 3)
        
        aver_r = int(np.mean(block[:, 0]))
        aver_g = int(np.mean(block[:, 1]))
        aver_b = int(np.mean(block[:, 2]))

        row_arr.append([aver_r, aver_g, aver_b])

    result_image.append(row_arr)

print("done")

# pg.MINIMUM_DURATION = 0
# pg.MINIMUM_SLEEP = 0
# pg.PAUSE = 0

sx, sy = get_clicked_position()
screen = Ig.grab().convert("RGB")

print("ok")

time.sleep(0.2)

cx, cy = get_clicked_position()
arr = get_colors_arr((cx, cy))

print("ok")

before_rgb = None

for i in range(len(result_image)) :
    for j in range(len(result_image[0])) :
        (mx, my), mrgb = get_similar_rgb_position(screen, arr, result_image[i][j])
        
        if mrgb != before_rgb :
            pg.moveTo(x=mx, y=my)
            mouse.click("left")

        mouse.move(sx + j * 7, sy + i * 7)
        mouse.click("left")

        before_rgb = mrgb

plt.imshow(np.array(result_image))
plt.show()
