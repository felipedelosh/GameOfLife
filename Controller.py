"""
FelipedelosH

this is a controller of game of life
"""

import os # To get a path project
import random

from Casette import *

class Controller():
    def __init__(self):
        self.projectPath = str(os.path.dirname(os.path.abspath(__file__)))
        self.casete = Casette() # Save all universes
        self.defaultMode = True # if you not charge a universe show a default universe
        self.insertCasette = False # If you charge a cassete ... if universe inside in cassete
        
        self.createAUniverseFolder()
        self.createDedaultUniverse()

    def createAUniverseFolder(self):
        """
        If the game is start need to create a folder universes in root
        this folder save a universe and loads. need create first.
        """
        if not os.path.isdir(self.projectPath+"\\universe"): # if not exist create
            os.mkdir(self.projectPath+"\\universe")

    def createDedaultUniverse(self):
        """
        When the game is run need to create a universe/default.txt
        """
        route = self.projectPath+"\\universe"+"\\"+"default.txt"
        f = open(route, "w", encoding="UTF-8")
        h = random.randint(20, 50)
        w = random.randint(20, 50)
        print("Generando universo de tamano y:", h, " x: ", w)
        txt = ""
        for i in range(0, h):
            for j in range(0, w):
                txt = txt + str(random.randint(0, 1))
            txt = txt + "\n"
        f.write(txt)
        f.close()
       

    def getCasseteBg1(self):
        bg1 = random.randint(0, 20)
        route = self.projectPath + "\\resources\\img\\tapes\\tapb1" + "\\" + str(bg1) + ".png"
        return route

    def getCasseteBg2(self):
        bg1 = random.randint(0, 5)
        route = self.projectPath + "\\resources\\img\\tapes\\tapb2" + "\\" + str(bg1) + ".png"
        return route

    def getCasseteBg3(self):
        bg1 = random.randint(0, 1)
        route = self.projectPath + "\\resources\\img\\tapes\\tapb3" + "\\" + str(bg1) + ".png"
        return route

    def saveUniverse(self, universeName, universe, generation):
        try:
            route = self.projectPath+"\\universe\\" + universeName

            if not os.path.isdir(route):
                os.mkdir(route)

            txt = ""

            for i in universe:
                for j in i:
                    txt = txt + str(j)
                txt = txt + "\n"

            f = open(route + "\\" + str(generation) + ".txt", "w", encoding="UTF-8")
            f.write(txt)
            f.close()

            return True
        except:
            return False

    def getUniverseMatrixSize(self):
        """
        return a x, y of universe size in tape pos 0
        """
        return len(self.casete.tape.data[0]), len(self.casete.tape.data)
     

    def getUniverseSize(self):
        """
        Return a size of all universes in cassete
        """
        return self.casete.duration

    def getUniverseName(self):
        return self.casete.name

    def loadUniverse(self, universeName):
        """
        universe/universeName/0.txt ... n.txt load in data cassete
        """

        self.casete.deteleAll()

        if universeName != "default":
            print("No es default")
            self.casete.deteleAll()
            """
            Se procede a leer los txt uno por uno
            """
            readNext = True
            idUniverse = 0

            while readNext:
                try:
                    ruta = self.projectPath+"\\universe" + "\\" + universeName + "\\" +  str(idUniverse)+".txt"

                    f = open(ruta, "r", encoding="UTF-8")
                    txt = f.read()
                    universe = []
                    cony = 0

                    for i in txt.split("\n"):
                        if str(i).strip() != "":
                            universe.append([])
                            for j in i:
                                universe[cony].append(int(j))
                            cony = cony + 1
                            
                    f.close()
                    # Add to casete
                    self.casete.addData(universe)
                   
                    readNext = True
                    idUniverse = idUniverse + 1
                except:
                    readNext = False

            self.casete.name = universeName
            self.defaultMode = False
            self.insertCasette = True


        else:    
            f = open(self.projectPath+"\\universe\\default.txt", "r", encoding="UTF-8")
            txt = f.read()

            universe = []
            cony = 0
            for i in txt.split("\n"):
                if str(i).strip() != "":
                    universe.append([])
                    for j in i:
                        universe[cony].append(int(j))
                    cony = cony + 1
            
            f.close()
            self.defaultMode = True
            self.insertCasette = False
            # Add to casete
            self.casete.addData(universe)
            self.casete.name = "default"
    
    def getUniverseDataPos(self, position):
        return self.casete.getData(position)
        
    def resetUniverse(self):
        self.casete.deteleAll()

    def getCasetePos(self, x):
        return self.casete.getData(x)