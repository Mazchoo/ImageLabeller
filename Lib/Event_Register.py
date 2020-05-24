import numpy as np
import keyboard, sys
from matplotlib.patches import Circle

class EventTracker:

    def __init__(self, axes, col, rad, alp, image, frame):
        self.frame = frame
        c_bar = self.frame.colour_bar
        self.c_index = c_bar.current_index
        self.n_colours = c_bar.max_index
        self.cursor_visible_setting = True
        self.col = col
        self.label_alpha = alp
        self.radius = rad
        self.axes = axes
        self.setupDrawingData(image)
        self.event_interface = None
        self.addAllLines()

    def loadAllLabels(self):
        self.labels = []
        for i in range(self.n_colours):
            self.addNewLabel()

    def addAllLines(self):
        n_colours = self.n_colours
        while n_colours > 0:
            self.addNewLine()
            n_colours -= 1

    def setupDrawingData(self, image):
        self.xs = [[]]
        self.ys = [[]]
        self.circs = [[]]
        self.lines = []
        self.im_h, self.im_w = len(image), len(image[0])

    def checkHotkeys(self):
        return False

    def checkCallIsValid(self, event):
        if event.inaxes != self.lines[self.c_index].axes: return True
        if event.xdata > self.im_w: return True
        if event.ydata > self.im_h: return True
        if keyboard.is_pressed('shift'): return True
        return False

    def checkLeftMouseClick(self, event):
        if event.button == 1:
            self.xs[self.c_index].append(event.xdata)
            self.ys[self.c_index].append(event.ydata)
            self.cursorEvent(event)
            self.draw()
            return True
        return False

    def updateLineData(self, label_index = None):
        if (label_index is None): label_index = self.c_index
        self.lines[label_index].set_data(self.xs[label_index], self.ys[label_index])

    def cursorEvent(self, event):
        self.updateLineData()
        self.addCircle(event.xdata, event.ydata)

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
        self.updateLineData()
        circ = self.circs[self.c_index].pop(-1)
        circ.remove()

    def __call__(self, event):
        if self.checkHotkeys(): return True
        if self.checkCallIsValid(event): return False
        if self.checkLeftMouseClick(event): return True
        if self.checkRightClickEvent(event): return True

    def setLineColor(self, col):
        self.lines[self.c_index].set_color(col)
        self.draw()

    def setLineWidth(self, weight):
        self.lines[self.c_index].set_linewidth(weight)
        self.draw()

    def setCursorColour(self, col):
        self.col = col
        for c in self.circs[self.c_index]:
            c.set_color(col)
        self.lines[self.c_index].set_color(col)
        self.draw()

    def setCursorAlpha(self,alp):
        self.label_alpha = alp
        for c in self.circs[self.c_index]:
            c.set_alpha(alp)
        self.draw()

    def setCursorWeight(self, rad):
        self.radius = rad
        for c in self.circs[self.c_index]:
            try:
                c.set_radius(self.radius)
            except:
                pass
        self.draw()

    def addCircle(self, x, y, label_index = None):
        if label_index is None : label_index = self.c_index
        self.circs[label_index].append(Circle((x, y),
            radius=self.radius, color=self.col,
            alpha=self.label_alpha)
        )
        self.axes.add_patch(self.circs[label_index][-1])

    def removeAllCircles(self):
        if len(self.circs[self.c_index]) != 0:
            for i in range(len(self.circs[self.c_index])):
                circ = self.circs[self.c_index].pop(-1)
                circ.remove()
            self.draw()

    def drawBackCircle(self, ind):
        self.circs[self.c_index].append(matplotlib.patches.Circle(
            (self.xs[ind], self.ys[ind]), radius=self.radius, color=self.col))

    def drawBackAllCircles(self):
        if len(self.circs[self.c_index]) == 0:
            for i in range(len(self.xs[self.c_index])):
                self.drawBackCircle(ind)
                self.axes.add_patch(self.circs[self.c_index][-1])
            self.draw()

    def setTogglePatches(self, toggle):
        self.cursor_visible_setting = toggle
        if toggle:
            self.drawBackAllCircles()
        else:
            self.removeAllCircles()

    def draw(self):
        self.lines[self.c_index].figure.canvas.draw()

    def showLabelData(self):
        pass

    def preprocessLabel(self, label):
        return label

    def updateColourIndex(self, new_index):
        self.c_index = new_index

    def loadLabel(self, label):
        self.labels = self.preprocessLabel(label)
        self.showLabelData()
        self.draw()

    def addNewLabel(self):
        pass

    def addNewLine(self):
        line = self.frame.addNewLine()
        if not(self.event_interface):
            self.fig = line.figure
            self.event_interface = line.figure.canvas.mpl_connect('button_press_event', self)
        self.lines.append(line)
        self.xs.append([])
        self.ys.append([])
        self.circs.append([])

    def checkHotkeys(self):
        if keyboard.is_pressed('q'):
            self.frame.makeBackup(); return
        if keyboard.is_pressed('w'):
            self.frame.nextImage(-1); return
        if keyboard.is_pressed('s'):
            self.frame.nextImage(1); return
        if keyboard.is_pressed('a'):
            self.frame.selectConsectiveLabel(-1); return
        if keyboard.is_pressed('d'):
            self.frame.selectConsectiveLabel(1); return
        return False

    def clear(self):
        self.fig.canvas.mpl_disconnect(self.event_interface)