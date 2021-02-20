#!/usr/bin/env python3

from PySimpleGUI.PySimpleGUI import Checkbox, T
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import matplotlib.backends.backend_qt5agg
import matplotlib.backends.backend_tkagg
import numpy as np
import os
import PySimpleGUI as sg
import queue
import threading
import time
from PIL import Image

done = False
x1 = x2 = y1 = y2 = 0
resimg = None

def main():
    matplotlib.use("Qt5Agg")
    images = []

    layout = [
        [sg.Input(key="_FILES_", enable_events=True, visible=False)],
        [sg.Text("Seleziona screenshots: "), sg.FilesBrowse("...", target="_FILES_")],
        [sg.Multiline(key="_FILELIST_", disabled=True)],
        [sg.Checkbox("Cancella Tell", default=True, key="_DELTELLS_"), sg.Button("Inizia!")],
    ]

    window = sg.Window("Screenshot Composer", layout, finalize=True, auto_size_text=True, auto_size_buttons=True, resizable=True)
    while True:
        event, values = window.read()
        # print(event, values)
        if event == sg.WIN_CLOSED:
            break

        if event == "_FILES_" and values.get("_FILES_"):
            maxline = 0
            images = values.get("_FILES_").split(";")
            for f in images:
                if len(f) > maxline:
                    maxline = len(f)

            maxcol = len(images)
            if maxline > 200:
                maxline = 200
            if maxcol > 20:
                maxcol = 20

            window["_FILELIST_"].Update("\n".join(images))
            window["_FILELIST_"].set_size((maxline, maxcol))
        
        elif event == "Inizia!":
            progress = queue.Queue()
            process(images, progress, values.get("_DELTELLS_"))
            while not done:
                time.sleep(1)
                if progress.qsize() > 0:
                    sg.OneLineProgressMeter('Processando le immagini...', progress.qsize(), len(images))
            if resimg:
                resimg.save("collage_{}.jpg".format(time.time()))
                resimg.show()


def onselect(eclick, erelease):
    global x1, x2, y1, y2
    x1 = int(eclick.xdata)
    x2 = int(erelease.xdata)
    y1 = int(eclick.ydata)
    y2 = int(erelease.ydata)

    # print(x1, x2, y1, y2)
    plt.close()


def process(images: list, progress: queue.Queue, deltells = False):
    global done, resimg, x1, x2, y1, y2
    resimg = None
    done = False
    x1 = x2 = y1 = y2 = 0

    if len(images) < 2:
        done = True
        return

    im = Image.open(images[0])
    # Select chat window
    fig = plt.figure()
    ax = fig.add_subplot(111)
    arr = np.asarray(im)
    plt.imshow(arr)
    rs = widgets.RectangleSelector(
        ax, onselect, drawtype='box',
        rectprops = dict(facecolor='red', edgecolor='black', alpha=0.5, fill=True))

    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.show()

    if x2 == 0:
        done = True
        return

    def process_thread():
        try:
            global resimg
            resimg = process_images(images, progress, deltells)
        finally:
            global done
            done = True

    th = threading.Thread(target=process_thread)
    th.daemon = True
    th.start()


def process_images(images: list, progress: queue.Queue, deltells = False) -> Image:
    if not images:
        return

    newimg = Image.new("RGB", (1,1))
    rows = 0
    cols = 0
    if len(images) > 4:
        maxrows = 5
    else:
        maxrows = len(images)

    for filename in images:
        im = Image.open(filename)
        
        if rows == 5:
            cols += 1
            rows = 0

        im1 = im.crop((x1, y1, x2, y2)).convert("RGB")
        # Delete tells
        if deltells:
            image_data = im1.load()
            height, width = im1.size
            for loop1 in range(height):
                for loop2 in range(width):
                    r, g, b = image_data[loop1,loop2]
                    if r < 50 and b < 50 and g > 170:
                        for x in range(5, height-5):
                            for y in range(loop2-7, loop2+7):
                                image_data[x, y] = r, 169, b

        tmpimg = Image.new("RGB", (maxrows*(x2-x1), (cols+1)*(y2-y1)))
        tmpimg.paste(newimg, (0, 0))
        tmpimg.paste(im1, (rows*(x2-x1), cols*(y2-y1)))
        
        newimg = tmpimg
        rows += 1
    
        progress.put(filename)

    return newimg

if __name__ == "__main__":
    main()
