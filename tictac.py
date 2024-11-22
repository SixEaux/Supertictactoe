from tkinter import *
class Jeu:
    def __init__(self, root, geometria):

        self.root = root
        self.root.resizable(0, 0)
        self.root.title("SuperTicTacToe")
        self.root.geometry(geometria)
        self.frames = {} # tous les ojets graphiques de frames avec en cle la position dans le tableau (1,1) , (1,2) ...
        self.tableau = {} # code du tableau c'est 11,12,13,14...
        self.obj = {i : [] for i in range(9)}
        self.croix = [] #positions avec croix
        self.rond = [] #positions ou il y a un rond
        self.positionspossibles = [(i,j) for i in range(3) for j in range(3) if i+j<=4]
        self.nseo = ["NW", "N", "NE", "W", None, "E", "SW", "S", "SE"]
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.initialisationgraph()




    def initialisationgraph(self): #creer frames pour chaque garnd carré puis grid et ajouter tous les tiktaktoes
        for p in range(len(self.positionspossibles)):
            f = Frame(self.root, background="white")
            self.tableau[p] = {}
            self.frames[p] = f
            f.grid(row=self.positionspossibles[p][0], column=self.positionspossibles[p][1], sticky=self.nseo[p], padx=0, pady=0)

        for h in range(9):
            self.creertictac(h)

    def creertictac(self, numpos):
        for p in range(len(self.positionspossibles)):
            b = Button(self.frames[numpos], borderwidth = 0, background="white", foreground="black")
            b.grid(row=self.positionspossibles[p][0], column=self.positionspossibles[p][1], padx=0, pady=0)
            self.obj[numpos].append((p, b))


    def ptitictac(self):
        pass

    def placement(self, figure, pos):
        pass

    def creerxo(self, signe):
        pass


root = Tk()
g = Jeu(root, "450x450")
root.mainloop()