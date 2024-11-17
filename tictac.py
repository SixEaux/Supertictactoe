from tkinter import *
class Jeu:
    def __init__(self, root, geometria):
        self.grosfram = None
        self.root = root
        self.root.title("SuperTicTacToe")
        self.root.geometry(geometria)

        self.tableau = {j : {i for i in range(9)} for j in range(9)} # code du tableau c'est 11,12,13,14...
        self.croi = []
        self.rond = [] #positions ou il y a un rond
        self.initialisationgraph()


    def initialisationgraph(self): #creer frames pour chaque garnd carré puis grid
        self.grosfram = []
        for p in [(i,j) for i in range(3) for j in range(3) if i+j<=4]:
            f = Frame(self.root, background="black")
            self.grosfram.append((f, p[0], p[1]))
            f.grid(row=p[0], column=p[1])
        

    def ptitictac(self):
        pass

    def placement(self, figure, pos):
        pass




root = Tk()
g = Jeu(root, "450x450")
root.mainloop()