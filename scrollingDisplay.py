#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
if sys.version_info.major == 3:
    import tkinter as tk
else:
    import Tkinter as tk
import time

DOT_SIZE = 16
MARGIN = 7
SPACING = 4
WIDTH = 50
HEIGHT = 8

FONT = dict()

def parse_font():
    with open("8x8_font.txt", 'r') as font:
        data = [i.split(' ') for i in font.read().split('\n')[:-1]]
    for char, matrix in data:
        m2 = [[k=='1' for k in matrix[i:i+8]] for i in range(0, 8*8, 8)]
        FONT[char.lower()] = m2
    

class ScrollDisplay():
    """"""
    def __init__(self, master):
        self.master = master
        self.leds = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.string = ""
        self.stringAs8bitFont = [[False] for _ in range(HEIGHT)]
        self.step = 0
        self.gui()
        self.update_string()
        self.scroll()

    def gui(self):
        """"""
        self.width = WIDTH*DOT_SIZE + (WIDTH-1)*SPACING + 2*MARGIN
        self.height = HEIGHT*DOT_SIZE + (HEIGHT-1)*SPACING + 2*MARGIN
        self.canvas = tk.Canvas(self.master,
                                width=self.width,
                                height=self.height,
                                bg="black")
        self.canvas.pack()
        # init the canva leds
        for r, line in enumerate(self.leds):
            for c, val in enumerate(line):
                self.canvas.create_oval(c*(DOT_SIZE+SPACING)+MARGIN,
                                        r*(DOT_SIZE+SPACING)+MARGIN,
                                        c*(DOT_SIZE+SPACING)+MARGIN+DOT_SIZE,
                                        r*(DOT_SIZE+SPACING)+MARGIN+DOT_SIZE,
                                        fill="gray")
        #
        self.uEntry = tk.StringVar()
        self.uEntry.set("Enter your text here")
        ent = tk.Entry(self.master, textvariable=self.uEntry)
        ent.pack(fill='x')
        ent.bind('<KeyRelease>', self.update_string)

    def update_leds(self):
        for r, line in enumerate(self.leds):
            for c, val in enumerate(line):
                color = "red" if self.leds[r][c] else "gray8"
                self.canvas.itemconfig(r*WIDTH+c+1, fill=color)

    def update_string(self, event=None):
        self.string = self.uEntry.get()
        self.step = 0
        self.string_to_8bit()

    def string_to_8bit(self):
        self.string = self.string.lower()
        self.stringAs8bitFont = [[False for _ in range(WIDTH)]
                                 for _ in range(HEIGHT)]
        for char in self.string:
            if char == ' ':
                for i in range(HEIGHT):
                    self.stringAs8bitFont[i] += [False]*3
                continue
            for i, line in enumerate(FONT[char]):
                self.stringAs8bitFont[i] += line
            # for spacing
            for i in range(HEIGHT):
                self.stringAs8bitFont[i].append(False)

    def scroll(self):
        for i in range(HEIGHT):
            for j in range(WIDTH):
                try:
                    if self.stringAs8bitFont[i][j]:
                        self.leds[i][j] = True
                    else:
                        self.leds[i][j] = False
                except IndexError:
                    self.leds[i][j] = False
        for i in range(HEIGHT):
            del self.stringAs8bitFont[i][0]
        if len(self.stringAs8bitFont[0]) == 0:
            self.string_to_8bit()
        self.update_leds()
        self.master.after(50, self.scroll)

    def print_bit(self):
        for i in self.stringAs8bitFont:
            print("".join(map(lambda x: '1' if x else '0', i)))
        print('\n')
        
        

if __name__ == "__main__":
    parse_font()
    root = tk.Tk()
    root.title("Scrolling Display")
    root.resizable(False, False)
    myApp = ScrollDisplay(root)
    root.mainloop()
