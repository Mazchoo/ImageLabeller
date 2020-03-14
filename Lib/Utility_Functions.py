import tkinter as tk
from tkinter import ttk

LARGE_FONT = ('Verdana',12)
NORM_FONT = ('Verdana',10)
SMALL_FONT = ('Verdana',8)

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title('!')
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side='top', fill ='x', pady=40)
    button1 = ttk.Button(popup, text='Okay', command=lambda: popup.destroy())
    button1.pack()
    popup.mainloop()

def enterValue(controller, attribute_string, callback):
    master = tk.Tk()
    master.wm_title('Enter ' + attribute_string)
    tk.Label(master, text='Enter ' + attribute_string + ' <=').grid(row=0)
    e = tk.Entry(master)
    e.grid(row=0, column=1)
    tk.Button(master, text='Cancel', command=lambda: controller.updatePlaceholder(master, None,
        callback)).grid(row=1, column=0, sticky='nsew', pady=4)
    tk.Button(master, text='Enter', command=lambda: controller.updatePlaceholder(master,e.get(
        ), callback)).grid(row=1, column=1, sticky='nsew', pady=4)
    tk.mainloop()

def convertToHexStr(x):
    return ('0' + hex(x).replace('0x', ''))[-2:]

def getEventColor(event_obj, k = None):
    if k is None: k = event_obj.c_index
    return event_obj.frame.colour_bar.colour_list[k]