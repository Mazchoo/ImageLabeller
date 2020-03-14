import numpy as np
import keyboard, sys
from matplotlib.patches import Circle, Rectangle

cwd = sys.path[0]
if len(cwd) == 0:
    cwd = 'C:/Users/berta/Desktop/Python/Image Labeller/'
    sys.path.append(cwd)
else:
    cwd += '/'

from Lib.Event_Register import *
from Lib.Utility_Functions import *

class BoundingBoxEvents(EventTracker):

    def __init__(self, axes, col, rad, alp, image, frame):
        super().__init__(axes, col, rad, alp, image, frame)
        self.loadAllLabels()

    def addNewLabel(self):
        self.labels.append(np.ndarray((2,2), dtype = np.uint16))
        self.labels[-1].fill(0)

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

    def addFirstPoint(self, x, y):
        self.addCircle(x, y)
        self.labels[self.c_index][0,0] = x
        self.labels[self.c_index][0,1] = y

    def addSecondPoint(self, x, y):
        self.addCircle(x, y)
        self.addCircle(self.xs[self.c_index][0], y)
        self.addCircle(x, self.ys[self.c_index][0])
        self.circs[self.c_index].append(Rectangle(
            (np.min([x,self.xs[self.c_index][0]]), np.min([y,self.ys[self.c_index][0]])),
            height=np.max([y,self.ys[self.c_index][0]])-np.min([y,self.ys[self.c_index][0]]),
            width=np.max([x,self.xs[self.c_index][0]])-np.min([x,self.xs[self.c_index][0]]),
            color=self.col, alpha=self.label_alpha)
        )
        self.axes.add_patch(self.circs[self.c_index][-1])
        self.labels[self.c_index][1,0] = x
        self.labels[self.c_index][1,1] = y

    def cursorEvent(self, event):
        if len(self.xs[self.c_index]) > 2:
            self.xs[self.c_index].pop(-1)
            self.ys[self.c_index].pop(-1)
        else:
            x = np.uint16(np.floor(event.xdata))
            y = np.uint16(np.floor(event.ydata))
            self.xs[self.c_index][-1] = x
            self.ys[self.c_index][-1] = y
            if len(self.xs[self.c_index]) == 1:
                self.addFirstPoint(x, y)
            else:
                self.addSecondPoint(x,y)

    def checkRightClickEvent(self, event):
        if event.button == 3:
            if len(self.xs[self.c_index])>0:
                x = self.xs[self.c_index].pop(-1)
                y = self.ys[self.c_index].pop(-1)
                self.deleteEvent(x, y)
                self.draw()
                return True
        return False

    def deleteEvent(self, x, y):
        n_events = len(self.xs[self.c_index])
        if n_events == 1:
            [self.circs[self.c_index][-i].remove() for i in range(1,5)]
            self.circs[self.c_index] = self.circs[self.c_index][:1]
            self.labels[self.c_index] *= 0
        elif n_events == 0:
            circ = self.circs[self.c_index].pop(-1)
            circ.remove()
        else:
            print('Illegal number of events for bounding box.')

    def addRectangleFromLabel(self, label, k):
        self.circs[k].append(Rectangle(
            (np.min([label[0,0],label[1,0]]),
            np.min([label[0,1],label[1,1]])),
            height=np.max([label[0,1],label[1,1]])-
            np.min([label[0,1],label[1,1]]),
            width=np.max([label[0,0],label[1,0]])-
            np.min([label[0,0],label[1,0]]),
            color=self.col, alpha=self.label_alpha))
        self.axes.add_patch(self.circs[k][-1])

    def showLabelData(self):
        for k in range(len(self.labels)):
            label = self.labels[k]
            self.col = getEventColor(self, k)
            if np.sum(label) != 0:
                self.xs[k] = list(label[0])
                self.ys[k] = list(label[1])
                self.addCircle(label[0,0], label[0,1], k)
                self.addCircle(label[0,0], label[1,1], k)
                self.addCircle(label[1,0], label[0,1], k)
                self.addCircle(label[1,0], label[1,1], k)
                self.addRectangleFromLabel(label, k)
        self.col = getEventColor(self)

    def preprocessLabel(self, input_labels):
        labels = []
        for label in input_labels:
            buffer = np.array(label, dtype = np.uint16)
            labels.append(np.ndarray((2,2), buffer = buffer, dtype = np.uint16))
        while len(labels) < self.n_colours:
            label = np.ndarray((2, 2), dtype=np.uint16)
            label.fill(0)
            labels.append(label)
        return labels