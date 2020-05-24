import numpy as np
import keyboard, sys
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt

cwd = sys.path[0] + '/'

from Lib.Event_Register import *
from Lib.Utility_Functions import *

class PolygonEvents(EventTracker):

    def __init__(self, axes, col, rad, alp, image, frame):
        super().__init__(axes, col, rad, alp, image, frame)
        self.canvas_image = np.zeros((self.im_h,self.im_w), dtype = np.uint8)
        self.filled_polygons = []
        self.drawn_polygons = []
        self.loadAllLabels()

    def addNewLabel(self):
        colour_ind = len(self.labels)
        self.labels.append([])
        self.filled_polygons.append(False)
        self.drawn_polygons.append(Polygon(np.array([[0,0]], dtype = np.uint16),
            closed=True, color = getEventColor(self, colour_ind)))

    def cursorEvent(self, event):
        x = np.uint16(np.floor(event.xdata))
        y = np.uint16(np.floor(event.ydata))
        self.labels[self.c_index].append(np.array([x,y], dtype = np.uint16))
        self.addCircle(x, y, self.c_index)
        self.drawn_polygons[self.c_index].set_xy(self.labels[self.c_index])
        self.updateLineData()

    def deleteEvent(self, x, y):
        if len(self.xs) != 0:
            self.labels[self.c_index] = self.labels[self.c_index][:-1]
            if len(self.labels[self.c_index]) > 0:
                self.drawn_polygons[self.c_index].set_xy(self.labels[self.c_index])
        else:
            self.drawn_polygons[self.c_index].set_xy(np.array([[0,0]], dtype = np.uint16))
            self.labels[self.c_index] = self.labels[self.c_index][:-1]
        circ = self.circs[self.c_index].pop(-1)
        circ.remove()
        self.updateLineData()

    def showLabelData(self):
        for k in range(len(self.labels)):
            self.col = getEventColor(self, k)
            label_len = len(self.labels[k])
            self.xs[k] = [self.labels[k][i][0] for i in range(label_len)]
            self.ys[k] = [self.labels[k][i][1] for i in range(label_len)]
            self.lines[k].set_color(self.col)
            self.updateLineData(k)
            if label_len != 0:
                self.drawn_polygons[k].set_xy(self.labels[k])
            for label in self.labels[k]:
                self.addCircle(label[0], label[1], k)
        self.col = getEventColor(self)

    def togglePolygon(self):
        if self.filled_polygons[self.c_index]:
            self.drawn_polygons[self.c_index].remove()
        else:
            self.axes.add_patch(self.drawn_polygons[self.c_index])
        self.filled_polygons[self.c_index] = not self.filled_polygons[self.c_index]
        self.draw()

    def genImage(self):
        fig, axes = plt.subplots(nrows=1, ncols=1)
        image = np.dstack([self.canvas_image] * 3)
        axes = plt.axes()
        axes.imshow(image)
        for k in range(self.n_colours):
            try:
                axes.add_patch(self.drawn_polygons[k])
            except:
                print('Label region', k, 'failed.')
        axes.axis('off')
        return fig

    def setCursorColour(self, col):
        self.col = col
        for c in self.circs[self.c_index]:
            c.set_color(col)
        self.lines[self.c_index].set_color(col)
        self.drawn_polygons[self.c_index].set_color(col)
        self.draw()

    def preprocessLabel(self, input_labels):
        labels = [[np.array(l, dtype = np.uint16) for l in label] for label in input_labels]
        loop_ind = len(labels)
        while len(labels) < self.n_colours:
            labels.append([])
            self.filled_polygons.append(False)
            self.drawn_polygons.append(Polygon(np.array([[0,0]], dtype = np.uint16),
                closed=True, color = getEventColor(self, loop_ind)))
            loop_ind += 1
        return labels