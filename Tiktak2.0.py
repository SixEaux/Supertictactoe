from tkinter import *
from tkinter import messagebox
from tkinter import font as tkFont
import random
from tabulate import tabulate
import pandas as pd
import copy
from tkinter import Toplevel
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Button, Label
from itertools import cycle


class Menujeu(Tk):
    def __init__(self, geometria, nbpokeparequipe):
        super().__init__()
        self.title("SuperTicTacToe")
        self.geometry(geometria)
        self.geometria = geometria
        self.nbpokeparequipe = nbpokeparequipe
        self.modes = cycle([1,2,3])
        self.modeordi = next(self.modes)
        self.campordi = True
        self.joueurs = {True: "X", False: "O"}
        self.txt = StringVar()
        self.txt.set(f"Niveau {self.modeordi}")
        self.boobool = None
        self.menu_principal()

    def menu_principal(self):
        for widget in self.winfo_children():
            widget.destroy()

        main_menu = Frame(self)
        main_menu.pack()

        Label(main_menu, text="SuperTicTacToe", font=("Helvetica", 24)).pack(pady=20)
        Button(main_menu, text="Avec Pokémon", font=("Helvetica", 16), command=self.menu_pokemon).pack(pady=10)
        Button(main_menu, text="Sans Pokémon", font=("Helvetica", 16), command=self.menu_sans_pokemon).pack(pady=10)
        Button(main_menu, text="Quitter", font=("Helvetica", 16), command=self.quit).pack(pady=10)

    def menu_pokemon(self):
        self.afficher_menu("Avec Pokémon", left_buttons=[("1 VS 1", lambda: self.allerau('pokemon')),
                                                    ("1 VS Ordi", lambda: self.allerau('jouerseulavecpoke'))],
                           right_buttons=[(f"Ordi joue {self.joueurs[self.campordi]}", self.bouton_changerval),
                                          ("Changer mode ordi", lambda: self.changermode())])
        self.boobool = True

    def menu_sans_pokemon(self):
        self.afficher_menu("Sans Pokémon", left_buttons=[("1 VS 1", lambda: self.allerau('jeu')),
                                                         ("1 VS Ordi", lambda: self.allerau('jouerseulsanspoke'))],
                           right_buttons=[(f"Ordi joue {self.joueurs[self.campordi]}", self.bouton_changerval),
                                          ("Changer mode ordi", lambda: self.changermode())])
        self.boobool = False

    def afficher_menu(self, title, left_buttons, right_buttons):
        for widget in self.winfo_children():
            widget.destroy()

        Label(self, text=title, font=("Helvetica", 24)).pack(pady=20)

        button_frame = Frame(self)
        button_frame.pack(fill="both", expand=True)

        left_frame = Frame(button_frame)
        left_frame.pack(side="left", fill="y", expand=True)
        for text, command in left_buttons:
            Button(left_frame, text=text, font=("Helvetica", 14), command=command).pack(pady=5)

        right_frame = Frame(button_frame)
        right_frame.pack(side="right", fill="y", expand=True)
        for text, command in right_buttons:
            Button(right_frame, text=text, font=("Helvetica", 14), command=command).pack(pady=5)

        Label(right_frame, font=("Helvetica", 14), textvariable=self.txt).pack(pady=5)

        Button(self, text="Retour", font=("Helvetica", 16), command=self.retour).pack(pady=20)

    def retour(self):
        self.menu_principal()
        self.boobool = None

    def changermode(self):
        self.modeordi = next(self.modes)
        self.txt.set(f"Niveau {self.modeordi}")

    def bouton_changerval(self):
        self.campordi = not self.campordi
        self.menu_pokemon() if self.boobool else self.menu_sans_pokemon()

    def allerau(self, enquoi):
        self.destroy()
        if enquoi == 'jeu':
            Multijoueur(self.geometria, self.nbpokeparequipe)
        elif enquoi == 'pokemon':
            MultijoueurPokemon(self.geometria, self.nbpokeparequipe)
        elif enquoi == 'jouerseulsanspoke':
            JouerSeulGraphsanspoke(self.geometria, self.nbpokeparequipe, self.modeordi, self.campordi)
        elif enquoi == 'jouerseulavecpoke':
            JouerSeulGraphavecpoke(self.geometria, self.nbpokeparequipe, self.modeordi, self.campordi)


class Jeutab:
    def __init__(self):
        self.joueurs = {True :("X", "red", "indianred", PhotoImage(file = r"Pokeball_rouge.png").subsample(15, 15)),
                        False : ("O", "blue", "lightblue", PhotoImage(file = r"Pokeball_bleu.png").subsample(15, 15))}

        self.quijoue = True #a qui le tour
        self.queltictac = None #ou est-ce que il faut jouer/ si None alors tu peux jouer nimporte ou

        self.tableau = {i : ["" for j in range(9)] for i in range(9)} #tableau avec le chiffre de chaque tictactoe et une liste avec le label de chaque case
        self.grostictac = ["" for i in range(9)] #chiffre du tictactoe avec "" si pas gagné puis mettre label si gagné
        self.gagne = {(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2, 5, 8), (0,4,8), (2,4,6)} #positions à verifier si gagné

        self.fin = False #estce que il y a déjà un gagnant?
        self.gagnant = ""

    def printTableau(self):
        print(tabulate(self.tableau.values(), tablefmt="heavy_outline"))

    def changepos(self, pos):
        return 3*pos[0] + pos[1]

    def changejoueur(self): #passer au joueur suivant
        self.quijoue = not self.quijoue

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
            print("NON")
            return False

    def fairemouvement(self, mouvement):  # faire mouvement dans tableau si possible
        if self.mouvpossible(mouvement):
            self.tableau[mouvement[0]][mouvement[1]] = self.joueurs[self.quijoue][0]
            if self.gagnepetit(mouvement[0]):
                self.grostictac[mouvement[0]] = self.joueurs[self.quijoue][0]
                self.gagnegros()
            elif self.estceegalite(self.tableau[mouvement[0]]):
                self.grostictac[mouvement[0]] = "Imp"
                if self.estceegalite(self.grostictac):
                    self.egalite()

            self.quijoue = not self.quijoue
            self.changetictac(mouvement)

    def gagnepetit(self, tictac): #regarder si dans le tableau il y a des gagnants, tictac c'est quel tableau des petits
        for i in self.gagne:
            if self.tableau[tictac][i[0]] == self.tableau[tictac][i[1]] == self.tableau[tictac][i[2]] != "":
                self.grostictac[tictac] = self.tableau[tictac][i[0]]
                return True
        return False

    def gagnegros(self): #regarder si dans le tableau il y a un gros gagnant
        for i in self.gagne:
            if self.grostictac[i[0]] == self.grostictac[i[1]] == self.grostictac[i[2]] != "":
                self.gagnetot(self.grostictac[i[0]])
                return True
        if self.estceegalite(self.grostictac) and self.fin == False: self.egalite()
        return False

    def gagnetot(self, signe): #le gros tictactoe est gagné et il faut donner qui a gagné
        self.fin = True
        self.gagnant = signe
        print(self.gagnant)

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
        print(self.gagnant)

    def rejouer(self): # remettre tout à zero pour rejouer
        self.fin = False
        self.gagnant = ""
        self.tableau = {i: ["" for j in range(9)] for i in range(9)}
        self.grostictac = ["" for i in range(9)]
        self.queltictac = None
        self.quijoue = True # a qui le tour

class JeutabPokemon(Jeutab):
    def __init__(self, nbequipepoke):
        super().__init__()
        self.definitivementgagne = {i: ["" for j in range(9)] for i in range(9)}

        self.pokedex = pd.read_csv('pokedexbien.csv', header = 0, index_col = "Name")
        self.pokedex["Image"] = self.pokedex.index.map(lambda nom: f"Pokemon Dataset/{nom.lower()}.png")

        self.nbpokeparequipe = nbequipepoke
        a, b = self.selectionner_pokemon()
        self.equipes = {"X": a, "O": b}

        self.pokemonutilise = {i: ["" for j in range(9)] for i in range(9)}  # pokemons qui ont été utilises
        self.pantheonpoke = {"X": [], "O": []}

        self.choixpoke = None

    def changejoueur(self): #passer au joueur suivant
        self.quijoue = not self.quijoue

    def mouvpossiblepoke(self, mouvement):
        if (self.fin == False and (self.queltictac is None or self.queltictac == mouvement[0])
                and self.grostictac[mouvement[0]] == "" and self.definitivementgagne[mouvement[0]][mouvement[1]] == ""):
            return True
        else:
            return False

    def calculate_damage(self, pokemon1, pokemon2):
        Pokemon1 = self.pokedex.loc[pokemon1]
        Pokemon2 = self.pokedex.loc[pokemon2]
        random_factor = random.uniform(0.85, 1.0)  # we use a random factor between 85% and 100%
        type1 = Pokemon1["Type_1"]
        if not pd.isnull(Pokemon1["Type_2"]): #some pokemons only have one typr
            type2 = Pokemon1["Type_2"]
            mc = Pokemon2[type1] * Pokemon2[type2] * random_factor
        else:
            mc = Pokemon2[type1] * random_factor
        damage = (((((Pokemon1["Level"] * 0.4 + 2) * Pokemon1["Attack"]) / Pokemon2["Defense"]) / 50) + 2) * mc * 10 # the link the professor put didnt work so I found this formula on google
        return max(damage, 1)  # pokeons cant deal less than 0 damage because if so we can be stuck in a loop

    def pokemon_combat(self,mouv, poke):
        pokemon11 = self.pokedex.loc[self.pokemonutilise[mouv[0]][mouv[1]]]
        pokemon22 = self.pokedex.loc[poke]
        pokemon1_name = pokemon11.name
        pokemon2_name = pokemon22.name
        HP1 = pokemon11["HP"]
        HP2 = pokemon22["HP"]

        while HP1 > 0 and HP2 > 0: #the pokemons keep fighting until one or both faint, also they both attack at the same time
            damage1 = self.calculate_damage(pokemon1_name, pokemon2_name)
            damage2 = self.calculate_damage(pokemon2_name, pokemon1_name)

            HP1 -= damage2
            HP2 -= damage1

        # We want to check who will win and who will lose
        if HP1 <= 0 and HP2 <= 0:
            print("Both fainted! its a draw.")
            return "Egalite"
        elif HP1 <= 0:
            print(f"{pokemon1_name} is Dead! {pokemon2_name} WINS THE FIGHT.")
            return self.joueurs[self.quijoue][0]
        elif HP2 <= 0:
            print(f"{pokemon2_name} is Dead! {pokemon1_name} WINS THE FIGHT.")
            return self.joueurs[not self.quijoue][0]
        else:
            print("Both Pokémon survived!")
            return "Egalite"

    def changetictac(self, mouvement):
        if self.grostictac[mouvement[1]] == "":
            self.queltictac = mouvement[1]
        elif self.grostictac[mouvement[1]] != "":
            self.queltictac = None

    def selectionner_pokemon(self):
        df = self.pokedex.sample(2 * self.nbpokeparequipe)
        groupe1 = [df.index[0]]
        groupe2 = [df.index[1]]

        somme1 = df.iloc[0]["Total"]
        somme2 = df.iloc[1]["Total"]
        for i in range(2, self.nbpokeparequipe * 2):
            s = df.iloc[i]["Total"]
            if len(groupe2) == self.nbpokeparequipe:
                somme1 += s
                groupe1.append(df.index[i])
            elif len(groupe1) == self.nbpokeparequipe:
                somme2 += s
                groupe2.append(df.index[i])
            elif abs(somme1 + s - somme2) > abs(somme2 + s - somme1):
                somme2 += s
                groupe2.append(df.index[i])
            else:
                somme1 += s
                groupe1.append(df.index[i])

        return groupe1, groupe2

    def gagnepetit(self, tictac): #regarder si dans le tableau il y a des gagnants, tictac c'est quel tableau des petits
        for i in self.gagne:
            if self.tableau[tictac][i[0]] == self.tableau[tictac][i[1]] == self.tableau[tictac][i[2]] != "":
                self.grostictac[tictac] = self.tableau[tictac][i[0]]
                return True
        return False

    def gagnegros(self): #regarder si dans le tableau il y a un gros gagnant
        for i in self.gagne:
            if self.grostictac[i[0]] == self.grostictac[i[1]] == self.grostictac[i[2]] != "":
                self.gagnetot(self.grostictac[i[0]])
                return True
        if self.estceegalite(self.grostictac) and self.fin == False: self.egalite()
        return False

    def gagnetot(self, signe): #le gros tictactoe est gagné et il faut donner qui a gagné
        self.fin = True
        self.gagnant = signe
        print(self.gagnant)

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
        print(self.gagnant)

    def rejouer(self): # remettre tout à zero pour rejouer
        self.fin = False
        self.gagnant = ""
        self.tableau = {i: ["" for j in range(9)] for i in range(9)}
        self.grostictac = ["" for i in range(9)]
        self.definitivementgagne = {i: ["" for j in range(9)] for i in range(9)}
        self.queltictac = None
        # self.ordre = cycle(self.joueurs)  # ordre des joueurs
        self.quijoue = True  # a qui le tour

        a, b = self.selectionner_pokemon()
        self.equipes = {"X": a, "O": b}
        self.pokemonutilise = {i: ["" for j in range(9)] for i in range(9)}  # pokemons qui ont été utilises
        self.choixpoke = None

    #peut etre il faudra faire une fonction pour mouvement et choix de pokemon pour entrainer ia

class Multijoueur(Tk):
    def __init__(self, geometria, nbpokeparequipe):
        Tk.__init__(self)
        self.jeutab = Jeutab()
        self.nbpokeparequipe = nbpokeparequipe

        self.title("Multijoueur")
        self.geometria = tuple(map(int, geometria.split("x"))) #dimensions fenetre
        self.resizable(width=False, height=False)

        self.positionspossibles = [(i,j) for i in range(3) for j in range(3) if i+j<=4] #pour affichage frames
        self.nseo = ["NW", "N", "NE", "W", None, "E", "SW", "S", "SE"] #pour stick frames
        self.font = tkFont.Font(family='Helvetica', size=9, weight=tkFont.BOLD)

        self.txt = StringVar()
        self.label = None

        self.height = round(int(self.geometria[0]) / 83) / 2
        self.width = round(int(self.geometria[0]) / 83)

        print(dir(self))

        self.postofrm = []
        self.butons = {}
        self.butonsinv = {}

        self.initialisationgraph()

    def initialisationgraph(self): #creer frames pour chaque garnd carré puis grid et ajouter tous les tiktaktoes

        for i in range(3):
            self.columnconfigure(i, weight=1, uniform="column")
            self.rowconfigure(i, weight=1, uniform="row")

        for p in range(len(self.positionspossibles)): #creer les frames qui vont contenir tictactoes
            f = LabelFrame(self, background="white", highlightbackground="grey", highlightthickness=2)
            f.grid(row=self.positionspossibles[p][0], column=self.positionspossibles[p][1], sticky=self.nseo[p], padx=3, pady=3)
            self.postofrm.append(f)

        barre = Menu(self)
        options = Menu(barre, tearoff=0, activebackground="grey", activeforeground= "red")
        barre.add_cascade(label="| Options |", menu=options)
        options.add_command(label="Revenir au Menu", command=lambda: self.revenirmenu())
        options.add_separator()
        options.add_command(label="Rejouer", command=lambda: self.rejouer())
        self.config(menu=barre) #ajouter nouvelle command qui renvoie vers instructions

        for h in self.postofrm:
            self.creertictac(h)

        self.rowconfigure(3, weight=3)

        f = LabelFrame(self, background="white", highlightbackground="grey", highlightthickness=2)
        f.grid(row=3, column=1)
        self.txt.set(f"Tour de: {self.jeutab.joueurs[self.jeutab.quijoue][0]}")
        self.label = Label(f, textvariable=self.txt, font=self.font)
        self.label.pack(side=BOTTOM)

    def creertictac(self, frame): #créer petits tiktaktoes
        for p in range(len(self.positionspossibles)):
            frame.rowconfigure(self.positionspossibles[p][0], weight=1, uniform="row1")
            frame.columnconfigure(self.positionspossibles[p][1], weight=1, uniform="column1")
            b = Button(frame, borderwidth = 1, background="white", foreground="black")
            b.config(command = lambda a=b: self.creerxo(a), height =int(self.height), width =int(self.width))
            b.grid(row=self.positionspossibles[p][0], column=self.positionspossibles[p][1], padx=2, pady=2, sticky="nsew")
            self.butons[b] = (self.postofrm.index(frame), p)
            self.butonsinv[(self.postofrm.index(frame), p)] = b

    def creerxo(self, bouton): #creer croix ou ronds
        pos = self.butons[bouton]

        if self.jeutab.fin:
            pass
        elif self.jeutab.mouvpossible(pos):
            self.jeutab.tableau[pos[0]][pos[1]] = self.jeutab.joueurs[self.jeutab.quijoue][0]
            bouton.config(text = self.jeutab.joueurs[self.jeutab.quijoue][0], fg = self.jeutab.joueurs[self.jeutab.quijoue][1], font=self.font)
            self.tourdejeu(pos)
        else:
            messagebox.showwarning("ATTENTION", "Vous avez choisi une case impossible! \n Essayez une autre", parent=self)

    def tourdejeu(self, mouv):
        posfrm = mouv[0]
        tabfrm = self.jeutab.tableau[posfrm]

        if self.jeutab.gagnepetit(posfrm):
            self.jeutab.grostictac[posfrm] = self.jeutab.joueurs[self.jeutab.quijoue][0]
            f = self.postofrm[posfrm]
            self.actualiserfrm(f)

        elif self.jeutab.estceegalite(tabfrm):
            self.jeutab.grostictac[posfrm] = "666"
            for i in self.postofrm[mouv[0]].winfo_children():
                i.config(text="", bg="black")


        self.jeutab.changejoueur()
        self.txt.set(f"Tour de: {self.jeutab.joueurs[self.jeutab.quijoue][0]}")

        if self.jeutab.queltictac is not None:
            self.postofrm[mouv[0]].config(highlightbackground="grey", highlightthickness=2)
        else:
            for i in range(9):
                self.postofrm[i].config(highlightbackground="grey", highlightthickness=2)

        self.jeutab.changetictac(mouv)
        if self.jeutab.queltictac is not None:
            self.postofrm[mouv[1]].config(highlightbackground=self.jeutab.joueurs[self.jeutab.quijoue][1], highlightthickness=2)
        else:
            for i in range(9):
                if self.jeutab.grostictac[i] == '':
                    self.postofrm[i].config(highlightbackground=self.jeutab.joueurs[self.jeutab.quijoue][1], highlightthickness=2)

        if self.jeutab.gagnegros():
            # self.jeutab.changejoueur()
            self.fin(f"{self.jeutab.joueurs[not self.jeutab.quijoue][0]} a gagné!")
        elif self.jeutab.estceegalite(self.jeutab.grostictac):
            self.fin("Egalite")
        return

    def actualiserfrm(self, frm):
        for i in frm.winfo_children():
            i.config(text="", bg = self.jeutab.joueurs[self.jeutab.quijoue][2])

    def fin(self, queltype):
        self.txt.set(queltype)
        self.jeutab.gagnetot(queltype)
        rootsecond = Toplevel()
        rootsecond.title("Cela est un message de fin")

        lab = Label(rootsecond, background="white", text = f"FIN DU JEU \n {queltype} \n Vous pouvez rejouer...\n si vous le souhaitez.", font = self.font)
        lab.pack(side=TOP)
        but = Button(rootsecond, text="Revenir au Jeu", fg="white", bg="black", command=rootsecond.destroy)
        but.pack(side=BOTTOM)
        rootsecond.focus()

    def rejouer(self): #tout remettre en place pour jouer
        for i in self.postofrm:
            for j in i.winfo_children():
                j.config(text="", bg = "white")
        self.txt.set("Prets?")
        if self.jeutab.queltictac is not None:
            self.postofrm[self.jeutab.queltictac].config(highlightbackground="grey", highlightthickness=2)
        self.jeutab.rejouer()

    def revenirmenu(self):
        for i in self.winfo_children():
            i.destroy()
        self.destroy()
        self.jeutab.rejouer()
        Menujeu(f"{self.geometria[0]}x{self.geometria[1]}", self.nbpokeparequipe)

class MultijoueurPokemon(Tk):
    def __init__(self, geometria, nbequipepoke):
        Tk.__init__(self)
        self.jeutab = JeutabPokemon(nbequipepoke)
        self.nbpokeparequipe = nbequipepoke

        self.title("Multijoueur pokemon")
        self.geometria = tuple(map(int, geometria.split("x")))  # dimensions fenetre
        self.resizable(width=False, height=False)

        self.positionspossibles = [(i, j) for i in range(3) for j in range(3) if i + j <= 4]  # pour affichage frames
        self.nseo = ["NW", "N", "NE", "W", None, "E", "SW", "S", "SE"]  # pour stick frames
        self.font = tkFont.Font(family='Helvetica', size=20, weight=tkFont.BOLD)

        self.txt = StringVar()
        self.label = None

        self.height = round(int(self.geometria[0]) / 83) / 2
        self.width = round(int(self.geometria[0]) / 83)

        print(dir(self))

        self.postofrm = []
        self.butons = {}
        self.butonsinv = {}

        self.initialisationgraph()

    def initialisationgraph(self):
        for i in range(3):
            self.columnconfigure(i, weight=1, uniform="column")
            self.rowconfigure(i, weight=1, uniform="row")

        for p in range(len(self.positionspossibles)): #creer les frames qui vont contenir tictactoes
            f = LabelFrame(self, background="white", highlightbackground="grey", highlightthickness=2)
            f.grid(row=self.positionspossibles[p][0], column=self.positionspossibles[p][1], sticky="nsew", padx=3, pady=3)
            self.postofrm.append(f)

        barre = Menu(self)
        options = Menu(barre, tearoff=0, activebackground="grey", activeforeground= "red")
        barre.add_cascade(label="| Options |", menu=options)
        options.add_command(label="Revenir au Menu", command=lambda: self.revenirmenu())
        options.add_separator()
        options.add_command(label="Rejouer", command=lambda: self.rejouer())
        self.config(menu=barre)

        for h in self.postofrm:
            self.creertiktak(h)

        self.rowconfigure(3, weight=3)

        f = LabelFrame(self, background="white", highlightbackground="grey", highlightthickness=2)
        f.grid(row=3, column=1)
        self.txt.set(f"Tour de: {self.jeutab.joueurs[self.jeutab.quijoue][0]}")
        self.label = Label(f, textvariable=self.txt, font=self.font)
        self.label.pack(side=BOTTOM)

    def creertiktak(self, frame):
        for p in range(len(self.positionspossibles)):
            frame.rowconfigure(self.positionspossibles[p][0], weight=1, uniform="row1")
            frame.columnconfigure(self.positionspossibles[p][1], weight=1, uniform="column1")
            b = Button(frame, borderwidth=1, background="white", foreground="black")
            b.config(command=lambda a=b: self.mouvementpoke(a), height=int(self.height),
                     width=int(self.width))
            b.grid(row=self.positionspossibles[p][0], column=self.positionspossibles[p][1], padx=2, pady=2,
                   sticky="nsew")
            self.butons[b] = (self.postofrm.index(frame), p)
            self.butonsinv[(self.postofrm.index(frame), p)] = b

    def mouvementpoke(self, buton, pokemon=None): #si il n'y a aucun pokemon je le mets sinon combat
        mouv = self.butons[buton]
        if self.jeutab.fin:
            pass
        elif self.jeutab.mouvpossiblepoke(mouv):
            if self.jeutab.tableau[mouv[0]][mouv[1]] == "":
                top = Toplevel(self)
                self.choixpokemon(buton, mouv, top)
                self.wait_window(top)
                if self.jeutab.choixpoke is not None:
                    self.apreschoixsanscombat(mouv, buton, self.jeutab.choixpoke)
                else:
                    self.txt.set("NOON")

            elif self.jeutab.tableau[mouv[0]][mouv[1]] == self.jeutab.joueurs[not self.jeutab.quijoue][0]:
                top = Toplevel(self)
                self.choixpokemon(buton, mouv, top)
                self.wait_window(top)
                combat = self.jeutab.pokemon_combat(mouv, self.jeutab.choixpoke)
                print(combat, self.jeutab.choixpoke)
                if combat == self.jeutab.joueurs[not self.jeutab.quijoue][0]:
                    self.jeutab.tableau[mouv[0]][mouv[1]] = self.jeutab.joueurs[self.jeutab.quijoue][0]
                    self.jeutab.definitivementgagne[mouv[0]][mouv[1]] = self.jeutab.joueurs[not self.jeutab.quijoue][0]
                    self.jeutab.equipes[self.jeutab.joueurs[self.jeutab.quijoue][0]].append(self.jeutab.choixpoke)
                    buton.config(image="", text = self.jeutab.joueurs[not self.jeutab.quijoue][0], fg=self.jeutab.joueurs[not self.jeutab.quijoue][1])
                    self.tourdejeu(mouv)

                elif combat == self.jeutab.joueurs[self.jeutab.quijoue][0]:
                    self.jeutab.equipes[self.jeutab.joueurs[not self.jeutab.quijoue][0]].append(self.jeutab.pokemonutilise[mouv[0]][mouv[1]]) #il ajoute des pokemnos deux fois de suite
                    self.jeutab.tableau[mouv[0]][mouv[1]] = self.jeutab.joueurs[self.jeutab.quijoue][0]
                    self.jeutab.definitivementgagne[mouv[0]][mouv[1]] = self.jeutab.joueurs[self.jeutab.quijoue][0]
                    self.jeutab.pokemonutilise[mouv[0]][mouv[1]] = self.jeutab.choixpoke
                    buton.config(image="", text=self.jeutab.joueurs[self.jeutab.quijoue][0], fg=self.jeutab.joueurs[self.jeutab.quijoue][1])
                    self.tourdejeu(mouv)

                elif combat=="Egalite":
                    self.jeutab.tableau[mouv[0]][mouv[1]] = ""
                    self.jeutab.equipes[self.jeutab.joueurs[not self.jeutab.quijoue][0]].append(self.jeutab.pokemonutilise[mouv[0]][mouv[1]])
                    self.jeutab.equipes[self.jeutab.joueurs[self.jeutab.quijoue][0]].append(self.jeutab.choixpoke)
                    buton.config(image="", text="")
                    return

                else:
                    print("Je ne sais pas pourquoi")

            else:
                messagebox.showwarning("ATTENTION", "Vous avez choisi une case impossible! \n Essayez une autre",parent=self)

        else:
            messagebox.showwarning("ATTENTION", "Vous avez choisi une case impossible! \n Essayez une autre", parent=self)

        if self.jeutab.gagnegros():
            self.fin(f"{self.jeutab.joueurs[not self.jeutab.quijoue][0]} a gagné!")

        elif self.jeutab.estceegalite(self.jeutab.grostictac):
            self.fin("Egalite")


    def choixpokemon(self, buton, mouv, top):
        fenetre_pokemons = top
        fenetre_pokemons.title("Choisissez un Pokémon")
        fenetre_pokemons.geometry("713x613")

        fenetre_pokemons.grab_set()  #empêche l'interaction avec les autres fenêtres

        joueur_actuel = self.jeutab.joueurs[self.jeutab.quijoue][0]
        pokemons_dispo = self.jeutab.equipes[joueur_actuel]
        pages = [pokemons_dispo[i:i + 20] for i in range(0, len(pokemons_dispo), 20)]  #20 Pokémon par page (5x4)
        page_actuelle = [0]  #permet de suivre la page actuelle
        self.images_pokemon = []

        def afficher_page(page_num):
            for widget in fenetre_pokemons.winfo_children():
                widget.destroy()

            frame_grille = Frame(fenetre_pokemons)
            frame_grille.pack(expand=True, fill="both", padx=10, pady=10)

            ligne, colonne = 0, 0
            for pokemon in pages[page_num]:
                image = Image.open(self.jeutab.pokedex.loc[pokemon]["Image"]).resize((80, 80))
                photo = ImageTk.PhotoImage(image)
                self.images_pokemon.append(photo)
                stats = self.jeutab.pokedex.loc[pokemon][["HP", "Attack", "Defense"]]
                stats_text = f"HP: {stats['HP']} | Attaque: {stats['Attack']} | Défense: {stats['Defense']}"

                bouton = Button(frame_grille, text=f"{pokemon}\n{stats_text}", image=photo, compound="top",
                                command=lambda p=pokemon: self.choisir_pokemon(fenetre_pokemons, p),
                                width=120, height=120, wraplength=120)
                bouton.grid(row=ligne, column=colonne, padx=5, pady=5)

                colonne += 1
                if colonne == 5:
                    colonne = 0
                    ligne += 1


            tourner_page = Frame(fenetre_pokemons)
            tourner_page.pack(pady=5)  #placer directement sous la grille

            if page_num > 0:
                Button(tourner_page, text="Page précédente",
                       command=lambda: afficher_page(page_num - 1),
                       width=15).pack(side="left", padx=10)

            if page_num < len(pages) - 1:
                Button(tourner_page, text="Page suivante",
                       command=lambda: afficher_page(page_num + 1),
                       width=15).pack(side="right", padx=10)
        afficher_page(page_actuelle[0]) #afficher la première page

    def choisir_pokemon(self, fen, pokemon):
        self.jeutab.choixpoke = pokemon
        print(f"Pokémon choisi : {pokemon}")
        fen.destroy()

    def choisi(self, objchoix, fen, buton, mouv):
        self.jeutab.choixpoke = objchoix.get()
        if self.jeutab.choixpoke != "":
            fen.destroy()
            self.focus()
            return
        else:
            return

    def apreschoixsanscombat(self, mouv, buton, poke):
        self.jeutab.tableau[mouv[0]][mouv[1]] = self.jeutab.joueurs[self.jeutab.quijoue][0]
        self.jeutab.pokemonutilise[mouv[0]][mouv[1]] = poke
        self.jeutab.equipes[self.jeutab.joueurs[self.jeutab.quijoue][0]].remove(poke)
        buton.config(image=self.jeutab.joueurs[self.jeutab.quijoue][3])
        self.tourdejeu(mouv)
        return

    def tourdejeu(self, mouv):
        posfrm = mouv[0]
        tabframdef = self.jeutab.definitivementgagne[posfrm]

        if self.jeutab.gagnepetit(posfrm):
            self.jeutab.grostictac[posfrm] =self.jeutab.joueurs[self.jeutab.quijoue][0]
            f = self.postofrm[posfrm]
            self.actualiserfrm(f)

        elif self.jeutab.estceegalite(tabframdef):
            self.jeutab.grostictac[posfrm] = "666"
            for i in self.postofrm[mouv[0]].winfo_children():
                i.config(text="", bg="black")

        self.jeutab.changejoueur()
        self.txt.set(f"Tour de: {self.jeutab.joueurs[self.jeutab.quijoue][0]}")
        if self.jeutab.queltictac is not None:
            self.postofrm[mouv[0]].config(highlightbackground="grey", highlightthickness=2)
        else:
            for i in range(9):
                self.postofrm[i].config(highlightbackground="grey", highlightthickness=2)

        self.jeutab.changetictac(mouv)

        if self.jeutab.queltictac is not None:
            self.postofrm[mouv[1]].config(highlightbackground=self.jeutab.joueurs[self.jeutab.quijoue][1],
                                          highlightthickness=2)
        else:
            for i in range(9):
                if self.jeutab.grostictac[i] == '':
                    self.postofrm[i].config(highlightbackground=self.jeutab.joueurs[self.jeutab.quijoue][1],
                                            highlightthickness=2)

        self.jeutab.choixpoke = None

    def actualiserfrm(self, frm):
        for i in frm.winfo_children():
            i.config(text="", bg = self.jeutab.joueurs[self.jeutab.quijoue][2], image="")

    def fin(self, queltype):
        self.txt.set(queltype)
        self.jeutab.gagnetot(queltype)
        rootsecond = Toplevel()
        rootsecond.title("Cela est un message de fin")

        lab = Label(rootsecond, background="white", text = f"FIN DU JEU \n {queltype} \n Vous pouvez rejouer...\n si vous le souhaitez.", font = self.font)
        lab.pack(side=TOP)
        but = Button(rootsecond, text="Revenir au Jeu", fg="white", bg="black", command=rootsecond.destroy)
        but.pack(side=BOTTOM)
        rootsecond.focus()

    def revenirmenu(self):
        for i in self.winfo_children():
            i.destroy()
        self.destroy()
        self.jeutab.rejouer()
        Menujeu(f"{self.geometria[0]}x{self.geometria[1]}", self.nbpokeparequipe)

    def rejouer(self): #tout remettre en place pour jouer
        for i in self.postofrm:
            for j in i.winfo_children():
                j.config(text="", bg = "white", image="")
        self.txt.set("Prets?")
        if self.jeutab.queltictac is not None:
            self.postofrm[self.jeutab.queltictac].config(highlightbackground="grey", highlightthickness=2)
        self.jeutab.rejouer()

class JouerSeulGraphsanspoke(Multijoueur):
    def __init__(self, geometria, nbpokeparequipe, modeordi, campordi):
        super().__init__(geometria, nbpokeparequipe)
        self.title("Jouer seul sans pokemon")
        self.ordijoue = campordi #joue les x
        self.humain = not campordi
        self.modeordi = modeordi
        self.prof = 5
        self.jouerordi()

    def aleatoire(self):
        if self.jeutab.fin:
            return
        if self.jeutab.queltictac is None:
            choixgros = random.choice(self.casesvide(self.jeutab.grostictac))
            choixpetit = random.choice(self.casesvide(self.jeutab.tableau[choixgros]))
            choix = (choixgros, choixpetit)
            self.creerxo(self.butonsinv[(choix[0], choix[1])])
        else:
            choixpetit = random.choice(self.casesvide(self.jeutab.tableau[self.jeutab.queltictac]))
            choix = (self.jeutab.queltictac, choixpetit)
            self.creerxo(self.butonsinv[(choix[0], choix[1])])

    def casesvide(self, tab):
        vide = []
        for i in range(9):
            if tab[i] == "":
                vide.append(i)
        return vide

    def jeuavecptiminimax(self):
        if self.jeutab.queltictac is None:
            num = self.minimaxpetit(self.jeutab.grostictac.copy(), self.prof, self.jeutab.quijoue) # faire qu'il choissise où jouer en activant la fonction dans le gros tictac
            new_board = copy.deepcopy(self.jeutab.tableau[num[0]])
            choix = self.minimaxpetit(new_board, self.prof, self.jeutab.quijoue)
            self.creerxo(self.butonsinv[(num[0], choix[0])])
        else:
            new_board = copy.deepcopy(self.jeutab.tableau[self.jeutab.queltictac])
            choix = self.minimaxpetit(new_board, self.prof, self.ordijoue)
            self.creerxo(self.butonsinv[(self.jeutab.queltictac, choix[0])])

    def gagnepetit2(self, tab):
        for i in self.jeutab.gagne:
            if tab[i[0]] == tab[i[1]] == tab[i[2]] != "":
                return True
        return False

    def minimaxpetit(self, position, prof, joueur):
        meilleur = [-1, float('-inf')] if joueur == self.ordijoue else [-1, float('inf')]

        if prof == 0 or self.gagnepetit2(position) or self.jeutab.estceegalite(position) or not self.casesvide(position):
            return [-1, self.evaluposition(position)]

        for case in self.casesvide(position):
            pos = position.copy()
            pos[case] = self.jeutab.joueurs[joueur][0]
            res = self.minimaxpetit(pos, prof-1, not joueur)
            res[0] = case
            # print(res)
            # print(pos)
            if joueur == self.ordijoue and res[1] > meilleur[1]:
                meilleur = res
            elif joueur == self.humain and res[1] < meilleur[1]:
                meilleur = res
        return meilleur

    def evaluposition(self, position):
        for i in self.jeutab.gagne:
            if position[i[0]] == position[i[1]] == position[i[2]] != "":
                if position[i[0]] == self.jeutab.joueurs[self.ordijoue][0]:
                    return 100
                elif position[i[0]] == self.jeutab.joueurs[self.humain][0]:
                    return -100
        return 0

    def jouerordi(self):
        if self.jeutab.quijoue == self.ordijoue:
            if self.modeordi == 1:
                self.aleatoire()
            if self.modeordi == 2:
                self.jeuavecptiminimax()
            if self.modeordi == 3:
                self.jeuminmaxGrand()
        else:
            pass

    def tourdejeu(self, mouv):
        posfrm = mouv[0]
        tabfrm = self.jeutab.tableau[posfrm]

        if self.jeutab.gagnepetit(posfrm):
            self.jeutab.grostictac[posfrm] = self.jeutab.joueurs[self.jeutab.quijoue][0]
            f = self.postofrm[posfrm]
            self.actualiserfrm(f)

        elif self.jeutab.estceegalite(tabfrm):
            self.jeutab.grostictac[posfrm] = "666"
            for i in self.postofrm[mouv[0]].winfo_children():
                i.config(text="", bg="black")

        self.jeutab.changejoueur()
        self.txt.set(f"Tour de: {self.jeutab.joueurs[self.jeutab.quijoue][0]}")

        if self.jeutab.queltictac is not None:
            self.postofrm[mouv[0]].config(highlightbackground="grey", highlightthickness=2)
        else:
            for i in range(9):
                self.postofrm[i].config(highlightbackground="grey", highlightthickness=2)

        self.jeutab.changetictac(mouv)

        if self.jeutab.queltictac is not None:
            self.postofrm[mouv[1]].config(highlightbackground=self.jeutab.joueurs[self.jeutab.quijoue][1],
                                          highlightthickness=2)
        else:
            for i in range(9):
                if self.jeutab.grostictac[i] == '':
                    self.postofrm[i].config(highlightbackground=self.jeutab.joueurs[self.jeutab.quijoue][1],
                                            highlightthickness=2)

        if self.jeutab.gagnegros():
            # self.jeutab.changejoueur()
            self.fin(f"{self.jeutab.joueurs[not self.jeutab.quijoue][0]} a gagné!")
        elif self.jeutab.estceegalite(self.jeutab.grostictac):
            self.fin("Egalite")

        self.jouerordi()
        return

class JouerSeulGraphavecpoke(MultijoueurPokemon):
    def __init__(self, geometria, nbpokeparequipe, modeordi, campordi):
        super().__init__(geometria, nbpokeparequipe)
        self.title("Jouer seul avec pokemon")
        self.ordi = campordi #joue les x
        self.humain = not campordi
        self.modeordi = modeordi
        self.probaspoke = pd.read_csv("PokemonProbs.csv", index_col = 0)
        self.jouerordi(True)

    def casesvide(self, tab1, tab2=None):
        vide = []
        for i in range(9):
            if tab1[i] == "" and (tab2 is None or tab2[i] != self.jeutab.joueurs[self.jeutab.quijoue][0]):
                vide.append(i)
        return vide

    def aleatoire(self):
        if self.jeutab.queltictac is None:
            choixgros = random.choice(self.casesvide(self.jeutab.grostictac))
            choixpetit = random.choice(self.casesvide(self.jeutab.definitivementgagne[choixgros], self.jeutab.tableau[choixgros])) #erreur vient du faite qu'il choisit une case qui est placee par lui
            choix = (choixgros, choixpetit)
            self.mouvementpoke(self.butonsinv[(choix[0], choix[1])])
        else:
            choixpetit = random.choice(self.casesvide(self.jeutab.definitivementgagne[self.jeutab.queltictac], self.jeutab.tableau[self.jeutab.queltictac])) #erreur vient du faite qu'il choisit une case qui est placee par lui
            choix = (self.jeutab.queltictac, choixpetit)
            pokemon = random.choice(self.jeutab.equipes[self.jeutab.joueurs[self.ordi][0]])
            self.mouvementpoke(self.butonsinv[(choix[0], choix[1])], pokemon)

    def jouerordi(self, bool = False):
        if not bool:
            self.after(400)
        if self.jeutab.quijoue == self.ordi:
            if self.modeordi == 1:
                self.aleatoire()
        else:
            pass

    def mouvementpoke(self, buton, p=None):
        if self.jeutab.quijoue == self.humain:
            mouv = self.butons[buton]
            if self.jeutab.fin:
                pass
            elif self.jeutab.mouvpossiblepoke(mouv):
                if self.jeutab.tableau[mouv[0]][mouv[1]] == "":
                    top = Toplevel(self)
                    self.choixpokemon(buton, mouv, top)
                    self.wait_window(top)
                    if self.jeutab.choixpoke is not None:
                        self.apreschoixsanscombat(mouv, buton, self.jeutab.choixpoke)
                    else:
                        self.txt.set("NOON")

                elif self.jeutab.tableau[mouv[0]][mouv[1]] == self.jeutab.joueurs[not self.jeutab.quijoue][0]:
                    top = Toplevel(self)
                    self.choixpokemon(buton, mouv, top)
                    self.wait_window(top)
                    combat = self.jeutab.pokemon_combat(mouv, self.jeutab.choixpoke)
                    if combat == self.jeutab.joueurs[not self.jeutab.quijoue][0]:
                        self.jeutab.tableau[mouv[0]][mouv[1]] = self.jeutab.joueurs[self.jeutab.quijoue][0]
                        self.jeutab.definitivementgagne[mouv[0]][mouv[1]] = \
                        self.jeutab.joueurs[not self.jeutab.quijoue][0]
                        self.jeutab.equipes[self.jeutab.joueurs[self.jeutab.quijoue][0]].append(self.jeutab.choixpoke)
                        buton.config(image="", text=self.jeutab.joueurs[not self.jeutab.quijoue][0],
                                     fg=self.jeutab.joueurs[not self.jeutab.quijoue][1])
                        self.tourdejeu(mouv)

                    elif combat == self.jeutab.joueurs[self.jeutab.quijoue][0]:
                        self.jeutab.equipes[self.jeutab.joueurs[not self.jeutab.quijoue][0]].append(
                            self.jeutab.pokemonutilise[mouv[0]][mouv[1]])  # il ajoute des pokemnos deux fois de suite
                        self.jeutab.tableau[mouv[0]][mouv[1]] = self.jeutab.joueurs[self.jeutab.quijoue][0]
                        self.jeutab.definitivementgagne[mouv[0]][mouv[1]] = self.jeutab.joueurs[self.jeutab.quijoue][0]
                        self.jeutab.pokemonutilise[mouv[0]][mouv[1]] = self.jeutab.choixpoke
                        buton.config(image="", text=self.jeutab.joueurs[self.jeutab.quijoue][0],
                                     fg=self.jeutab.joueurs[self.jeutab.quijoue][1])
                        self.tourdejeu(mouv)

                    elif combat == "Egalite":
                        self.jeutab.tableau[mouv[0]][mouv[1]] = ""
                        self.jeutab.equipes[self.jeutab.joueurs[not self.jeutab.quijoue][0]].append(
                            self.jeutab.pokemonutilise[mouv[0]][mouv[1]])
                        self.jeutab.equipes[self.jeutab.joueurs[self.jeutab.quijoue][0]].append(self.jeutab.choixpoke)
                        buton.config(image="", text="")
                        return

                    else:
                        print("Je ne sais pas pourquoi")

                else:
                    messagebox.showwarning("ATTENTION", "Vous avez choisi une case impossible! \n Essayez une autre",
                                           parent=self)

            else:
                messagebox.showwarning("ATTENTION", "Vous avez choisi une case impossible! \n Essayez une autre",
                                       parent=self)

            if self.jeutab.gagnegros():
                self.fin(f"{self.jeutab.joueurs[not self.jeutab.quijoue][0]} a gagné!")

            elif self.jeutab.estceegalite(self.jeutab.grostictac):
                self.fin("Egalite")
        else:
            mouv = self.butons[buton]
            if self.jeutab.fin:
                pass
            elif self.jeutab.mouvpossiblepoke(mouv):
                if self.jeutab.tableau[mouv[0]][mouv[1]] == "":
                    pokemon = random.choice(self.jeutab.equipes[self.jeutab.joueurs[self.ordi][0]])
                    self.apreschoixsanscombat(mouv, buton, pokemon)

                elif self.jeutab.tableau[mouv[0]][mouv[1]] == self.jeutab.joueurs[not self.jeutab.quijoue][0]:
                    pokemon = self.choixordi(self.jeutab.pokemonutilise[mouv[0]][mouv[1]])

                    combat = self.jeutab.pokemon_combat(mouv, pokemon)

                    if combat == self.jeutab.joueurs[not self.jeutab.quijoue][0]:
                        self.jeutab.tableau[mouv[0]][mouv[1]] = self.jeutab.joueurs[not self.jeutab.quijoue][0]
                        self.jeutab.definitivementgagne[mouv[0]][mouv[1]] = self.jeutab.joueurs[not self.jeutab.quijoue][0]
                        self.jeutab.equipes[self.jeutab.joueurs[self.jeutab.quijoue][0]].append(self.jeutab.choixpoke)
                        buton.config(image="", text=self.jeutab.joueurs[not self.jeutab.quijoue][0],
                                     fg=self.jeutab.joueurs[not self.jeutab.quijoue][1])
                        self.tourdejeu(mouv)

                    elif combat == self.jeutab.joueurs[self.jeutab.quijoue][0]:
                        self.jeutab.equipes[self.jeutab.joueurs[not self.jeutab.quijoue][0]].append(self.jeutab.pokemonutilise[mouv[0]][mouv[1]])  # il ajoute des pokemnos deux fois de suite
                        self.jeutab.tableau[mouv[0]][mouv[1]] = self.jeutab.joueurs[self.jeutab.quijoue][0]
                        self.jeutab.definitivementgagne[mouv[0]][mouv[1]] = self.jeutab.joueurs[self.jeutab.quijoue][0]
                        self.jeutab.pokemonutilise[mouv[0]][mouv[1]] = pokemon
                        buton.config(image="", text=self.jeutab.joueurs[self.jeutab.quijoue][0],fg=self.jeutab.joueurs[self.jeutab.quijoue][1])
                        self.tourdejeu(mouv)

                    elif combat == "Egalite":
                        self.jeutab.tableau[mouv[0]][mouv[1]] = ""
                        self.jeutab.equipes[self.jeutab.joueurs[not self.jeutab.quijoue][0]].append(self.jeutab.pokemonutilise[mouv[0]][mouv[1]])
                        self.jeutab.equipes[self.jeutab.joueurs[self.jeutab.quijoue][0]].append(self.jeutab.choixpoke)
                        buton.config(image="", text="")
                        self.tourdejeu(mouv)

    def tourdejeu(self, mouv):
        posfrm = mouv[0]
        tabframdef = self.jeutab.definitivementgagne[posfrm]

        if self.jeutab.gagnepetit(posfrm):
            self.jeutab.grostictac[posfrm] = self.jeutab.joueurs[self.jeutab.quijoue][0]
            f = self.postofrm[posfrm]
            self.actualiserfrm(f)

        elif self.jeutab.estceegalite(tabframdef):
            self.jeutab.grostictac[posfrm] = "666"
            for i in self.postofrm[mouv[0]].winfo_children():
                i.config(text="", bg="black")

        self.jeutab.changejoueur()
        self.txt.set(f"Tour de: {self.jeutab.joueurs[self.jeutab.quijoue][0]}")
        if self.jeutab.queltictac is not None:
            self.postofrm[mouv[0]].config(highlightbackground="grey", highlightthickness=2)
        else:
            for i in range(9):
                self.postofrm[i].config(highlightbackground="grey", highlightthickness=2)

        self.jeutab.changetictac(mouv)

        if self.jeutab.queltictac is not None:
            self.postofrm[mouv[1]].config(highlightbackground=self.jeutab.joueurs[self.jeutab.quijoue][1],
                                          highlightthickness=2)
        else:
            for i in range(9):
                if self.jeutab.grostictac[i] == '':
                    self.postofrm[i].config(highlightbackground=self.jeutab.joueurs[self.jeutab.quijoue][1],
                                            highlightthickness=2)
        self.jeutab.choixpoke = None

        self.jouerordi()
        return

    def choixordi(self, pokegag):
        poke = self.probaspoke.loc[pokegag]
        pokeligne = poke[poke >= 0.8].to_dict()
        print(pokeligne.keys())
        equipeset = set(self.jeutab.equipes[self.jeutab.joueurs[self.ordi][0]])
        print(equipeset)
        inter = set(pokeligne.keys()).intersection(equipeset)
        return random.choice(list(inter)) if inter else random.choice(self.jeutab.joueurs[self.ordi][0])

    def rejouer(self):
        for i in self.postofrm:
            for j in i.winfo_children():
                j.config(text="", bg="white", image="")
        self.txt.set("Prets?")
        if self.jeutab.queltictac is not None:
            self.postofrm[self.jeutab.queltictac].config(highlightbackground="grey", highlightthickness=2)
        self.jeutab.rejouer()
        self.jouerordi(True)

def jouer(): #ameliorer le code en mettant toutes les varaibles non graphiques dans une class jeutabpokemon et
                                        #ainsi pouvoir faire plus facilement les algos de résolution
    tableau = Menujeu("513x513", 60)
    tableau.mainloop()

if __name__ == "__main__":
    jouer()