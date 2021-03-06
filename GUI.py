import tkinter as tk
from datetime import datetime
import time as t
from PIL import ImageTk, Image
import os
from CheckersGame import CheckersGame
from adversarialSearches import *

dir = os.path.dirname(__file__)

global mouse_x
global mouse_y


class GUI:

    def __init__(self):

        self.tile_size = 64

        self.root = tk.Tk()  # Creates window
        self.root.title("Checkers")
        self.root.geometry("512x512")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=self.tile_size * 8, height=self.tile_size * 8)
        self.canvas.pack()

        checkerboard = os.path.join(dir, 'images', 'checkerboard.png')
        red_circle = os.path.join(dir, 'images', 'red_circle.png')
        black_circle = os.path.join(dir, 'images', 'black_circle.png')
        red_king = os.path.join(dir, 'images', 'red_king.png')
        black_king = os.path.join(dir, 'images', 'black_king.png')
        checkerboard = Image.open(checkerboard).resize((self.tile_size * 8, self.tile_size * 8), Image.ANTIALIAS)
        self.checkerboard = ImageTk.PhotoImage(checkerboard)
        red_circle = Image.open(red_circle).resize((self.tile_size, self.tile_size), Image.ANTIALIAS)
        self.red_circle = ImageTk.PhotoImage(red_circle)
        black_circle = Image.open(black_circle).resize((self.tile_size, self.tile_size), Image.ANTIALIAS)
        self.black_circle = ImageTk.PhotoImage(black_circle)
        red_king = Image.open(red_king).resize((self.tile_size, self.tile_size), Image.ANTIALIAS)
        self.red_king = ImageTk.PhotoImage(red_king)
        black_king = Image.open(black_king).resize((self.tile_size, self.tile_size), Image.ANTIALIAS)
        self.black_king = ImageTk.PhotoImage(black_king)

        self.cg = CheckersGame()
        self.state = self.cg.initial

        self.first_click = False
        self.first_click_pos = None



        self.draw(self.canvas, self.state)

        def motion(event):
            global mouse_x, mouse_y
            mouse_x = event.x
            mouse_y = event.y

        self.root.bind('<Motion>', motion)

        def mouseclick(event):
            tile_x = mouse_x//self.tile_size
            tile_y = mouse_y//self.tile_size
            print(tile_x, tile_y)

            if not self.first_click:
                self.first_click_pos = [tile_x, tile_y]
            elif self.cg.is_legal_move(self.state.board, self.first_click_pos, [tile_x, tile_y], "B"):
                # move = alpha_beta_cutoff_search(self.state, self.cg, d=4) #AI using A-B cutoff
                # move = minmax_decision(self.state, self.cg, depth=2) #AI using Minimax
                self.state = self.cg.result(self.state, [self.first_click_pos, [tile_x, tile_y]])# <-change last paramenter to move for AI v AI

                time = t.time()
                move = alpha_beta_cutoff_search(self.state, self.cg, d=4) #AI using A-B Cutoff
                # move = minmax_decision(self.state, self.cg, depth=2)  # AI using Minimax
                print("Time taken: ", t.time() - time, " s")
                self.state = self.cg.result(self.state, move)# [self.first_click_pos, [tile_x, tile_y]]) <- Uncomment this and block comment 'move' for Human v Human
            self.first_click = not self.first_click
            self.draw(self.canvas, self.state)

        self.root.bind('<Button-1>', mouseclick)

        tk.mainloop()

    def draw(self, canvas, state):
        canvas.delete("all")
        canvas.create_image(0, 0, image=self.checkerboard, anchor=tk.NW)

        for i in range(len(state.board)):
            for j in range(len(state.board)):
                image = None
                if state.board[i][j] == "B":
                    image = self.black_circle
                elif state.board[i][j] == "BK":
                    image = self.black_king
                elif state.board[i][j] == "R":
                    image = self.red_circle
                elif state.board[i][j] == "RK":
                    image = self.red_king
                canvas.create_image(j*self.tile_size, i*self.tile_size, image=image, anchor=tk.NW)


GUI()
