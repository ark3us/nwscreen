#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import numpy as np
import os
from PIL import Image


x1 = x2 = y1 = y2 = 0


def onselect(eclick, erelease):
    global x1, x2, y1, y2
    x1 = int(eclick.xdata)
    x2 = int(erelease.xdata)
    y1 = int(eclick.ydata)
    y2 = int(erelease.ydata)
    plt.close()


def main():
    images = []

    for root, _, files in os.walk("imgs"):
        for f in files:
            if "screenshots_here" in f:
                continue
            filename = os.path.join(root, f)
            images.append(filename)

    # Sort by creation time
    images.sort(key=os.path.getctime)
    newimg = Image.new("RGB", (1,1))
    rows = 0
    cols = 0
    if len(images) > 4:
        maxrows = 5
    else:
        maxrows = len(images)

    for filename in images:
        im = Image.open(filename)
        if not x2:
            # Select chat window
            fig = plt.figure()
            ax = fig.add_subplot(111)
            arr = np.asarray(im)
            plt.imshow(arr)
            rs=widgets.RectangleSelector(
                ax, onselect, drawtype='box',
                rectprops = dict(facecolor='red', edgecolor = 'black', alpha=0.5, fill=True))
            
            mng = plt.get_current_fig_manager()
            mng.resize(*mng.window.maxsize())
            plt.show()
        
        if rows == 5:
            cols += 1
            rows = 0

        im1 = im.crop((x1, y1, x2, y2))
        tmpimg = Image.new("RGB", (maxrows*(x1+x2), (cols+1)*(y2-y1)))
        tmpimg.paste(newimg, (0, 0))
        tmpimg.paste(im1, (rows*(x1+x2), cols*(y2-y1)))
        newimg = tmpimg
        rows += 1

    # newimg.show()

    # Delete tells
    image_data = newimg.load()
    height, width = newimg.size
    for loop1 in range(height):
        for loop2 in range(width):
            r,g,b = image_data[loop1,loop2]
            if r < 50 and b < 50 and g > 170:
                for x in range(loop1-5, loop1+5):
                    for y in range(loop2-5, loop2+5):
                        image_data[x, y] = r, 169, b

    newimg.show()


if __name__ == "__main__":
    main()
