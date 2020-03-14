import sys

## TODO - Create markup file in GitHub

cwd = sys.path[0]
if len(cwd) == 0:
    cwd = 'C:/Users/berta/Desktop/Python/Image Labeller/'
    sys.path.append(cwd)

from Lib.Main_Window import *

app = MainWindow()
app.geometry("1000x600")
app.mainloop()