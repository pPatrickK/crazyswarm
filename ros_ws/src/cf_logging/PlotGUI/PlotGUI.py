# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 10:42:31 2019

@author: diewa
"""

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import os
import sys
import CF_functions as cff

LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = []
a.append(f.add_subplot(111))

opts = [ "" ]

NUM_ROWS = 1
NUM_COLS = 1

cf_data = {}
filename = ""
app = None

# read csv values and plot them:
#def animate(i):
#    if(app.filename != ""):
#        pullData = open(app.filename,"r").read()
#        dataList = pullData.split('\n')
#        xList = []
#        yList = []
#        for eachLine in dataList:
#            if len(eachLine) > 1:
#                x, y = eachLine.split(',')
#                xList.append(int(x))
#                yList.append(int(y))
#
#        a.clear()
#        a.plot(xList, yList)
#        a.set_aspect('equal', 'box')


def new_plot():
    global a
    f.clf()
    a = []
    count = 1
    for i in range(1,NUM_ROWS+1):
        for j in range(1,NUM_COLS+1):
            a.append(f.add_subplot(NUM_ROWS, NUM_COLS, count))
            count = count + 1
    app.canvas.show()

def onclick(event):
    global a
    if event.dblclick:
        axNum = a.index(event.inaxes)
        promptData = DataPage(axNum)
        promptData.mainloop()

class AutocompleteEntry(tk.Entry):
    def __init__(self, lista, *args, **kwargs):
        tk.Entry.__init__(self, *args, **kwargs)

        self.lista = lista
        #print("lista in autocom " + str(lista))
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = tk.StringVar()
        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.lb_up = False


    def changed(self, name, index, mode):
        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            print(words)
            if words:
                if not self.lb_up:
                    self.lb = tk.Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):
        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        pattern = re.compile(self.var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]


class PlottingGUI(tk.Tk):

    filename = ""
    canvas = None

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

#        tk.Tk.iconbitmap(self, default="icon.ico")
        tk.Tk.wm_title(self, "CF Data Plotting GUI")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open File", command = self.open_file, accelerator="Ctrl+O")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.destroy, accelerator="Ctrl+W")
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Grid", command = self.selectRowsCols, accelerator="Ctrl+G")
        editmenu.add_command(label="Info", command = self.infoBox, accelerator="Ctrl+I")
        menubar.add_cascade(label="Edit", menu=editmenu)

        self.bind_all("<Control-w>", self.quit)
        self.bind_all("<Control-o>", self.open_file)
        self.bind_all("<Control-g>", self.selectRowsCols)
        self.bind_all("<Control-i>", self.infoBox)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

#        for F in (StartPage, PageOne, PageTwo, PageThree):
#
#            frame = F(container, self)
#
#            self.frames[F] = frame
#
#            frame.grid(row=0, column=0, sticky="nsew")
#
        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def open_file(self, event=None):
        global cf_data

        self.filename =  tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*"),("txt files","*.txt")))

        if len(self.filename) > 0:
            cf_data = cff.decode(self.filename)
            global filename
            filename = self.filename

    def selectRowsCols(self, event=None):
        promptSel = RowColPage()
        promptSel.mainloop()

    def infoBox(self, event=None):
        infoBox = InfoPage()
        infoBox.mainloop()

    def quit(self, event):
        self.destroy()
        sys.exit()


class RowColPage(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Number of Rows and Columns")


        slideBox =  tk.Frame(self)
        rowBox =  tk.Frame(slideBox)
        rowBox.configure(height=100)
        rowBox.grid_propagate(0)
        label = tk.Label(rowBox, text="Rows")
        label.pack(side=tk.BOTTOM, expand=False)
        self.rows = tk.Scale(rowBox, from_=1, to=3, orient=tk.HORIZONTAL)
        self.rows.pack(side=tk.TOP, expand=False)
        rowBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        colBox =  tk.Frame(slideBox)
        colBox.configure(height=100)
        colBox.grid_propagate(0)
        label = tk.Label(colBox, text="Columns")
        label.pack(side=tk.BOTTOM, expand=False)
        self.cols = tk.Scale(colBox, from_=1, to=3, orient=tk.HORIZONTAL)
        self.cols.pack(side=tk.TOP, expand=False)
        colBox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        slideBox.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        butBox =  tk.Frame(self)
        butBox.configure(height=50)
        butBox.grid_propagate(0)
        button1 = tk.Button(self, text = "OK", command = self.okay)
        button1.pack(side=tk.LEFT, expand=True, padx=25)
        button2 = tk.Button(self, text = "Cancel", command = self.quit)
        button2.pack(side=tk.RIGHT, expand=True, padx=25)
        butBox.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)

        # self.grid(row=0, column=0, sticky="nsew")

        self.tkraise()

    def okay(self, event=None):
        global NUM_ROWS
        global NUM_COLS
        NUM_ROWS = self.rows.get()
        NUM_COLS = self.cols.get()
        new_plot()
        self.destroy()

    def quit(self, event=None):
        self.destroy()


class InfoPage(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Current Log-File:")

        global filename

        infoBox =  tk.Frame(self)
        infoBox.configure(height=50)
        # infoBox.configure(width=200)
        label = tk.Label(self, text=filename)
        label.pack(side=tk.LEFT, expand=True)
        infoBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        butBox =  tk.Frame(self)
        butBox.configure(height=50)
        butBox.grid_propagate(0)
        button = tk.Button(self, text = "Close", command = self.quit)
        button.pack(side=tk.LEFT, expand=True, padx=25)
        butBox.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)

        # self.grid(row=0, column=0, sticky="nsew")

        self.tkraise()

    def quit(self, event=None):
        self.destroy()


class DataPage(tk.Tk):

    def __init__(self, i, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Data")

        self.i = i

        selBox =  tk.Frame(self)

        global opts
        global cf_data
        opts = []
        for cfg in cf_data.keys():
            opts.append(cfg)

        boxX = tk.Frame(selBox)
        boxX.configure(height=100)
        boxX.grid_propagate(0)
        label = tk.Label(boxX, text="X Data:")
        label.pack(side=tk.LEFT, expand=False)
        self.xOpt = ttk.Combobox(boxX, values = opts)
        self.xOpt.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        boxX.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        boxY = tk.Frame(selBox)
        boxY.configure(height=100)
        boxY.grid_propagate(0)
        label = tk.Label(boxY, text="Y Data:")
        label.pack(side=tk.LEFT, expand=False)
        self.yOpt = ttk.Combobox(boxY, values = opts)
        self.yOpt.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        boxY.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        selBox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        butBox =  tk.Frame(self)
        butBox.configure(height=50)
        butBox.grid_propagate(0)
        button1 = tk.Button(self, text = "OK", command = self.okay)
        button1.pack(side=tk.LEFT, expand=True, padx=25)
        button2 = tk.Button(self, text = "Cancel", command = self.quit)
        button2.pack(side=tk.RIGHT, expand=True, padx=25)
        butBox.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)

        # self.grid(row=0, column=0, sticky="nsew")

        self.tkraise()

    def okay(self, event=None):
        global a
        global cf_data
        xKey = self.xOpt.get()
        yKey = self.yOpt.get()
        if xKey in cf_data.keys() and yKey  in cf_data.keys():
            a[self.i].clear()
            a[self.i].plot(cf_data[xKey], cf_data[yKey])
            a[self.i].autoscale()
            app.canvas.show()
        self.destroy()

    def quit(self, event=None):
        self.destroy()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        controller.canvas = FigureCanvasTkAgg(f, self)
        controller.canvas.show()
        cid = controller.canvas.mpl_connect('button_press_event', onclick)
        controller.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(controller.canvas, self)
        toolbar.update()
        controller.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

app = PlottingGUI()
#ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
