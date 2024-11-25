from tkinter import *
from itertools import cycle
from tabulate import tabulate


class Jeutab:
    def __init__(self):
        self.joueurs = (("X", "red"), ("O", "blue"))
        self.ordre = cycle(self.joueurs) #ordre des joueurs
        self.quijoue = next(self.ordre) #a qui le tour
        self.queltictac = None #ou est-ce que il faut jouer/ si None alors tu peuc jouer nimporte ou

        self.tableau = {i : ["" for j in range(9)] for i in range(9)} #tableau avec le chiffre de chaque tictactoe et une liste avec le label de chaque case
        self.grostictac = ["" for i in range(9)] #chiffre du tictactoe avec "" si pas gagné puis mettre label si gagné
        self.gagne = {(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2, 5, 8), (0,4,8), (2,4,6)} #positions à verifier si gagné

        self.fin = False #estce que il y a déjà un gagnant?
        self.gagnant = ""

    def printTableau(self):
        print(tabulate(self.tableau.values(), tablefmt="heavy_outline"))

    def changejoueur(self): #passer au joueur suivant
        self.quijoue = next(self.ordre)

    def changetictac(self, mouvement):
        if self.grostictac[mouvement[1]] == "":
            self.queltictac = mouvement[1]
        elif self.grostictac[mouvement[1]] != "":
            self.queltictac = None


    def mouvpossible(self, mouvement): #regarder su mouvement est possible et regarder si le mouvement est sur le bon tiktak / mouvement serait surement des coordonnées (grosframe,petitframe)
        if (self.fin == False and (self.queltictac is None or self.queltictac == mouvement[0])
                and self.grostictac[mouvement[0]] == "" and self.tableau[mouvement[0]][mouvement[1]] == ""):
            return True
        else:
            print("Imp")
            return False

    def fairemouvement(self, mouvement): #faire mouvement dans tableau si possible
        if  self.mouvpossible(mouvement):
            self.tableau[mouvement[0]][mouvement[1]] = self.quijoue[0]
            if self.gagnepetit(mouvement[0]):
                self.grostictac[mouvement[0]] = self.quijoue[0]
                self.gagnegros()
            elif self.estceegalite(self.tableau[mouvement[0]]):
                self.grostictac[mouvement[0]] = "Imp"
                if self.estceegalite(self.grostictac):
                    self.egalite()

            self.quijoue = next(self.ordre)
            self.changetictac(mouvement)
            self.printTableau()

    def gagnepetit(self, tictac): #regarder si dans le tableau il y a des gagnants, tictac c'est quel tableau des petits
        for i in self.gagne:
            if self.tableau[tictac][i[0]] == self.tableau[tictac][i[1]] == self.tableau[tictac][i[2]] != "":
                self.grostictac[tictac] = self.tableau[tictac][i[0]]
                return True

    def gagnegros(self): #regarder si dans le tableau il y a un gros gagnant
        for i in self.gagne:
            if self.grostictac[i[0]] == self.grostictac[i[1]] == self.grostictac[i[2]] != "":
                self.gagnetot(self.grostictac[i[0]])
        if self.estceegalite(self.grostictac) and self.fin == False: self.egalite()


    def gagnetot(self, signe): #le gros tictactoe est gagné et il faut donner qui a gagné
        self.fin = True
        self.gagnant = signe

    def estceegalite(self, tictac): #regarder si il y a egalite / tictac c'est directement le tableau
        cpt = 0
        for i in tictac:
            if i == "": cpt += 1
        if cpt == 0:
            return True
        else:
            return False

    def egalite(self): #fin si egalite
        self.fin = True
        self.gagnant = "Aucun des deux"

    def rejouer(self): # remettre tout à zero pour rejouer
        self.fin = False
        self.gagnant = ""
        self.tableau = {i: ["" for j in range(9)] for i in range(9)}
        self.grostictac = ["" for i in range(9)]


class Menujeu(Tk):
    def __init__(self, geometria):
        super().__init__()
        self.title("SuperTicTacToe")
        self.geometria = geometria
        self.menu()

    def menu(self):
        menu = Frame(self)
        menu.pack()
        Label(menu, text="SuperTicTacToe").pack()
        Button(menu, text='Jouer', command=lambda: self.alleraujeu('jeu')).pack()
        Button(menu, text='Quitter', command=self.quit).pack()

    def alleraujeu(self, enquoi):
        self.destroy()
        Jeu(self.geometria)




class Jeu(Tk, Jeutab):
    def __init__(self, geometria):
        Tk.__init__(self)
        self.jeutab = Jeutab()

        self.title("Multijoueur")
        self.geometria = tuple(map(int, geometria.split("x"))) #dimensions fenetre

        self.positionspossibles = [(i,j) for i in range(3) for j in range(3) if i+j<=4] #pour affichage frames
        self.nseo = ["NW", "N", "NE", "W", None, "E", "SW", "S", "SE"] #pour stick frames

        self.txt = StringVar()
        self.label = None

        self.height = round(int(self.geometria[0]) / 83) / 2
        self.width = round(int(self.geometria[0]) / 83)

        print(dir(self))

        self.postofrm = []
        self.butons = {}

        self.initialisationgraph()

    def initialisationgraph(self): #creer frames pour chaque garnd carré puis grid et ajouter tous les tiktaktoes

        for i in range(3):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i, weight=1)

        for p in range(len(self.positionspossibles)): #creer les frames qui vont contenir tictactoes
            f = Frame(self, background="white", highlightbackground="grey", highlightthickness=2)
            f.grid(row=self.positionspossibles[p][0], column=self.positionspossibles[p][1], sticky=self.nseo[p], padx=3, pady=3)
            self.postofrm.append(f)
        print(self.postofrm)

        barre = Menu(self)
        options = Menu(barre, tearoff=0, activebackground="grey", activeforeground= "red")
        barre.add_cascade(label="| Options |", menu=options)
        options.add_command(label="Revenir au Menu", command=lambda: self.revenirmenu())
        options.add_separator()
        options.add_command(label="Rejouer", command=lambda: self.rejouer())
        self.config(menu=barre)

        for h in self.postofrm:
            self.creertictac(h)

        self.rowconfigure(3, weight=3)

        f = Frame(self, background="white", highlightbackground="grey", highlightthickness=2)
        f.grid(row=3, column=1)
        self.txt.set(f"Tour de: {self.jeutab.quijoue[0]}")
        self.label = Label(f, text= "Tour de: ", textvariable=self.txt, font=40)
        self.label.pack(side=BOTTOM)

    def creertictac(self, frame): #créer petits tiktaktoes
        for p in range(len(self.positionspossibles)):
            b = Button(frame, borderwidth = 1, background="white", foreground="black")
            b.config(command = lambda a=b: self.creerxo(a))
            b.grid(row=self.positionspossibles[p][0], column=self.positionspossibles[p][1], padx=2, pady=2, sticky="nsew")
            b.config(height =int(self.height), width =int(self.width))
            self.butons[b] = (self.postofrm.index(frame), p)

    def creerxo(self, bouton): #creer croix ou ronds
        pos = self.butons[bouton]
        if self.jeutab.mouvpossible(pos):
            self.jeutab.tableau[pos[0]][pos[1]] = self.jeutab.quijoue[0]
            bouton.config(text = self.jeutab.quijoue[0], fg = self.jeutab.quijoue[1])
            print(self.nametowidget(bouton.winfo_parent()))
            self.tourdejeu(self.nametowidget(bouton.winfo_parent()), pos)
        else:
            self.txt.set("Réessaye")

    def tourdejeu(self, frame, mouv):
        posfrm = self.postofrm.index(frame)
        tabfrm = self.jeutab.tableau[posfrm]

        if self.jeutab.estceegalite(tabfrm):
            self.grostictac[posfrm] = "Imp"
            if self.jeutab.estceegalite(self.postofrm):
                self.fin("Egalite")

        elif self.jeutab.gagnepetit(posfrm):
            self.grostictac[posfrm] = self.jeutab.quijoue[0]
            if self.jeutab.gagnegros():
                self.fin(f"{self.jeutab.quijoue[0]} a gagné!")

        self.jeutab.changejoueur()
        self.jeutab.changetictac(mouv)

    def fin(self, queltype):
        self.txt.set(queltype)
        self.jeutab.gagnetot("Aucun")

    def rejouer(self): #tout remettre en place pour jouer
        pass
        # remettre à zero tous les elements de tableau

    def revenirmenu(self):
        self.destroy()
        Menujeu(self.geometria)


def jouer():
    tableau = Menujeu("513x513")
    tableau.mainloop()


if __name__ == "__main__":
    jouer()