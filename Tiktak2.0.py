from tkinter import *
from itertools import cycle
from tabulate import tabulate

import tictac


class Jeu:
    def __init__(self):
        self.joueurs = (("X", "red"), ("O", "blue"))
        self.ordre = cycle(self.joueurs) #ordre des joueurs
        self.quijoue = next(self.ordre) #a qui le tour
        self.queltictac = None #ou est-ce que il faut jouer/ si None alors tu peuc jouer nimporte ou

        self.tableau = {i : ["" for j in range(9)] for i in range(9)} #tableau avec le chiffre de chaque tictactoe et une liste avec le label de chaque case
        self.grostictac = {i:"" for i in range(9)} #chiffre du tictactoe avec "" si pas gagné puis mettre label si gagné
        self.gagne = {(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2, 5, 8), (0,4,8), (2,4,6)} #positions à verifier si gagné

        self.dejagagne = False #estce que il y a déjà un gagnant?
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
        if (self.dejagagne == False and (self.queltictac is None or self.queltictac == mouvement[0])
                and self.grostictac[mouvement[0]] == "" and self.tableau[mouvement[0]][mouvement[1]] == ""):
            print(mouvement, self.dejagagne, self.queltictac, self.grostictac[mouvement[0]], self.tableau[mouvement[0]][mouvement[1]])
            return True
        else:
            print(mouvement, self.dejagagne, self.queltictac, self.grostictac[mouvement[0]],
                  self.tableau[mouvement[0]][mouvement[1]])
            return False

    def fairemouvement(self, mouvement):
        if  self.mouvpossible(mouvement):
            self.tableau[mouvement[0]][mouvement[1]] = self.quijoue[0]
            self.gagnepetit(mouvement[0])
            if self.estceegalite(mouvement):
                self.grostictac[mouvement[0]] = "N"
            self.gagnegros()
            self.quijoue = next(self.ordre)
            self.changetictac(mouvement)

        else:
            print("Ce mouvement n'est pas possible")

    def gagnepetit(self, tictac): #regarder si dans le tableau il y a des gagnants, tictac c'est quel tableau des petits
        for i in self.gagne:
            if self.tableau[tictac][i[0]] == self.tableau[tictac][i[1]] == self.tableau[tictac][i[2]] != "":
                self.grostictac[tictac] = self.tableau[tictac][i[0]]

    def gagnegros(self): #regarder si dans le tableau il y a un gros gagnant
        for i in self.gagne:
            if self.grostictac[i[0]] == self.grostictac[i[1]] == self.grostictac[i[2]] != "":
                self.gagnetot(self.grostictac[i[0]])
        if self.estceegalite(list(self.grostictac.keys())) and self.dejagagne == False: self.egalite()

    def gagnetot(self, signe): #le gros tictactoe est gagné et il faut donner qui a gagné
        self.dejagagne = True
        self.gagnant = signe

    def estceegalite(self, mouvement):
        cpt = 0
        for i in self.tableau[mouvement[0]]:
            if i == "": cpt += 1
        if cpt == 0:
            return True
        else:
            return False

    def egalite(self):
        self.dejagagne = True
        self.gagnant = "Aucun des deux"

    def rejouer(self):
        self.dejagagne = False
        self.gagnant = ""
        self.tableau = {i: ["" for j in range(9)] for i in range(9)}
        self.grostictac = {i: "" for i in range(9)}


class Graphique(Tk):
    def __init__(self):
        super().__init__()




def jouer():
    jeu = Jeu()
    jeu.fairemouvement((0,0))
    jeu.fairemouvement((1, 4))
    jeu.printTableau()
    # tableau = Graphique(jeu)


if __name__ == "__main__":
    jouer()