import pandas as pd
import random
import csv

pokedex = pd.read_csv('pokedexbien.csv', header=0, index_col="Name")

def minimaxpetit(new_board, player):

    avail_spots = empty_indices(new_board) # Available spots

    if winning(new_board, hu_player):  #here we need the function that checks if this is a winning pos
        return {"score": -10}
    elif winning(new_board, ai_player):
        return {"score": 10}
    elif len(avail_spots) == 0:
        return {"score": 0}

    moves = []  # here we store all the poosible moves and their score

    for i in avail_spots:

        move = {"index": new_board[i]}  # I create a new dictionary


        new_board[i] = player # this is just a simulation to test if I put a player here what will happen


        if player == ai_player: #we get the scores with the minmax
            result = minimax(new_board, hu_player)
            move["score"] = result["score"]
        else:
            result = minimax(new_board, ai_player)
            move["score"] = result["score"]

        # we reset the spot to empty and we append it to our available moves
        new_board[i] = move["index"]

        moves.append(move)

    # here we choose the best move
    best_move = None
    if player == ai_player:
        best_score = -10000000000000000000000000000000000000000000 #I use a very low score and try to find a better score
        for i in range(len(moves)):
            if moves[i]["score"] > best_score:
                best_score = moves[i]["score"]
                best_move = i
    else:
        best_score = 1000000000000000000000000000000000000000000000000 #I do the inverse
        for i in range(len(moves)):
            if moves[i]["score"] < best_score:
                best_score = moves[i]["score"]
                best_move = i
    # Return the chosen move (object) from the moves array
    return moves[best_move]

