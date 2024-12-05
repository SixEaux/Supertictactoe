position = ["X", "O", "",
            "", "X", "O",
            "", "", ""]

# Appel de l'algorithme
a =
resultat = self.minimaxpetit(position, 3, self.ordijoue)
print("Case choisie :", resultat[0], "Score :", resultat[1])