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
            self.tableau[p] = [None for i in range(9)]

            f.grid(row=self.positionspossibles[p][0], column=self.positionspossibles[p][1], sticky=self.nseo[p], ipadx=2, ipady=2)

        # Fran = Frame(self.root, background="white")
        # Fran.grid(column=3)
        # Label(Fran, text= "TIKTAKTOE")

        for h in self.root.winfo_children():
            self.creertictac(h)



    def creertictac(self, frame):
        for p in range(len(self.positionspossibles)):
            b = Button(self.frames[numpos], borderwidth = 1, background="white", foreground="black")
            b.grid(row=self.positionspossibles[p][0], column=self.positionspossibles[p][1], padx=0, pady=0, ipadx = 0, ipady = 0)
            b = Button(self.frames[numpos], borderwidth = 1, background="white", foreground="black")
            b.grid(row=self.positionspossibles[p][0], column=self.positionspossibles[p][1], padx=0, pady=0)

            height=round(int(self.geometry[0])/83)/2
            width=round(int(self.geometry[0])/83)

            b.config( height =int(height), width =int(width))



    def testgagne(self, dernbttouch):
        gagne = {(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2, 5, 8), (0,4,8), (2,4,6)}
        frm = self.root.winfo_parent(dernbttouch)
        frmij = self.root.grid_location(frm)
        t = self.postotab[(frmij[0], frmij[1])]
        for i in gagne:
            if self.tableau[t][i[0]] == self.tableau[t][i[1]] == self.tableau[t][i[2]]:
                self.gagnegrosframe(frm)


    def gagnegrosframe(self, frame):
        for obj in frame.winfo_children():
            obj.destroy()

    def placement(self, figure, pos):
        pass

    def creerxo(self, signe):
        pass




root = Tk()
g = Jeu(root, "450x450")
root.mainloop()