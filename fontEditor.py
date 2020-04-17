#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
if sys.version_info.major == 3:
    import tkinter as tk
else:
    import Tkinter as tk
import pickle as pk
import os

savePath = os.path.join(os.path.dirname(__file__), "8x8_fonts")


DOT_SIZE = 22
MARGIN = 8
SPACING = 4

class FontEditor():
    """"""
    def __init__(self, master):
        self.master = master
        self.leds = [[False for _ in range(8)] for _ in range(8)]
        self.gui()
        self.display()
        try:
            self.load()
        except FileNotFoundError:
            self.data = dict()

    def gui(self):
        """"""
        self.width = self.height = 8*DOT_SIZE + 7*SPACING + 2*MARGIN
        self.canvas = tk.Canvas(self.master,
                                width=self.width,
                                height=self.height,
                                bg="black")
        self.canvas.grid(columnspan=3)
        self.canvas.bind('<Button-1>', self.switch)
        # init the canva leds
        for r, line in enumerate(self.leds):
            for c, val in enumerate(line):
                self.canvas.create_oval(c*(DOT_SIZE+SPACING)+MARGIN,
                                        r*(DOT_SIZE+SPACING)+MARGIN,
                                        c*(DOT_SIZE+SPACING)+MARGIN+DOT_SIZE,
                                        r*(DOT_SIZE+SPACING)+MARGIN+DOT_SIZE,
                                        fill="gray8")
        # infos to display errors
        self.info = tk.StringVar()
        tk.Label(self.master, textvariable=self.info).grid(row=1, column=0)
        self.symbol = tk.StringVar()
        entry = tk.Entry(self.master, textvariable=self.symbol, width=12)
        entry.grid(row=2, column=0)
        entry.bind('<KeyRelease>', self.check_entry)
        tk.Button(self.master, text="Save", command=self.save)\
          .grid(row=1, column=1)
        tk.Button(self.master, text="Load", command=self.load_symbol)\
          .grid(row=1, column=2)
        tk.Button(self.master, text="Reset", command=self.reset)\
          .grid(row=2, column=1, columnspan=2)

    def switch(self, event):
        """Switch the led when clicking on it"""
        column = 8*event.x//self.width
        row = 8*event.y//self.height
        self.leds[row][column] = not self.leds[row][column]
        self.update_led(row, column)

    def check_entry(self, event=None):
        """Prevent the entry of several characters"""
        try:
            self.symbol.set(self.symbol.get()[0])
        except IndexError: # when backspace
            pass

    def update_info(self, string):
        """Display some infos of what is wrong"""
        self.info.set(string)
        self.master.after(1000, lambda *args: self.info.set(''))

    def leds_as_string(self):
        """Return the leds status as one string"""
        return ''.join(''.join(map(lambda x: '1' if x else '0', i)) for i in self.leds)

    def display(self):
        """Update all leds"""
        for r, line in enumerate(self.leds):
            for c, val in enumerate(line):
                self.update_led(r, c)
        self.master.update_idletasks()

    def update_led(self, row, column):
        """Update one leds"""
        color = "red" if self.leds[row][column] else "gray8"
        self.canvas.itemconfig(row*8+column+1, fill=color)
        

    def reset(self):
        """Switch all leds to off"""
        self.leds = [[False for _ in range(8)] for _ in range(8)]
        self.display()

    def load_symbol(self):
        """Loads a symbol from the data"""
        try:
            s = self.symbol.get()[0]
        except IndexError: # when nothing in the entry
            return self.update_info("Enter a symbol")
        if s not in self.data.keys():
            self.update_info("Not found")
        else:
            for i in range(8):
                for j in range(8):
                    self.leds[i][j] = self.data[s][i*8+j]=='1'
            self.display()
        

    def load(self):
        """Loads all symbols from save"""
        print(savePath)
        with open(savePath, 'rb') as font:
            self.data = pk.load(font)

    def save(self):
        """Save the current symbol"""
        sym = self.symbol.get()
        if len(sym) != 1:
            print(sym)
            return
        sg = self.leds_as_string()
        if sg == '0'*8*8:
            return self.update_info("Empty symbol")
        self.data[sym] = sg
        with open(savePath, 'wb') as font:
            pk.dump(self.data, font)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pixel Font Editor")
    root.resizable(False, False)
    myApp = FontEditor(root)
    root.mainloop()
