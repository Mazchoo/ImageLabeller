import tkinter as tk
from tkinter import ttk
import sys

cwd = sys.path[0] + '/'

from Lib.Pages import *
from Lib.Utility_Functions import *

default_grid = 50
valid_image_extentions = ['.png','.jpg','.bmp']
ignore_sufixes = ['_labelled']
LARGE_FONT = ('Verdana',12)
NORM_FONT = ('Verdana',10)
SMALL_FONT = ('Verdana',8)
BUTTON_FONT = ('Arial', 12)

class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.setupWindow()
        self.setupParameters()
        self.setupContainer()
        self.initialiseMenuBar()
        self.initialiseFileMenu()
        self.intialiseOptionMenu()
        self.initialiseHelpMenu()
        self.initialiseTopBar()
        self.initialiseFrames()

    def initialiseMenuBar(self):
        self.MenuBar = tk.Menu(self.container)

    def initialiseFileMenu(self):
        self.FileMenu = tk.Menu(self.MenuBar, tearoff=0)
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label='Exit', command = lambda: self.destroy())

    def setupWindow(self):
        tk.Tk.iconbitmap(self, default=cwd+'Graphics/Icon.ico')
        tk.Tk.wm_title(self, 'Grid Image Labeller')
        ttk.Style().configure('TButton', padding=6, relief='flat',
            background='#000', font=BUTTON_FONT)

    def setupParameters(self):
        self.gridSize = default_grid
        self.placeholder_entry = ''
        self.start_labels = False

    def setupContainer(self):
        self.container = tk.Frame(self)
        self.container.pack(side='top',fill='both',expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def intialiseOptionMenu(self):
        self.OptionMenu = tk.Menu(self.MenuBar,tearoff=1)
        self.addCursorColorMenu()
        self.addCursorWidthMenu()
        self.addCursorAlphaMenu()
        self.addLineWithMenu()
        self.addCursorTogMenu()
        self.addGridColMenu()
        self.addGridWidthMenu()

    def addCursorTogMenu(self):
        CursorTogMenu = tk.Menu(self, tearoff=0)
        CursorTogMenu.add_command(label='Cursor On',
            command = lambda: self.togglePatches(True))
        CursorTogMenu.add_command(label='Cursor Off',
            command = lambda: self.togglePatches(False))
        self.OptionMenu.add_cascade(label='Toggle cursor',menu=CursorTogMenu)

    def addGridWidthMenu(self):
        GridWidthMenu = tk.Menu(self,tearoff=0)
        GridWidthMenu.add_command(label='0.0 px', command = lambda: self.setGridWeight(0.0))
        GridWidthMenu.add_command(label='0.5 px', command = lambda: self.setGridWeight(0.5))
        GridWidthMenu.add_command(label='1.0 px', command = lambda: self.setGridWeight(1))
        GridWidthMenu.add_command(label='1.5 px', command = lambda: self.setGridWeight(1.5))
        GridWidthMenu.add_command(label='2.0 px', command = lambda: self.setGridWeight(2))
        GridWidthMenu.add_command(label='2.5 px', command = lambda: self.setGridWeight(2.5))
        GridWidthMenu.add_command(label='3.0 px', command = lambda: self.setGridWeight(3))
        GridWidthMenu.add_command(label='3.5 px', command = lambda: self.setGridWeight(3.5))
        GridWidthMenu.add_command(label='4.0 px', command = lambda: self.setGridWeight(4))
        self.OptionMenu.add_cascade(label='Grid width', menu=GridWidthMenu)

    def addGridColMenu(self):
        GridColMenu = tk.Menu(self,tearoff=0)
        GridColMenu.add_command(label='Blue', command = lambda: self.setGridColour('#6e80f4'))
        GridColMenu.add_command(label='Green', command = lambda: self.setGridColour('#a8f46e'))
        GridColMenu.add_command(label='Red', command = lambda: self.setGridColour('#f4806e'))
        GridColMenu.add_command(label='Cyan', command = lambda: self.setGridColour('#5befe0'))
        GridColMenu.add_command(label='Magenta', command = lambda: self.setGridColour('#ea5bef'))
        GridColMenu.add_command(label='Yellow', command = lambda: self.setGridColour('#efe55b'))
        GridColMenu.add_command(label='Black', command = lambda: self.setGridColour('#070707'))
        GridColMenu.add_command(label='White', command = lambda: self.setGridColour('#f9f9f9'))
        GridColMenu.add_command(label='Custom', command = lambda: self.addCustomGridColor())
        self.OptionMenu.add_cascade(label='Grid colour', menu=GridColMenu)

    def addLineWithMenu(self):
        LinWidthMenu = tk.Menu(self,tearoff=0)
        LinWidthMenu.add_command(label='0.0 px', command = lambda: self.setLineWeight(0.0))
        LinWidthMenu.add_command(label='0.5 px', command = lambda: self.setLineWeight(0.5))
        LinWidthMenu.add_command(label='1.0 px', command = lambda: self.setLineWeight(1))
        LinWidthMenu.add_command(label='1.5 px', command = lambda: self.setLineWeight(1.5))
        LinWidthMenu.add_command(label='2.0 px', command = lambda: self.setLineWeight(2))
        LinWidthMenu.add_command(label='2.5 px', command = lambda: self.setLineWeight(2.5))
        LinWidthMenu.add_command(label='3.0 px', command = lambda: self.setLineWeight(3))
        LinWidthMenu.add_command(label='3.5 px', command = lambda: self.setLineWeight(3.5))
        LinWidthMenu.add_command(label='4.0 px', command = lambda: self.setLineWeight(4))
        self.OptionMenu.add_cascade(label='Line width', menu=LinWidthMenu)

    def addCursorColorMenu(self):
        CursorColMenu = tk.Menu(self,tearoff=0)
        CursorColMenu.add_command(label='Blue',
            command = lambda: self.setCursorColour('#6e80f4'))
        CursorColMenu.add_command(label='Green',
            command = lambda: self.setCursorColour('#a8f46e'))
        CursorColMenu.add_command(label='Red',
            command = lambda: self.setCursorColour('#f4806e'))
        CursorColMenu.add_command(label='Cyan',
            command = lambda: self.setCursorColour('#5befe0'))
        CursorColMenu.add_command(label='Magenta',
            command = lambda: self.setCursorColour('#ea5bef'))
        CursorColMenu.add_command(label='Yellow',
            command = lambda: self.setCursorColour('#efe55b'))
        CursorColMenu.add_command(label='Black',
            command = lambda: self.setCursorColour('#070707'))
        CursorColMenu.add_command(label='White',
            command = lambda: self.setCursorColour('#f9f9f9'))
        CursorColMenu.add_command(label='Custom',
            command = lambda: self.addCustomCursorColor())
        self.OptionMenu.add_cascade(label='Cursor colour', menu=CursorColMenu)

    def addCursorWidthMenu(self):
        CursorWidthMenu = tk.Menu(self,tearoff=0)
        CursorWidthMenu.add_command(label='4.0 px', command = lambda: self.setCursorWeight(2))
        CursorWidthMenu.add_command(label='8.0 px', command = lambda: self.setCursorWeight(4))
        CursorWidthMenu.add_command(label='10.0 px', command = lambda: self.setCursorWeight(5))
        CursorWidthMenu.add_command(label='12.0 px', command = lambda: self.setCursorWeight(6))
        CursorWidthMenu.add_command(label='14.0 px', command = lambda: self.setCursorWeight(7))
        CursorWidthMenu.add_command(label='16.0 px', command = lambda: self.setCursorWeight(8))
        CursorWidthMenu.add_command(label='20.0 px', command = lambda: self.setCursorWeight(10))
        CursorWidthMenu.add_command(label='28.0 px', command = lambda: self.setCursorWeight(14))
        self.OptionMenu.add_cascade(label='Cursor diameter', menu=CursorWidthMenu)

    def addCursorAlphaMenu(self):
        CursorAlphaMenu = tk.Menu(self,tearoff=0)
        CursorAlphaMenu.add_command(label='12.5 %',
            command = lambda: self.setCursorAlpha(0.125))
        CursorAlphaMenu.add_command(label='25.0 %',
            command = lambda: self.setCursorAlpha(0.25))
        CursorAlphaMenu.add_command(label='37.5 %',
            command = lambda: self.setCursorAlpha(0.375))
        CursorAlphaMenu.add_command(label='50.0 %',
            command = lambda: self.setCursorAlpha(0.5))
        CursorAlphaMenu.add_command(label='62.5 %',
            command = lambda: self.setCursorAlpha(0.625))
        CursorAlphaMenu.add_command(label='75.0 %',
            command = lambda: self.setCursorAlpha(0.75))
        CursorAlphaMenu.add_command(label='87.5 %',
            command = lambda: self.setCursorAlpha(0.875))
        CursorAlphaMenu.add_command(label='100.0 %',
            command = lambda: self.setCursorAlpha(1))
        self.OptionMenu.add_cascade(label='Cursor opacity',menu=CursorAlphaMenu)

    def addCustomGridColor(self):
        callback = lambda: self.evaluateCustomGridColor()
        enterValue(self, 'Grid Color', callback)

    def addCustomCursorColor(self):
        callback = lambda: self.evaluateCustomCursorColor()
        enterValue(self, 'Grid Color', callback)

    def checkHexValue(self):
        valid_entry = True
        if not(isinstance(self.placeholder_entry, str)):
            valid_entry = False; print('Not string.')
        elif len(self.placeholder_entry) != 7:
            valid_entry = False; print('Wrong length.')
        elif self.placeholder_entry[0] != '#':
            valid_entry = False; print('First character is not hash.')
        else:
            try:
                int_hex = int('0x' + self.placeholder_entry[1:], 16)
                if int_hex > 16777215:
                    valid_entry = False; print('Hex value is too high.')
            except:
                valid_entry = False; print('Could not treat value as hex.')
        if not(valid_entry):
            popupmsg('The colour should be a 24-bit hex value.\n' +
                '  >>  e.g #a1b657\nYou can look up the "color picker" online.')
        return valid_entry

    def evaluateCustomGridColor(self):
        if self.checkHexValue(): self.setGridColour(self.placeholder_entry)

    def evaluateCustomCursorColor(self):
        if self.checkHexValue(): self.setCursorColour(self.placeholder_entry)

    def initialiseTopBar(self):
        self.MenuBar.add_cascade(label='File', menu=self.FileMenu)
        self.MenuBar.add_cascade(label='Options', menu=self.OptionMenu)
        self.MenuBar.add_cascade(label='Help', menu=self.HelpMenu)
        tk.Tk.config(self, menu=self.MenuBar)

    def initialiseHelpMenu(self):
        self.HelpMenu = tk.Menu(self.MenuBar, tearoff=1)
        self.HelpMenu.add_command(label = 'Doccumentation', command = lambda: popupmsg(
            'See the following github page for doccumentation.\n' +
            'www.github.com/something'))

    def initialiseFrames(self):
        self.frames = {}
        frames = (StartPage, SingleCellPage, BoundingBoxPage, PolygonRegionPage)
        for F in frames:
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0,column=0, sticky = 'nsew')
        self.current_frame = self.frames[StartPage]
        self.showFrame(StartPage, force_load=True)

    def showFrame(self, new_page, log='', force_load=False):
        if len(log)>0:
            print(log)
        file = self.getImageFile()
        print(file)
        if file.is_file() or force_load:
            if (file.suffix in valid_image_extentions) or force_load:
                self.current_frame.clear()
                self.current_frame = self.frames[new_page]
                self.current_frame.load()
                self.current_frame.tkraise()
            else:
                popupmsg('No recognised image file has been selected.')
        else:
            popupmsg('No valid file has been selected.')

    def setLineColour(self, col):
        self.current_frame.line_col = col
        self.setLineColor(col)

    def setLineWeight(self, weight):
        self.current_frame.line_weight = weight
        self.setLineWidth(weight)

    def setCursorColour(self, col):
        self.current_frame.cursor_col = col
        self.current_frame.events.setCursorColour(col)
        self.current_frame.colour_bar.changeIndexedColour(col)

    def setCursorWeight(self, weight):
        self.current_frame.cursor_weight = weight
        self.current_frame.events.setCursorWeight(weight)

    def setCursorAlpha(self, alp):
        self.current_frame.cursor_alpha = alp
        self.current_frame.events.setCursorAlpha(alp)

    def togglePatches(self, toggle):
        self.current_frame.events.setTogglePatches(toggle)

    def setGridSize(self, size):
        size = int(size)
        if size <= 0:
            popupmsg('Grid size entered must be a positive integer.'); return
        self.gridSize = size
        self.current_frame.drawGrid()

    def setGridColour(self, col):
        self.current_frame.grid_col = col
        self.current_frame.drawGrid()

    def setGridWeight(self, weight):
        self.current_frame.grid_weight = weight
        self.current_frame.drawGrid()

    def updatePlaceholder(self, win, value, callback):
        self.placeholder_entry = value
        win.destroy()
        callback()

    def getImageFile(self):
        return Path(self.frames[StartPage].fileSelect.getCurrentFile())

    def setFile(self, filename):
        self.frames[StartPage].fileSelect.setCurrentFile(filename)

    def setLabelIndex(self, value):
        self.current_frame.events.updateColourIndex(value)

    def addNewLabel(self):
        self.current_frame.events.addNewLine()
        self.current_frame.events.addNewLabel()

    def offsetLabel(self, offset):
        self.current_frame.color_bar.selectConsectiveLabel(offset)

    def exit(self):
        self.quit()
        self.destroy()