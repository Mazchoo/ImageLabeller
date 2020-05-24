import tkinter as tk
from tkinter import ttk
import sys, json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import use; use('TkAgg')
from matplotlib import style; style.use('dark_background')
from pathlib import Path
from os import listdir
from os.path import isfile, join

cwd = sys.path[0] + '/'

from Lib.File_Selection import *
from Lib.Colour_Labels import *
from Lib.Event_Register import *
from Lib.BoundingBox_Events import *
from Lib.Polygon_Events import *
from Lib.Grid_Events import *

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.setupDefaultColours()

        self.loadFileSelection()
        self.loadTopButtons()
        self.loadColorSelection()
        self.loadImageCanvas()

        self.initialiseImageData()

    def prepareRightBar(self):
        right = tk.Frame(self)
        right.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        return right

    def loadNewColourBar(self):
        self.colour_bar = ColourSelect(self.right_bar, self.controller, self.cursor_col)
        self.colour_bar.pack(in_=self.right_bar, side = 'top', padx=0, pady=10)

    def loadColorSelection(self):
        self.right_bar = self.prepareRightBar()
        self.loadNewColourBar()

    def loadFileSelection(self):
        bottom = self.prepareBottomBar()
        self.fileSelect = FileSelect(self.controller)
        self.fileSelect.pack(in_=bottom, side='bottom', fill=tk.BOTH, expand=True, pady=0)

    def loadTopButtons(self):
        top = self.prepareTopBar()
        buttons = self.createTopButtons()
        self.packButtonsInBar(buttons, top)

    def loadImageCanvas(self):
        left = self.prepareLeftBar()
        self.drawImageCanvas(left)

    def initialiseImageData(self):
        self.events = None
        self.image = None
        self.gridlines = []
        self.files = []
        self.im_folder = ''
        self.im_labels = {}
        self.init_dict = {}
        self.file_index = 0
        self.already_labelled = False
        self.saveImage = False

    def drawImageCanvas(self, bar):
        self.fig = Figure(figsize=(16,10),dpi=100)
        self.axes = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(in_=bar,side='top')
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.canvas._tkcanvas.pack(side='top')

    def setupDefaultColours(self):
        self.line_col = '#00ff00'
        self.line_weight = 1
        self.cursor_alpha = 1.0
        self.cursor_col = '#00ff00'
        self.cursor_weight = 4
        self.grid_col = "#ffffff"
        self.grid_weight = 1

    def prepareTopBar(self):
        top = tk.Frame(self)
        top.pack(side=tk.TOP)
        return top

    def createTopButtons(self):
        buttons =[]
        buttons.append(ttk.Button(self, text='Single Cell',
            command=lambda: self.controller.showFrame(
            SingleCellPage, log='Single Cell running...'), style='TButton'))
        buttons.append(ttk.Button(self,text='Bounded Rectangle',
            command=lambda: self.controller.showFrame(
            BoundingBoxPage, log='Bounded Rectangle running...'), style='TButton'))
        buttons.append(ttk.Button(self,text='Bounded Region',
            command=lambda: self.controller.showFrame(
            PolygonRegionPage, log='Bounded Region running...'), style='TButton'))
        grid_entry = tk.Entry(self, justify='center', font=LARGE_FONT, width=6, bd=5)
        buttons.append(ttk.Button(self, text='Set Grid',
            command = lambda: self.controller.setGridSize(grid_entry.get()), style='TButton'))
        buttons.append(grid_entry)
        buttons[-1].insert(0, str(self.controller.gridSize))
        buttons.append(ttk.Button(self, text='Exit Program',
            command = lambda: self.controller.exit(), style='TButton'))
        return buttons

    def packButtonsInBar(self, buttons, bar):
        for button in buttons: button.pack(in_=bar, side='left', padx=10)

    def prepareBottomBar(self):
        bottom = tk.Frame(self)
        bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        return bottom

    def prepareLeftBar(self):
        left = tk.Frame(self)
        left.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        return left

    def clear(self):
        self.axes.cla()
        if not(self.events is None): self.events.clear()
        del self.events

    def drawGrid(self):
        self.axes.autoscale(enable=False)
        im_h, im_w = len(self.image), len(self.image[0])
        gs = self.controller.gridSize
        for i in range(len(self.gridlines)):
            line = self.gridlines.pop(-1)
            line.remove()
        for i in np.arange(0,im_h-np.mod(im_h, gs),step=gs):
            line = self.axes.plot((0,im_w-1), (i,i), '--',
                linewidth=self.grid_weight, color=self.grid_col)[0]
            self.gridlines.append(line)
        for i in np.arange(0,im_w-np.mod(im_w, gs),step=gs):
            line =  self.axes.plot((i,i), (0,im_h-1), '--',
                linewidth=self.grid_weight, color=self.grid_col)[0]
            self.gridlines.append(line)
        line.figure.canvas.draw()
        self.axes.autoscale(enable=True)

    def load(self):
        self.image = plt.imread(cwd+'Graphics/splash.jpg')
        self.drawGrid()
        self.axes.imshow(self.image)
        self.events = EventTracker(self.axes, self.cursor_col,
            self.cursor_weight, self.cursor_alpha, self.image, self)
        self.colour_bar.selectButton(self.events.c_index)
        self.toolbar.update()
        self.canvas.draw()

    def addNewLine(self):
        line, = self.axes.plot([0], [0], color=self.line_col, linewidth=self.line_weight)
        return line

    def softBackup(self):
        file = self.controller.getImageFile()
        self.im_labels[file.name] = [label.tolist() for label in self.events.labels]
        self.im_labels['meta'] = self.colour_bar.getMetaDictionary()

    def hardBackup(self):
        gs = self.controller.gridSize
        with open(self.getSaveDictionaryName(), 'w') as fp:
            json.dump(self.im_labels, fp, indent = 4)

    def makeBackup(self):
        self.softBackup()
        self.hardBackup()

    def loadLabelImages(self):
        self.controller.start_labels = True
        file = self.controller.getImageFile()
        self.im_folder = str(file.parents[0])
        self.files = [f for f in listdir(self.im_folder) if isfile(
            join(self.im_folder, f)) if Path(f).suffix in valid_image_extentions and not f[
            f.rfind('_'):f.rfind('.')] in ignore_sufixes]
        self.file_index = self.files.index(file.name)
        gs = self.controller.gridSize
        dict_path = self.getSaveDictionaryName()
        if Path(dict_path).is_file():
            with open(dict_path, 'r') as fp:
                self.im_labels = json.loads(fp.read())
            self.init_dict = self.im_labels.copy()
            self.colour_bar.clearButtons()
            self.loadNewColourBar()
            self.colour_bar.loadColors(self.im_labels['meta'])
            print('There is a json!')
        else:
            print('No json file yet.')
        self.loadNewImage(file)

    def loadNewImage(self, file):
        if file.name in self.im_labels.keys():
            self.already_labelled = True
        else:
            self.already_labelled = False
        self.image = plt.imread(str(self.controller.getImageFile()))
        self.drawGrid()
        self.axes.imshow(self.image)
        if self.already_labelled:
            self.axes.set_ylabel(file.stem[:40] + ' {' + file.suffix + '} ' + ' {labelled}')
        else:
            self.axes.set_ylabel(file.stem[:40] + ' {' + file.suffix + '} ' + ' {unlabelled}')
        self.loadEvents()
        if self.already_labelled:
            self.events.loadLabel(self.im_labels[file.name])
        self.toolbar.update()
        self.canvas.draw()

    def loadEvents(self):
        self.events = EventTracker(self.axes, self.cursor_col,
            self.controller.gridSize, self.cursor_alpha, self.image, self)

    def nextImage(self, ind):
        self.file_index += ind
        self.file_index = np.mod(self.file_index, len(self.files))
        self.makeBackup()
        file =  self.im_folder + '/' + self.files[self.file_index]
        self.controller.setFile(file)
        p_file = Path(file)
        self.clear()
        self.loadNewImage(p_file)

    def saveCSV(self, lines_in_batch, update_only, file_name):
        '''
        Writes lines of a csv to file using the current label dictionary.

        The 'lines_in_batch' parameter is just introduced for speed to reduce
        the number of I/O writes.

        The dictionary can be updated with the 'update_only' parameter which
        means that only newly labelled images will be updated.

        The 'file_name' parameter is a string with the name of where the
        file should be saved.
        '''
        self.makeBackup()
        save_name = self.im_folder + '/' + file_name + '.csv'
        line = ''
        current_line_number = 0
        for key in self.im_labels.keys():
            if not(update_only) or not(key in self.init_dict):
                data = [key] + list(self.im_labels[key].ravel())
                line += str(data).replace(" ","").replace("[","").replace(
                    "]","").replace("'","")+"\n"
                current_line_number += 1
            if current_line_number >= lines_in_batch:
                f_handle = open(save_name,'a')
                f_handle.write(line)
                f_handle.close()
                i_lin = 0
                line = ''
        f_handle = open(save_name,'a')
        f_handle.write(line)
        f_handle.close()

    def getSaveDictionaryName(self):
        return 'error'

class SingleCellPage(StartPage):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

    def createTopButtons(self):
        buttons = []
        buttons.append(ttk.Button(self,text='Back up',
            command=lambda: self.makeBackup(), style='TButton'))
        buttons.append(ttk.Button(self,text='Previous Image',
            command=lambda: self.nextImage(-1), style='TButton'))
        buttons.append(ttk.Button(self,text='Next Image',
            command=lambda: self.nextImage(1), style='TButton'))
        buttons.append(ttk.Button(self, text='Update CSV',
            command = lambda: self.saveCSV(n_lines, True,
            'grid_labels_' + str(self.controller.gridSize)), style='TButton'))
        buttons.append(ttk.Button(self, text='Save CSV',
            command = lambda: self.saveCSV(n_lines, False,
            'grid_labels_' + str(self.controller.gridSize)), style='TButton'))
        buttons.append(ttk.Button(self, text='Go Back',
            command = lambda: self.controller.showFrame(
            StartPage, log='Main menu loading...'), style='TButton'))
        buttons.append(ttk.Button(self, text='Exit Program',
            command = lambda: self.controller.exit(), style='TButton'))
        return buttons

    def setupDefaultColours(self):
        self.line_col = '#00ff00'
        self.line_weight = 1
        self.cursor_col = '#00ff00'
        self.cursor_weight = 4
        self.cursor_alpha = 0.5
        self.grid_col = "w"
        self.grid_weight = 1

    def load(self):
        self.loadLabelImages()

    def loadEvents(self):
        self.events = GridEvents(self.axes, self.cursor_col,
            self.controller.gridSize, self.cursor_alpha, self.image, self)

    def loadFileSelection(self):
        pass

    def clear(self):
        self.gridlines = []
        self.axes.cla()
        self.events.clear()
        del self.events

    def getSaveDictionaryName(self):
        return self.im_folder+'/grid_labels_' + str(self.controller.gridSize) + '.json'

class BoundingBoxPage(StartPage):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

    def createTopButtons(self):
        buttons = []
        buttons.append(ttk.Button(self,text='Back up',
            command=lambda: self.makeBackup(), style='TButton'))
        buttons.append(ttk.Button(self,text='Previous Image',
            command=lambda: self.nextImage(-1), style='TButton'))
        buttons.append(ttk.Button(self,text='Next Image',
            command=lambda: self.nextImage(1), style='TButton'))
        buttons.append(ttk.Button(self, text='Update CSV',
            command = lambda: self.saveCSV(n_lines, True,
            'grid_labels_' + str(self.controller.gridSize)), style='TButton'))
        buttons.append(ttk.Button(self, text='Save CSV',
            command = lambda: self.saveCSV(n_lines, False,
            'grid_labels_' + str(self.controller.gridSize)), style='TButton'))
        buttons.append(ttk.Button(self, text='Go Back',
            command = lambda: self.controller.showFrame(
            StartPage, log='Main menu loading...'), style='TButton'))
        buttons.append(ttk.Button(self, text='Exit Program',
            command = lambda: self.controller.exit(), style='TButton'))
        return buttons

    def setupDefaultColours(self):
        self.line_col = '#00ff00'
        self.line_weight = 1
        self.cursor_col = '#00ff00'
        self.cursor_weight = 1
        self.cursor_alpha = 0.5
        self.grid_col = "#ffffff"
        self.grid_weight = 1

    def load(self):
        self.loadLabelImages()

    def loadEvents(self):
        self.events = BoundingBoxEvents(self.axes, self.cursor_col,
            self.cursor_weight, self.cursor_alpha, self.image, self)

    def loadFileSelection(self):
        pass

    def clear(self):
        self.gridlines = []
        self.axes.cla()
        self.events.clear()
        del self.events

    def getSaveDictionaryName(self):
        return self.im_folder+'/bounding_box_labels.json'

class PolygonRegionPage(StartPage):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.save_image = False

    def createTopButtons(self):
        buttons = []
        buttons.append(ttk.Button(self,text='Back up',
            command=lambda: self.makeBackup(), style='TButton'))
        buttons.append(ttk.Button(self,text='Previous Image',
            command=lambda: self.nextImage(-1), style='TButton'))
        buttons.append(ttk.Button(self,text='Next Image',
            command=lambda: self.nextImage(1), style='TButton'))
        buttons.append(ttk.Button(self, text='Save Images',
            command = lambda: self.toggleSaveImage(), style='TButton'))
        buttons.append(ttk.Button(self, text='Close Region',
            command = lambda: self.events.togglePolygon() , style='TButton'))
        buttons.append(ttk.Button(self, text='Go Back',
            command = lambda: self.controller.showFrame(
            StartPage, log='Main menu loading...'), style='TButton'))
        buttons.append(ttk.Button(self, text='Exit Program',
            command = lambda: self.controller.exit(), style='TButton'))
        return buttons

    def setupDefaultColours(self):
        self.line_col = '#ff00ff'
        self.line_weight = 1
        self.cursor_col = '#ff00ff'
        self.cursor_weight = 1
        self.cursor_alpha = 1.
        self.grid_col = "w"
        self.grid_weight = 0

    def load(self):
        self.loadLabelImages()

    def loadEvents(self):
        self.events = PolygonEvents(self.axes, self.cursor_col,
            self.cursor_weight, self.cursor_alpha, self.image, self)

    def loadFileSelection(self):
        pass

    def clear(self):
        self.gridlines = []
        self.axes.cla()
        self.events.clear()

    def makeBackup(self):
        self.softBackup()
        self.hardBackup()
        if self.save_image:
            self.saveLabel()

    def softBackup(self):
        file = self.controller.getImageFile()
        self.im_labels[file.name] = [[
            l.tolist() for l in label] for label in self.events.labels]
        self.im_labels['meta'] = self.colour_bar.getMetaDictionary()

    def saveLabel(self):
        fig = self.events.genImage()
        file = self.controller.getImageFile()
        save_name = self.im_folder+'/'+file.stem+'_labelled'+file.suffix
        fig.savefig(save_name, bbox_inches='tight', pad_inches=0)
        plt.close(fig)

    def toggleSaveImage(self):
        self.save_image = not self.save_image
        if self.save_image:
            popupmsg('Images will now be saved.')
        else:
            popupmsg('Images will now not be saved.')

    def getSaveDictionaryName(self):
        return self.im_folder+'/polygon_region_labels.json'