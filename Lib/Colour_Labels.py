import tkinter as tk
from tkinter import ttk
import numpy as np
import sys

cwd = sys.path[0] + '/'

from Lib.Utility_Functions import *

LARGE_FONT = ('Verdana', 12)
NORM_FONT = ('Verdana', 10)
SMALL_FONT = ('Verdana', 8)

class ColourSelect(tk.Frame):

    def __init__(self, root, controller, first_colour, **kw):
        tk.Frame.__init__(self, root)
        self.colour_list = []
        self.hex_names = []
        self.radio_buttons = []
        self.colour_buttons = []
        self.max_index = 0
        self.current_index = 0
        self.selection_var = tk.IntVar()
        self.root = root
        self.controller = controller
        self.packButtons(first_colour)
        self.configure(**kw)

    def addInitialButtons(self):
        self.labelframe = tk.LabelFrame(self, text="Select a Label")
        self.labelframe.pack(fill="both", expand="yes")
        self.add_button = ttk.Button(self.labelframe, text='+New Label',
            command=lambda: self.addNewLabel(), style='TButton')
        self.add_button.grid(row=0, column=0, columnspan = 2, sticky='w')

    def selectConsectiveLabel(self, offset):
        new_index = np.mod(self.current_index + offset, self.max_index)
        self.selectButton(new_index)

    def generateRandomColor(self):
        output_string = '#'
        output_string += ''.join([convertToHexStr(
            np.random.randint(0,256)) for i in range(3)])
        return output_string

    def addButton(self, colour_specified = None):
        if self.max_index == 255: return
        if not(colour_specified): colour_specified = self.generateRandomColor()
        self.hex_names.append(convertToHexStr(self.max_index))
        B = tk.Button(self.labelframe, text = ' ' * 6, bg = colour_specified)
        R = tk.Radiobutton(self.labelframe, variable = self.selection_var,
            text=self.hex_names[-1], value=self.max_index)
        R.val = self.max_index
        self.registerButton(R, R)
        self.registerButton(B, R)
        self.max_index += 1
        R.grid(row=self.max_index, column=0, sticky='ne')
        B.grid(row=self.max_index, column=1, sticky='w')
        self.radio_buttons.append(R)
        self.colour_buttons.append(B)
        self.colour_list.append(colour_specified)

    def addNewLabel(self):
        self.addButton()
        self.radio_buttons[-1].select()
        self.radio_buttons[self.current_index].select()
        self.controller.addNewLabel()

    def packButtons(self, first_colour):
        self.addInitialButtons()
        self.addButton(first_colour)

    def registerButton(self, target_button, button):
        target_button.config(command=lambda: self.selectButton(button.val))

    def selectButton(self, value):
        self.current_index = value
        self.radio_buttons[value].select()
        self.controller.setLabelIndex(value)
        self.controller.setCursorColour(self.colour_list[value])

    def getMetaDictionary(self):
        meta_dict = {}
        for i in range(self.max_index):
            meta_dict[self.hex_names[i]] = self.colour_list[i]
        return meta_dict

    def clearButtons(self):
        grid_list = self.labelframe.grid_slaves()
        for l in grid_list:
            l.destroy()
        self.destroy()

    def changeIndexedColour(self, new_colour, colour_ind = None):
        if not(colour_ind): colour_ind = self.current_index
        self.colour_list[colour_ind] = new_colour
        self.colour_buttons[colour_ind].configure(bg = new_colour)

    def loadColors(self, meta_dict):
        first_value = True
        for colour in meta_dict.values():
            if first_value:
                self.changeIndexedColour(colour, colour_ind = 0)
                first_value = False
            else: self.addButton(colour)
        self.radio_buttons[self.current_index].select()