from tkinter import *


class Jeu:
    def __init__(self, root, geometria):

        self.root = root
        self.root.resizable(0, 0)
        self.root.title("SuperTicTacToe")
        self.root.geometry(geometria)
        self.geometry = (geometria[:3], geometria[4:])
        self.frames = {} # tous les ojets graphiques de frames avec en cle la position dans le tableau (1,1) , (1,2) ...
        self.tableau = {} # code du tableau c'est 11,12,13,14...
        self.obj = {i : [] for i in range(9)}
        self.croix = [] #positions avec croix
        self.rond = [] #positions ou il y a un rond
        self.signe = True #True = X et False = O
        self.positionspossibles = [(i,j) for i in range(3) for j in range(3) if i+j<=4]
        self.nseo = ["NW", "N", "NE", "W", None, "E", "SW", "S", "SE"]
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        print(help(self.root.winfo_x))
        print(dir(self.root))

        self.initialisationgraph()







    def initialisationgraph(self): #creer frames pour chaque garnd carré puis grid et ajouter tous les tiktaktoes
        for p in range(len(self.positionspossibles)):
            f = Frame(self.root, background="white")
            self.tableau[p] = {}
            self.frames[p] = f
            f.grid(row=self.positionspossibles[p][0], column=self.positionspossibles[p][1], sticky=self.nseo[p], padx=0, pady=0) #, highlightbackground="blue", highlightthickness=1

        for h in range(9):
            self.creertictac(h)

    def creertictac(self, numpos):
        for p in range(len(self.positionspossibles)):

            b = Button(self.frames[numpos], borderwidth = 1, background="white", foreground="black", command = self.creerxo())
            b.grid(row=self.positionspossibles[p][0], column=self.positionspossibles[p][1], padx=0, pady=0)

            height=round(int(self.geometry[0])/83)/2
            width=round(int(self.geometry[0])/83)
            print(height, width)
            b.config( height =int(height), width =int(width) )

            self.obj[numpos].append((p, b))


    def ptitictac(self):
        pass

    def placement(self, figure, pos):
        pass

    def creerxo(self):
        #utiliser bouton.configure()
        pos = b.grid_location()
        f = b.winfo_parent()

        """
        x = bouton.winfo_rootx()
        y = bouton.winfo_rooty()
        taille = bouton.winfo_height()"""

        b.destroy()
        canvas = Canvas(f, background="white")
        canvas.grid(row = pos[0], column = pos[1])
        canvas.create_text(canvas.winfo_height()/2, canvas.winfo_height()/2, text = "X" )


root = Tk()
g = Jeu(root, "500x500")
root.mainloop()