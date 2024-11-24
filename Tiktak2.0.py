from tkinter import *
from itertools import cycle

class Jeu:
    def __init__(self):
        self.joueurs = (("X", "red"), ("O", "blue"))
        self.ordre = cycle(self.joueurs) #ordre des joueurs
        self.quijoue = next(self.ordre) #a qui le tour

        self.tableau = {i : ["" for j in range(9)] for i in range(9)} #tableau avec le chiffre de chaque tictactoe et une liste avec le label de chaque case
        self.grostictac = {i:"" for i in range(9)} #chiffre du tictactoe avec "" si pas gagné puis mettre label si gagné
        self.gagne = {(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2, 5, 8), (0,4,8), (2,4,6)} #positions à verifier si gagné

        self.dejagagne = False #estce que il y a déjà un gagnant?
        self.gagnant = ""

    def changejoueur(self):
        self.quijoue = next(self.ordre)

    def mouvpossible(self, mouvement): #regarder su mouvement est possible / mouvement serait surement des coordonnées (grosframe,petitframe)
        if self.tableau[mouvement[0]][mouvement[1]] == "" and :


    def agagnepetit(self, tictac): #regarder si dans le tableau il y a des gagnants, tictac c'est quel tableau des petits
        for i in self.gagne:
            if self.tableau[tictac][i[0]] == self.tableau[tictac][i[1]] == self.tableau[tictac][i[2]] and self.tableau[tictac][i[0]] != "":
                self.grostictac[tictac] = self.tableau[tictac][i[0]]


    def gagnegros(self): #regarder si dans le tableau il y a un gros gagnant
        for i in self.gagne:
            if self.grostictac[i[0]] == self.grostictac[i[1]] == self.grostictac[i[2]]:
                self.gagnetot(self.grostictac[i[0]])

    def gagnetot(self, signe): #le gros tictactoe est gagné et il faut donner qui a gagné
        self.dejagagne = True
        self.gagnant = signe



class Graphique(Tk):
    def __init__(self):
        super().__init__()




def jouer():
    jeu = Jeu()
    tableau = Graphique(jeu)
