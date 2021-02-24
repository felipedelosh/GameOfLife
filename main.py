"""
The game of life by felipedelosh

1 = Alive
0 = death
"""

from tkinter import *
import threading
import math

class Software():
    def __init__(self):
        #Display vars
        self.display = Tk()
        self.canvas =  Canvas(self.display, width=720, height=500)
        self.canvas.bind('<Button-1>', self.evtRigthClick) # If you click r
        self.btnPlay = Button(self.canvas, text="Play", command=self.evtBtnPlay)
        self.btnNextGen  = Button(self.canvas, text="Next GEN", command=self.nextGeneration)

        #Universe vars
        self.gameIsPlay = False # Sayme if the game is running
        self.universe = self.generateDeathUniverse() # Contains a 0 death or 1 alive

        self.thread = threading.Thread(target=self.runGameOfLife)
        self.thread.start()
        #Show and draw screem
        self.showDisplay()

    def showDisplay(self):
        self.display.title("Game of life by loko")
        self.display.geometry("720x500")

        self.canvas.place(x=0, y=0)
        self.btnPlay.place(x=330, y=460)
        self.btnNextGen.place(x=400, y=460)
        self._paintRectanglesOfUniverse()
        self.display.mainloop()

    def _paintRectanglesOfUniverse(self):
        """
        Calculate a size of universe and represent in canvas
        every cell taged with #:#
        """
        xmax = len(self.universe)
        ymax = len(self.universe[0])

        # To break line and paint rectangeles
        xcon = 0
        ycon = 0

        sizex = int(self.canvas['width'])/xmax 
       
        # Need a 10% of the screem to put control buttons
        sizey = (int(self.canvas['height'])*0.9)/ymax
        
        for i in self.universe:
            xcon = 0
            for j in i:
                x0 = (sizex*xcon)
                y0 = (sizey*ycon)
                x1 = (sizex*(xcon+1))
                y1 = (sizey*(ycon+1))
                self.canvas.create_rectangle(x0, y0, x1, y1, tags=str(xcon)+":"+str(ycon))
                xcon = xcon + 1
            ycon = ycon + 1

    def generateDeathUniverse(self):
        """
        The universe is generate in [[0,0,0,0], [,0,0,0,0] ....]
        """
        universe = []

        for i in range(0, 22):
            universe.append([])
            for j in range(0, 22):
                universe[i].append(0)

        return universe

    def paintUniverseSatus(self):
        for i in range(0, len(self.universe)):
            for j in range(0, len(self.universe[i])):
                cell = self.canvas.find_withtag(str(i)+":"+str(j))
                if self.universe[i][j] == 0:
                    self.canvas.itemconfigure(cell, fill="white")
                else:
                    self.canvas.itemconfigure(cell, fill="black")

    def evtBtnPlay(self):
        """
        If you start the game the bool activate a rules of life
        """
        self.gameIsPlay = not self.gameIsPlay

        if self.gameIsPlay:
            self.btnPlay['bg'] = 'green'
        else:
            self.btnPlay['bg'] = 'red'

        self.paintUniverseSatus()

    def evtRigthClick(self, Event):
        """
        If you click inside of universe the cell is alive
        """
        if int(self.canvas['height'])*0.9 >= Event.y:
            sizex = int(self.canvas['width'])/len(self.universe)
            sizey = (int(self.canvas['height'])*0.9)/len(self.universe[0])
            xID = math.floor(Event.x/sizex)
            yID = math.floor(Event.y/sizey)
            # Alive in universe
            self.universe[xID][yID] = 1

            self.paintUniverseSatus()

    def runGameOfLife(self):
        """
        This is the main thread of the game
        """
        con = 0
        while True:
            self.paintUniverseSatus()
            if self.gameIsPlay:
                self.nextGeneration()

    def nextGeneration(self):
        newUniverse = self.generateDeathUniverse()
        for i in range(0, len(self.universe)):
            for j in range(0, len(self.universe[0])):

                # Count of neigthbors
                countN = 0

                #N1
                try:
                    if self.universe[i-1][j-1] == 1:
                        countN = countN + 1
                except:
                    pass
                #N2
                try:
                    if self.universe[i-1][j] == 1:
                        countN = countN + 1
                except:
                    pass
                #N3
                try:
                    if self.universe[i-1][j+1] == 1:
                        countN = countN + 1
                except:
                    pass
                #N4
                try:
                    if self.universe[i][j-1] == 1:
                        countN = countN + 1
                except:
                    pass
                #N5
                try:
                    if self.universe[i][j+1] == 1:
                        countN = countN + 1
                except:
                    pass
                #N6
                try:
                    if self.universe[i+1][j-1] == 1:
                        countN = countN + 1
                except:
                    pass
                #N7
                try:
                    if self.universe[i+1][j] == 1:
                        countN = countN + 1
                except:
                    pass
                #N8
                try:
                    if self.universe[i+1][j+1] == 1:
                        countN = countN + 1
                except:
                    pass

                # Rule
                if self.universe[i][j] == 1:
                    if countN == 2 or countN == 3:
                        newUniverse[i][j] = 1
                    else:
                        newUniverse[i][j] = 0
                else:
                    if countN == 3:
                        newUniverse[i][j] = 1
                    else:
                        newUniverse[i][j] = 0

        self.universe = newUniverse



s = Software()