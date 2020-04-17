#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
if sys.version_info.major == 3:
    import tkinter as tk
else:
    import Tkinter as tk

DOT_SIZE = 20
MARGIN = 10
SPACING = 10

class FontEditor():
    """"""
    def __init__(self, master):
        self.master = master
        self.leds = [[False for _ in range(8)] for _ in range(8)]
        self.gui()
        self.display()

    def gui(self):
        """"""
        self.width = self.height = 8*DOT_SIZE + 7*SPACING + 2*MARGIN
        self.canvas = tk.Canvas(self.master,
                                width=self.width,
                                height=self.height,
                                bg="black")
        self.canvas.grid(columnspan=2)
        self.canvas.bind('<Button-1>', self.switch)
        # init the canva leds
        for r, line in enumerate(self.leds):
            for c, val in enumerate(line):
                self.canvas.create_oval(c*(DOT_SIZE+SPACING)+MARGIN,
                                        r*(DOT_SIZE+SPACING)+MARGIN,
                                        c*(DOT_SIZE+SPACING)+MARGIN+DOT_SIZE,
                                        r*(DOT_SIZE+SPACING)+MARGIN+DOT_SIZE,
                                        fill="gray")
        
        tk.Label(self.master, text="Letter").grid(row=1, column=0)
        self.symbol = tk.StringVar()
        tk.Entry(self.master, textvariable=self.symbol).grid(row=2, column=0)
        tk.Button(self.master, text="Save", command=self.save)\
          .grid(row=1, column=1)
        tk.Button(self.master, text="Reset", command=self.reset)\
          .grid(row=2, column=1)

    def switch(self, event):
        column = 8*event.x//self.width
        row = 8*event.y//self.height
        self.leds[row][column] = not self.leds[row][column]
        self.update_led(row, column)
        

    def leds_as_string(self):
        return ''.join(''.join(map(lambda x: '1' if x else '0', i)) for i in self.leds)

    def display(self):
        for r, line in enumerate(self.leds):
            for c, val in enumerate(line):
                self.update_led(r, c)
        self.master.update_idletasks()

    def update_led(self, row, column):
        color = "red" if self.leds[row][column] else "gray"
        self.canvas.itemconfig(row*8+column+1, fill=color)
        

    def reset(self):
        for i in range(8):
            for j in range(8):
                self.leds[i][j] = False
        self.display()

    def save(self):
        with open("8x8_font.txt", 'a') as font:
            font.write(self.symbol.get() + ' ' + self.leds_as_string() + '\n')


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pixel Font Editor")
    root.resizable(False, False)
    myApp = FontEditor(root)
    root.mainloop()
