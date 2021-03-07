"""
This is the game of life v2.0

1 The system show a interface

1 = Alive
0 = death
"""
from tkinter import *
import math
import threading
import time
from Controller import *


class Software():
    def __init__(self):
        #Display vars
        self.controller = Controller()
        self.display = Tk()
        self.canvasUniverse =  Canvas(self.display, width=720, height=500) # Paint the universe
        self.canvasUniverse.bind('<Button-1>', self.evtRigthClick) # If you click r
        self.canvasUniverseControl = Canvas(self.display, width=720, height=200)
        self.canvasCassete = Canvas(self.display, width=200, height=120)
        self.imgCaseteBG1 = PhotoImage(file=self.controller.getCasseteBg1())
        self.imgCaseteBG2 = PhotoImage(file=self.controller.getCasseteBg2())
        self.imgCaseteBG3 = PhotoImage(file=self.controller.getCasseteBg3())
        self.lblGeneration = Label(self.canvasUniverseControl, text="generation: 0")
        self.lblLenUniverse = Label(self.canvasUniverseControl, text="of: 0")
        self.lblUniverseName = Label(self.canvasUniverseControl, text="name:")
        self.lblUniverseSize = Label(self.canvasUniverseControl, text="size: 0x0")
        self.txtUniverseName = Entry(self.canvasCassete, bg='gray')
        self.btnBlockWriter = Button(self.canvasUniverseControl, text="WR Block", bg="red", command=self.evtWrProtection)
        self.btnRec = Button(self.canvasUniverseControl, text="Rec", bg="blue", command=self.evtBtnRec)
        self.btnPlay = Button(self.canvasUniverseControl, text="Play", command=self.evtBtnPlay)
        self.btnNextGen  = Button(self.canvasUniverseControl, text="Next", command=self.evtNext)
        self.btnPrevGen = Button(self.canvasUniverseControl, text=" Prev")
        self.btnStop = Button(self.canvasUniverseControl, text="Stop", command=self.evtStop)
        self.btnEject = Button(self.canvasUniverseControl, text="Eject", command=self.evtEject)

        #Universe vars
        self.generation = 0 # number of generation 0, 1, 2 ... 
        self.wrProtection = True # say if i can write
        self.universeIsRepresentate = False # Say if universe is ready to paint
        self.gameIsRec = False # Sayme if the user save a universe
        self.gameIsPlay = False # Sayme if the game is running
        self.universe = [] # Contains a 0 death or 1 alive
        # Charge a default universe
        self.controller.loadUniverse("default")

        # Hilo
        self.hilo = threading.Thread(target=self.run)

        #Show and draw screem
        self.showDisplay()
        
        

    def showDisplay(self):
        self.display.title("Game of life by loko")
        self.display.geometry("720x700")

        self.canvasUniverse.place(x=0, y=0)
        self.canvasUniverseControl.place(x=0, y=500)
        self.canvasCassete.place(x=250, y=520)
            
        self.lblGeneration.place(x=20, y=20)
        self.lblLenUniverse.place(x=150, y=20)
        self.lblUniverseName.place(x=20, y=40)
        self.lblUniverseSize.place(x=20, y=60)
        self.txtUniverseName.place(x=38, y=16)
        self.btnBlockWriter.place(x=450, y=20)
        self.btnRec.place(x=220, y=160)
        self.btnPlay.place(x=280, y=160)
        self.btnPrevGen.place(x=340, y=160)
        self.btnNextGen.place(x=400, y=160)
        self.btnStop.place(x=460, y=160)
        self.btnEject.place(x=520, y=160)

        self.loadAndShowUniverse()

        self.display.mainloop()

    def showCassete(self):
        """
        Paint a cassete in canvas cassete
        """
        self.canvasCassete.create_image(0, 0, image=self.imgCaseteBG1, anchor=NW, tags="cassete")
        self.canvasCassete.create_image(0, 0, image=self.imgCaseteBG2, anchor=NW, tags="cassete")
        self.canvasCassete.create_image(0, 0, image=self.imgCaseteBG3, anchor=NW, tags="cassete")

    def hideCassete(self):
        self.canvasCassete.delete("cassete")


    def loadAndShowUniverse(self, universeName="default"):
        """
        charge a universe from tape.
        paint a rectangles and show 1 and 0
        """
        if len(self.universe) > 0:
            # Si ya se pinto un universo borrelo de la pantalla
            for i in range(0, len(self.universe)):
                for j in range(0, len(self.universe[0])):
                    self.canvasUniverse.delete(str(j)+":"+str(i))

        x, y = self.controller.getUniverseMatrixSize()
        self.universe = self.generateEmptyUniverse(y, x)
        self.universe = self.controller.getUniverseDataPos(0)
        self.paintRectanglesOfUniverse()
        self.paintUniverseSatusFromTape()
        


    def generateEmptyUniverse(self, y, x):
        """
        The universe[y][x] is create with 0...0
        """
        universe = []
        for i in range(0, y):
            universe.append([])
            for j in range(0, x):
                universe[i].append(0)

        return universe

    def paintRectanglesOfUniverse(self):
        """
        Calculate a size of universe and represent in canvas
        every cell taged with #:#
        """
        xmax = len(self.universe[0])
        ymax = len(self.universe)

        # To break line and paint rectangeles
        xcon = 0
        ycon = 0

        sizex = int(self.canvasUniverse['width'])/xmax 
       
        sizey = (int(self.canvasUniverse['height']))/ymax
        
        for i in range(0, ymax):
            xcon = 0
            for j in range(0, xmax):
                x0 = (sizex*xcon)
                y0 = (sizey*ycon)
                x1 = (sizex*(xcon+1))
                y1 = (sizey*(ycon+1))
                self.canvasUniverse.create_rectangle(x0, y0, x1, y1, tags=str(j)+":"+str(i), fill="green")
                xcon = xcon + 1
            ycon = ycon + 1
    

    def paintUniverseSatusFromTape(self):
        """
        The universe is contain in casete 
        i get the information and clone
        """
        data = []
        data = self.controller.getCasetePos(self.generation)


        if data != None:
            for i in range(0, len(data)):
                for j in range(0, len(data[0])):
                    cell = self.canvasUniverse.find_withtag(str(j)+":"+str(i))
                    if data[i][j] == 0:
                        self.universe[i][j] = 0
                        self.canvasUniverse.itemconfigure(cell, fill="green")
                    else:
                        self.universe[i][j] = 1
                        self.canvasUniverse.itemconfigure(cell, fill="black")

    def paintUniverseFromMatrix(self):
        """
        paint a universe self.universe
        """
    
        for i in range(0, len(self.universe)):
                for j in range(0, len(self.universe[0])):
                    cell = self.canvasUniverse.find_withtag(str(j)+":"+str(i))
                    if self.universe[i][j] == 0:
                        self.canvasUniverse.itemconfigure(cell, fill="black")
                    else:
                        self.universe[i][j] = 1
                        self.canvasUniverse.itemconfigure(cell, fill="white")


    def eraseUniverseSatus(self):
        for i in range(0, len(self.universe)):
            for j in range(0, len(self.universe[0])):
                cell = self.canvasUniverse.find_withtag(str(j)+":"+str(i))
                self.canvasUniverse.itemconfigure(cell, fill="white")
               
    def calculateNextGeneration(self):
        """
        Need information about x,y universe size
        run the matrix in toroid mode
        """
        leny = len(self.universe)
        lenx = len(self.universe[0])

        newUniverse = self.generateEmptyUniverse(leny, lenx)

 
        for i in range(0, len(self.universe)):
            for j in range(0, len(self.universe[0])):

                # Count of neigthbors
                countN = 0

                #N1
                countN = countN + self.universe[(i-1)%leny][(j-1)%lenx]

                #N2
                countN = countN + self.universe[(i-1)%leny][j]

                #N3
                countN = countN + self.universe[(i-1)%leny][(j+1)%lenx]

                #N4
                countN = countN + self.universe[i][(j-1)%lenx]

                #N5
                countN = countN + self.universe[i][(j+1)%lenx]

                #N6
                countN = countN + self.universe[(i+1)%leny][(j-1)%lenx]

                #N7
                countN = countN + self.universe[(i+1)%leny][j]

                #N8
                countN = countN + self.universe[(i+1)%leny][(j+1)%lenx]

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
        self.generation = self.generation + 1
    

    def evtRigthClick(self, Event):
        """
        If you click inside of universe the cell is alive
        """
        pass

            

    def evtWrProtection(self):
        self.wrProtection = not self.wrProtection

        if self.wrProtection:
            self.btnBlockWriter['bg'] = 'red'
        else:
            self.btnBlockWriter['bg'] = 'white'

    def evtBtnRec(self):
        """
        If the rec button is press activate a txt save generator
        """
        self.gameIsRec = not self.gameIsRec

        if self.gameIsRec:
            self.btnRec['bg'] = 'red'
        else:
            self.btnRec['bg'] = 'blue'

    def evtNext(self):
        print("siguiente")

    def evtEject(self):
        self.evtStop()
        self.controller.insertCasette = False
        self.generation = 0
        self.hideCassete()
    

    def evtBtnPlay(self):
        """
        If you start the game the bool activate a rules of life
        if you click for first time the thread is run
        paint if the casste is inside or ouside
        """
        self.gameIsPlay = not self.gameIsPlay

        

    
        if self.gameIsPlay:

            # If the tape is not insert and you insert a universe name:
            if not self.controller.insertCasette and self.validateTxtNameUniverse():
                self.controller.loadUniverse(self.txtUniverseName.get().strip())
                self.generation = 0
                self.loadAndShowUniverse()
                self.showCassete()

            try:
                self.hilo.start()
            except:
                pass

            self.btnPlay['text'] = 'pause'
            self.btnPlay['bg'] = 'green'
        else:
            self.btnPlay['text'] = 'play'
            self.btnPlay['bg'] = 'red'

    def evtStop(self):
        self.gameIsPlay = False
        self.btnPlay['bg'] = "red"


    def refrestStadics(self):
        self.refreshGenerationText()
        self.refreshUniverseName()
        self.refreshSizeOfAllGenerations()
        self.refreshUniverseSize()

    def refreshGenerationText(self):
        self.lblGeneration['text'] = "generation: " + str(self.generation) 

    def refreshUniverseName(self):
        self.lblUniverseName['text'] = "name: " + self.controller.getUniverseName()

    def refreshSizeOfAllGenerations(self):
        self.lblLenUniverse['text'] = "of: " + str(self.controller.getUniverseSize())

    def refreshUniverseSize(self):
        self.lblUniverseSize['text'] = "size: " + str(len(self.universe)) + "x" + str(len(self.universe[0]))

    def validateTxtNameUniverse(self):
        return str(self.txtUniverseName.get()).strip() != ""

    def alertSMS(self, title, txt):
        w = Toplevel()
        w.title(title)
        w.geometry("300x120")
        lblSms = Label(w, text=txt)
        lblSms.place(x=20, y=10)
        btnAcept = Button(w, text="Aceptar", command=w.destroy)
        btnAcept.place(x=240, y=80)


    def run(self):
        while True:
            if self.gameIsPlay:


                # If you insert a name casete and need save
                if self.controller.insertCasette and self.gameIsRec and not self.wrProtection:
                    self.controller.saveUniverse(self.txtUniverseName.get().strip(), self.universe, self.generation)
                    self.calculateNextGeneration()
                    self.paintUniverseFromMatrix() 
                    
                else:
                    # If you insert a tape read
                    if self.controller.insertCasette and not self.controller.defaultMode:
                        self.paintUniverseSatusFromTape()
                        if self.generation<self.controller.casete.duration:
                            self.generation = self.generation + 1
                        time.sleep(0)

                    # If you not insert a tape and you in default mode
                    if not self.controller.insertCasette and self.controller.defaultMode:
                        self.calculateNextGeneration()
                        self.paintUniverseFromMatrix()                      
            

            self.refrestStadics()


s = Software()