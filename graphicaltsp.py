#!/usr/bin/python
        
#  Visualize TSP
#
from tkinter import *
from sys import exit
import tkinter.messagebox
import tspdata

from math import radians, sin, cos, tan

from gatspsub import Gatspsub

class mainWindow:

    def __init__(self,master,title):

        self.points = []
        self.window = master
        master.title(title)
        ctlframe=Frame(master)
        ctlframe.pack(side=LEFT)

        #  Menubar on top
        master.config(menu=self.makeMenus(master))

        #  Parameter frame: parameters for running the
        #  genetic algorithm (mostly a bunch of Entry text boxes)
        #
        mframe = Frame(ctlframe, bd=5, relief=GROOVE)
        mframe.grid(row=3, column=0, columnspan=2, pady=10)
       
        Label(mframe, text="Num Cities").grid(row=3, column=0, sticky=S+E)
        self.cinput=Entry(mframe, bg="white", width=4)
        self.cinput.insert(0, str(len(tspdata.cities)))
        self.cinput.grid(row=3, column=1)

        Label(mframe,text="Pop Size").grid(row=4, column=0, sticky=S+E)
        self.pinput=Entry(mframe, bg="white", width=4)
        self.pinput.insert(0, "50")
        self.pinput.grid(row=4, column=1)

        Label(mframe,text="Num Gens").grid(row=5, column=0, sticky=S+E)
        self.ginput=Entry(mframe, bg="white", width=4)
        self.ginput.insert(0, "100")
        self.ginput.grid(row=5, column=1)

        Label(mframe,text="Evolve Opts").grid(row=6, column=0, sticky=S+E)
        self.eoinput=Entry(mframe, bg="white", width=4)
        self.eoinput.insert(0, "")
        self.eoinput.grid(row=6, column=1)

        #  Ctrl Frame:  Reset and Go
        Label(ctlframe, bg="white", \
            text="Travelling Salesman\nGenetic Algorithm Visualizer").grid(\
                row=0, column=0, columnspan=2, pady=10)
        self.startButton=Button(ctlframe, text="Start", command=self.start)
        self.startButton.grid(row=1, column=0, pady=40, sticky=N+S)
        self.pauseButton=Button(ctlframe, text="Pause", command=self.pause, \
                    width=8)
        self.pauseButton.grid(row=1, column=1, pady=40, sticky=N+S)

        #  Status Frame inside Ctl Frame
        #        
        self.statframe = Frame(ctlframe)
        self.statframe.grid(row=4, column=0, columnspan=2, pady=10)
        Label(self.statframe, text="Generation").grid(row=0, column=0)
        Label(self.statframe, text="Shortest").grid(row=1, column=0)
        Label(self.statframe, text="Longest").grid(row=2, column=0)
        self.statg = Label(self.statframe, "", bg="white", width=9, 
            justify=RIGHT)
        self.statg.grid(row=0, column=1, sticky=W)
        self.stats = Label(self.statframe, "", bg="white", width=9, 
            justify=RIGHT)
        self.stats.grid(row=1, column=1, sticky=W)
        self.statl = Label(self.statframe, "", bg="white", width=9,
            justify=RIGHT)
        self.statl.grid(row=2, column=1, sticky=W)
        
        #  Drawing Canvas
        #
        self.canvasframe = Frame(master, bd=5, relief=GROOVE)
        self.canvasframe.pack(side=RIGHT)
        self.newcanvas()
        self.pathid = None

    def newcanvas(self):
        self.canvas = Canvas(self.canvasframe, bg="white", width=450, height=330)
        self.canvas.grid(row=0, column=0)
        self.xscale=400
        self.yscale=300

        # Mouse button action
        #self.canvas.bind("<Button-1>", self.mouseSelect)

    #  Menus (on the top menu bar)
    #
    def makeMenus(self,frame):
        returner=Menu(frame)
    
        #  Your usual 'file' menu a 'quit'  
        fileMenu=Menu(returner,tearoff=0)
        returner.add_cascade(label="File",menu=fileMenu)
        fileMenu.add_command(label="Quit",command=frame.quit)
    
        #  A 'help' menu contains only 'about'
        helpMenu=Menu(returner,tearoff=0)
        returner.add_cascade(label="Help",menu=helpMenu)
        helpMenu.add_command(label="About",command=self.about)

        return returner

    #  'Start' button handler: 
    #
    def start(self):
        self.popsize = cvt(self.pinput)
        self.ngens   = cvt(self.ginput)
        self.ncities = cvt(self.cinput)
        self.eopts   = self.eoinput.get()
        self.ga = Gatspsub(popsize=self.popsize, ngens=self.ngens, 
            ncities=self.ncities, evolveopts=self.eopts)
        self.ncities = self.ga.ncities
        self.cinput.delete(0,len(self.cinput.get()))
        self.cinput.insert(0,str(self.ncities))
        self.genno = 0
        # self.newcanvas()
        self.drawpath(self.ga.population[0])
        self.best_pathlen = 0
        self.worst_pathlen = 0
        self.recall = self.canvas.after(10, self.nextgen)
        self.statupdate("yellow")

    def statupdate(self, color):
        self.statg.configure(text=str(self.genno), bg=color)
        self.stats.configure(text=str(self.best_pathlen), bg=color)
        self.statl.configure(text=str(self.worst_pathlen), bg=color)

    def nextgen(self):
        if self.genno < self.ngens:
            self.genno, self.best_path, self.best_pathlen, \
                self.worst_pathlen = self.ga.run_ga(5)
            self.drawpath(self.best_path)
            self.statupdate("yellow")
            self.recall = self.canvas.after(10, self.nextgen)
        else:
            self.statupdate("white")

    #  'Clear' button handler: clears the points
    #
    def pause(self):
        self.canvas.after_cancel(self.recall)
        self.pauseButton.configure(text="Continue", command=self.contin)

    def contin(self):
        self.pauseButton.configure(text="Pause   ", command=self.pause)
        self.recall = self.canvas.after(10, self.nextgen)
 
    # Now draw a path
    def drawpath(self, path):
        if self.pathid:
            self.canvas.delete(self.pathid)
        else:
            self.draw_some_cities(path)

        if len(path) > 1:
            loclist = [tspdata.scaledloc(c) for c in path]
            vertexlist = []
            for yr, xr in loclist:
                vertexlist.append(scalept(xr,self.xscale))
                vertexlist.append(scalept(yr,self.yscale))
            yr, xr = loclist[0]
            vertexlist.append(scalept(xr,self.xscale))
            vertexlist.append(scalept(yr,self.yscale))
            
            self.pathid=self.canvas.create_line(*vertexlist)

    def draw_some_cities(self, path):

        xrmin = 1.0
        yrmin = 1.0
        xrmax = 0.0
        yrmax = 0.0
        for c in path:
            yr, xr = tspdata.scaledloc(c)
            xrmin = min(xrmin, xr)
            yrmin = min(yrmin, yr)
            xrmax = max(xrmax, xr)
            yrmax = max(yrmax, yr)
            x0, y0 = (scalept(xr, self.xscale)-1, scalept(yr, self.yscale)-1)
            self.canvas.create_oval(x0-1, y0-1, x0+1, y0+1, fill="green")

        for c in path:
            yr, xr = tspdata.scaledloc(c)
            x0, y0 = (scalept(xr, self.xscale)-1, scalept(yr, self.yscale)-1)
            if xr == xrmin:
                self.canvas.create_text(x0-10, y0+10, anchor=W, text=c[:-4])
            if xr == xrmax:
                self.canvas.create_text(x0-10, y0+10, anchor=W, text=c[:-4])
            if yr == yrmin:
                self.canvas.create_text(x0-20, y0+1, anchor=N, text=c[:-4])
            if yr == yrmax:
                self.canvas.create_text(x0-20, y0-1, anchor=S, text=c[:-4])

    def about(self):
        tkinter.messagebox.showinfo("About", "Genetic Travelling Salesman ")

# Convert string to integer
def cvt(textwid):
    try:
        val = int(textwid.get())
    except:
        val = 0
    return val

def scalept(x, scale):
    return int(round((1-x)*scale))+15

#  Main Program
#
if __name__=="__main__":

    w = Tk()
    tspdata.input()
    window = mainWindow(w, "Travelling Salesman")

    #  Wait for something to happen!
    window.window.mainloop()
