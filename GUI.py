import tkinter as tk
from PIL import ImageTk, Image
import os

dir = os.path.dirname(__file__)

global mouse_x
global mouse_y


class GUI:
    checkerboard = os.path.join(dir, 'images', 'checkerboard.png')
    tile_size = 64

    root = tk.Tk()
    root.resizable(False, False)
    w = tk.Canvas(root, width=tile_size * 8, height=tile_size * 8)
    w.pack()

    img = Image.open(checkerboard).resize((tile_size * 8, tile_size * 8), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    w.create_image(0, 0, image=img, anchor=tk.NW)

    def motion(event):
        global mouse_x, mouse_y
        mouse_x = event.x
        mouse_y = event.y

    root.bind('<Motion>', motion)

    def mouseclick(event):
        print(mouse_x, mouse_y)

    root.bind('<Button-1>', mouseclick)

    tk.mainloop()


GUI()
