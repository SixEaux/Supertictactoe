import pandas as pd
import random
import csv

pokedex = pd.read_csv('pokedexbien.csv', header=0, index_col="Name")


def minimaxpetit(self, new_board, player):
    avail_spots = self.casesvide(self.jeutab.tableau[self.jeutab.queltictac])  # Available spots

    if any(self.jeutab.tableau[i[0]] == self.jeutab.tableau[i[1]] == self.jeutab.tableau[i[2]] ==
           self.jeutab.joueurs[self.humain][0] for i in self.jeutab.gagne):
        return {"score": -10}
    elif any(self.jeutab.tableau[i[0]] == self.jeutab.tableau[i[1]] == self.jeutab.tableau[i[2]] ==
             self.jeutab.joueurs[self.ordijoue][0] for i in self.jeutab.gagne):
        return {"score": 10}
    elif len(avail_spots) == 0:
        return {"score": 0}

    moves = []  # here we store all the poosible moves and their score

    for i in avail_spots:

        move = {"index": new_board[i]}  # I create a new dictionary

        new_board[i] = player  # this is just a simulation to test if I put a player here what will happen

        if player == self.ordijoue:  # we get the scores with the minmax
            result = self.minimaxpetit(new_board, self.humain)
            move["score"] = result["score"]
        else:
            result = self.minimaxpetit(new_board, self.ordijoue)
            move["score"] = result["score"]

        # we reset the spot to empty and we append it to our available moves
        new_board[i] = move["index"]

        moves.append(move)

    # here we choose the best move
    best_move1 = None
    if player == self.humain:
        best_score = -10000000000000000000000000000000000000000000  # I use a very low score and try to find a better score
        for i in range(len(moves)):
            if moves[i]["score"] > best_score:
                best_score = moves[i]["score"]
                best_move1 = i
                print(best_move1)
    else:
        best_score = 1000000000000000000000000000000000000000000000000  # I do the inverse
        for i in range(len(moves)):
            if moves[i]["score"] < best_score:
                best_score = moves[i]["score"]
                best_move1 = i
                print(best_move1)
    # Return the chosen move (object) from the moves array
    return self.jeutab.queltictac, moves[best_move1]
