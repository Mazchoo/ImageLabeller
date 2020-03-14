import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
import sys

cwd = sys.path[0]
if len(cwd) == 0:
    cwd = 'C:/Users/berta/Desktop/Python/Image Labeller/'
    sys.path.append(cwd)
else:
    cwd += '/'

from Lib.Utility_Functions import *

default_grid = 25
valid_image_extentions = ['.png','.jpg','.bmp']
ignore_sufixes = ['_labelled']
LARGE_FONT = ('Verdana',12)
NORM_FONT = ('Verdana',10)
SMALL_FONT = ('Verdana',8)

class FileSelect(tk.Frame):

    def __init__(self,root,label="",**kw):
        tk.Frame.__init__(self,root)
        self.root = root
        self.configure(**kw)
        self.setupMenu()

    def setupMenu(self):
        self.Label = tk.Label(self, text='Select Image :',font=LARGE_FONT)
        self.Label.config(width=14, anchor='center')
        self.btnBrowse = ttk.Button(self,text='Browse',command=self.browseFile,style='TButton')
        self.filenamebox = tk.Label(self, text = '',font=NORM_FONT)
        self.filenamebox.config(width=80)
        self.btnBrowse.config(width=10)
        self.Label.grid(row=0,column=0,pady=0,padx=10,sticky='ns')
        self.filenamebox.grid(row=0,column=1,pady=0,padx=10,sticky='ns')
        self.btnBrowse.grid(row=0,column=2,pady=0,padx=10,sticky='ns')

    def getCurrentFile(self):
        return Path(self.filenamebox.cget('text'))

    def setCurrentFile(self, input_string):
        self.filenamebox.configure(text = input_string)

    def isFileValid(self, file, old_file):
        if not(file.is_file()): popupmsg('That is not a file.'); return False
        if not(file.suffix in valid_image_extentions):
            popupmsg('No recognised image file has been selected.'); return False
        if str(file.parent) != str(old_file.parent):
            popupmsg('You must select a file in the same folder as the original.'); return False
        if file.stem.rfind('_labelled') != -1:
            popupmsg('The image should not end with the suffix _unlabelled.'); return False
        return True

    def browseFile(self):
        old_file = self.getCurrentFile()
        filename = filedialog.askopenfilename(filetypes=[('All File','*.*')])
        file = Path(filename)
        if self.root.start_labels:
            if not(self.isFileValid(file, old_file)): return False
            self.setCurrentFile(filename)
            self.root.current_frame.clear()
            self.root.current_frame.load()
        else:
            self.setCurrentFile(filename)
        return True