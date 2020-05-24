import numpy as np
import keyboard, sys
from matplotlib.patches import Circle, Rectangle

cwd = sys.path[0] + '/'

from Lib.Event_Register import *
from Lib.Utility_Functions import *

class GridEvents(EventTracker):

    def __init__(self, axes, col, rad, alp, image, frame):
        super().__init__(axes, col, rad, alp, image, frame)
        self.height_cells = int((self.im_h - np.mod(self.im_h,rad))/rad)
        self.width_cells = int((self.im_w - np.mod(self.im_w,rad))/rad)
        self.loadAllLabels()

    def addNewLabel(self):
        self.labels.append(np.ndarray((self.height_cells, self.width_cells), dtype=np.bool))
        self.labels[-1].fill(False)

    def checkHotkeys(self):
        if keyboard.is_pressed('q'):
            self.frame.back_up(); return
        if keyboard.is_pressed('w'):
            self.frame.next_image(-1); return
        if keyboard.is_pressed('s'):
            self.frame.next_image(1); return
        if keyboard.is_pressed('a'):
            self.controller.offsetLabel(-1); return
        if keyboard.is_pressed('d'):
            self.controller.offsetLabel(1); return
        return False

    def updateLineData(self):
        self.lines[self.c_index].set_data(self.xs[self.c_index], self.ys[self.c_index])

    def checkCoordinatesInGrid(self, x, y):
        if (x > self.im_w - self.radius) or (y > self.im_h - self.radius):
            self.xs[self.c_index].pop(-1)
            self.ys[self.c_index].pop(-1)
            return True
        return False

    def removeLabelFromGrid(self, x_r, y_r):
        self.xs[self.c_index].pop(-1)
        self.ys[self.c_index].pop(-1)
        x_g = self.radius * x_r
        y_g = self.radius * y_r
        for c in self.circs[self.c_index]:
            if (x_g,y_g) == c.xy:
                c.remove()
                ind = self.circs[self.c_index].index(c)
                self.xs[self.c_index].pop(ind)
                self.ys[self.c_index].pop(ind)
                self.circs[self.c_index].pop(ind)
        self.labels[self.c_index][y_r,x_r] = False

    def addNewLabelToGrid(self, x_r, y_r, x, y):
        self.circs[self.c_index].append(Rectangle((x, y),
            width=self.radius, height=self.radius,
            color=self.col, alpha=self.label_alpha)
        )
        self.axes.add_patch(self.circs[self.c_index][-1])
        self.labels[self.c_index][y_r,x_r] = True

    def cursorEvent(self, event):
        x = event.xdata-np.mod(event.xdata,self.radius)
        y = event.ydata-np.mod(event.ydata,self.radius)
        if self.checkCoordinatesInGrid(x, y): return False
        x_r, y_r = self.pixelsToGrid(x,y)
        if self.labels[self.c_index][y_r,x_r]:
            self.removeLabelFromGrid(x_r, y_r)
        else:
            self.addNewLabelToGrid(x_r, y_r, x, y)
        return True

    def deleteEvent(self, x, y):
        x_r, y_r = self.pixelsToGrid(x,y)
        self.labels[self.c_index][y_r,x_r] = False;
        circ = self.circs[self.c_index].pop(-1)
        circ.remove()

    def drawBackCircle(self, ind):
        x = self.xs[self.c_index][ind]-np.mod(self.xs[self.c_index][ind],self.radius)
        y = self.ys[self.c_index][ind]-np.mod(self.ys[self.c_index][ind],self.radius)
        self.circs[self.c_index].append(Rectangle((x, y),
            width=self.radius, height=self.radius,
            color=self.col, alpha=self.label_alpha)
        )

    def drawSquareBackOnGrid(self, i, j, k):
        self.xs[k].append(j*self.radius)
        self.ys[k].append(i*self.radius)
        self.circs[k].append(Rectangle((self.xs[k][-1], self.ys[k][-1]),
            width=self.radius, height=self.radius,
            color=self.col, alpha=self.label_alpha)
        )
        self.axes.add_patch(self.circs[k][-1])

    def showLabelData(self):
        for k in range(self.n_colours):
            self.col = getEventColor(self, k)
            for i in range(len(self.labels[k])):
                for j in range(len(self.labels[k][0])):
                    if self.labels[k][i,j]:
                        self.drawSquareBackOnGrid(i, j, k)
        self.col = getEventColor(self)

    def pixelsToGrid(self,x,y):
        x_r = int(x/self.radius)
        y_r = int(y/self.radius)
        if x_r >= self.width_cells: x_r = self.width_cells - 1
        if y_r >= self.height_cells: y_r = self.height_cells - 1
        return x_r, y_r

    def setCursorWeight(self, rad):
        pass

    def preprocessLabel(self, input_labels):
        labels = []
        for label in input_labels:
            buffer = np.array(label, dtype = np.bool)
            labels.append(np.ndarray((self.height_cells,self.width_cells),
                buffer = buffer, dtype = np.bool))
        while len(labels) < self.n_colours:
            label = np.ndarray((self.height_cells, self.width_cells), dtype=np.bool)
            label.fill(False)
            labels.append(label)
        return labels