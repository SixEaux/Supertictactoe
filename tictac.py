from tkinter import *
class Jeu:
    def __init__(self, root, geometria):

        self.root = root
        self.root.title("SuperTicTacToe")
        self.root.geometry(geometria)
        self.obj = {} # tous les ojets graphiques
        self.tableau = {} # code du tableau c'est 11,12,13,14...
        self.croix = []
        self.rond = [] #positions ou il y a un rond
        self.initialisationgraph()


    def initialisationgraph(self): #creer frames pour chaque garnd carré puis grid
        c = 0
        for p in [(i,j) for i in range(3) for j in range(3) if i+j<=4]:
            f = Frame(self.root, background="black")
            print(f)
            self.tableau[c] = {}
            self.obj[p] = f

            f.grid(row=p[0], column=p[1])
            c+=1

    def creertictac(self, frm):
        pass

    def ptitictac(self):
        pass

    def placement(self, figure, pos):
        pass

    def creerxo(self, signe):
        pass


root = Tk()
g = Jeu(root, "450x450")
root.mainloop()