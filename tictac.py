from tkinter import *


class Jeu:
    def __init__(self, root, geometria):
        self.root = root
        self.root.resizable(0, 0)
        self.root.title("SuperTicTacToe")
        self.root.geometry(geometria)
        self.geometry = tuple(map(int, geometria.split("x")))

        self.tableau = {} # code du tableau c'est 11,12,13,14...

        self.positionspossibles = [(i,j) for i in range(3) for j in range(3) if i+j<=4]
        self.nseo = ["NW", "N", "NE", "W", None, "E", "SW", "S", "SE"]
        self.postotab = {(0,0):0, (0,1):1, (0,2):2, (1,0):3, (1,1):4, (1,2): 5, (2,0):6, (2,1):7, (2,2):8}

        for i in range(3):
            self.root.columnconfigure(i, weight=1)
            self.root.rowconfigure(i, weight=1)
        self.root.columnconfigure(3, weight=3)
        self.root.rowconfigure(3, weight=1)

        print(dir(self.root))

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
            b = Button(frame, borderwidth = 1, background="white", foreground="black")
            b.grid(row=self.positionspossibles[p][0], column=self.positionspossibles[p][1], padx=1, pady=1)

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
g = Jeu(root, "600x600")
root.mainloop()