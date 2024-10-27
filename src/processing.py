import numpy as np
import pandas as pd
import os
import itertools
from typing import Tuple

def score_deck(deck: str,
               seq1: str,
               seq2: str) -> Tuple[int]:
    '''
    Given a shuffled deck of cards, a sequence chosen by player1, and a sequence chosen by player two, 
    return the number of cards/tricks for each variation of Penney's Game.
    
    Arguments:
        - deck (str): randomly shuffled deck of 52 cards
        - seq1 (str): the 3-card sequence chosen by player 1 (ex. BBB, RBR)
        - seq2 (str): the 3-card sequence chosen by player 2 (ex. RRR, BRB)

    Outputs:
        - p1_cards (int): the number of cards player 1 won
        - p2_cards (int): the number of cards player 2 won
        - p1_tricks (int): the number of tricks player 1 won
        - p2_tricks (int): the number of tricks player 2 won
    '''
    p1_cards = 0
    p2_cards = 0
    pile = 2
    
    p1_tricks = 0
    p2_tricks = 0
    
    i = 0
    while i < len(deck) - 2:
        pile += 1
        current_sequence = deck[i:i+3]
        if current_sequence == seq1:
            p1_cards += pile
            pile = 2
            p1_tricks += 1
            i += 3
        elif current_sequence == seq2:
            p2_cards += pile
            pile = 2 
            p2_tricks += 1
            i += 3
        else:
            i += 1

    return p1_cards, p2_cards, p1_tricks, p2_tricks


def calculate_winner(p1_cards: int,
                     p2_cards: int,
                     p1_tricks: int,
                     p2_tricks: int):
        '''
        Given the number of cards and tricks for each player, calculate who wins for cards and tricks, as well as draws for cards and tricks.
        If player one wins, the winner is set to 0. If player 2 wins, the winner is set to 1.
        Also indicates if there was a draw.

        Arguments:
            p1_cards (int): number of cards player 1 won
            p2_cards (int): number of cards player 2 won
            p1_tricks (int): number of tricks player 1 won
            p2_tricks (int): number of tricks player 2 won
        
        Output:
            cards_winner (int): specifies who won based on cards
            cards_draw (int): 1 if a draw occurred, 0 otherwise
            tricks_winner (int): specifies who won based on tricks
            tricks_draw (int): 1 if a draw occured, 0 otherwise
        '''
        cards_winner = 0
        cards_draw = 0
        tricks_winner = 0
        tricks_draw = 0

        # if p2 wins set winner to 1, otherwise it is 0 (including draws).
        # if there is a draw, set draw counter to 1
        if p1_cards < p2_cards:
            cards_winner = 1
        elif p1_cards == p2_cards:
            cards_draw = 1
        if p1_tricks < p2_tricks:
            tricks_winner = 1
        elif p1_tricks == p2_tricks:
            tricks_draw = 1
        return cards_winner, cards_draw, tricks_winner, tricks_draw


def play_one_deck(deck: str,
                  data: str):
    '''
    For a single deck, this function plays every possible combination of sequences for both players and saves the outcome as .npy arrays.
    
    Arguments:
        - deck (str): a string of either 0 or 1 representing a generated deck.
        - data (str): the data file information is being saved to.
    
    Returns nothing, but saves .npy files for each category (cards, tricks, ties for cards, tricks for cards) to the specified data folder.
    '''
    sequences = ['000', '001', '010', '011', '100', '101', '110', '111']
    combinations = itertools.product(sequences, repeat=2)
    p2_wins_cards = pd.DataFrame(columns=sequences, index=sequences)
    p2_wins_tricks = pd.DataFrame(columns=sequences, index=sequences)
    draws_cards = pd.DataFrame(columns=sequences, index=sequences)
    draws_tricks = pd.DataFrame(columns=sequences, index=sequences)

    for seq1, seq2 in combinations:
        p1_cards, p2_cards, p1_tricks, p2_tricks = score_deck(deck, seq1, seq2)
        cards_winner, cards_draw, tricks_winner, tricks_draw = calculate_winner(p1_cards, p2_cards, p1_tricks, p2_tricks)
        p2_wins_cards.at[seq1, seq2] = cards_winner
        draws_cards.at[seq1, seq2] = cards_draw
        p2_wins_tricks.at[seq1, seq2] = tricks_winner
        draws_tricks.at[seq1, seq2] = tricks_draw
    
    deck_name = str(int(deck, 2))
    np.save(f'{data}/cards/{deck_name}.npy', p2_wins_cards, allow_pickle = True)
    np.save(f'{data}/tricks/{deck_name}.npy', p2_wins_tricks, allow_pickle = True)
    np.save(f'{data}/card_ties/{deck_name}.npy', draws_cards, allow_pickle = True)
    np.save(f'{data}/trick_ties/{deck_name}.npy', draws_tricks, allow_pickle = True)

def sum_games(data: str, average: bool):
    '''
    Iterate over each file in the specified data filepath, and calculates the sum (or the average).

    Arguments:
        - data (str): the filepath to the specified data folder
        - average (bool): if True, returns the average (by dividing by the number of files in the directory)
    
    Output:
        - games_total (numpy.ndarray): a numpy array that either contains:
            - the average of the files if average is True
            - the sum of the files if average is False
        - num_games (int): the number of games played
    '''
    files = [file for file in os.listdir(data) if os.path.isfile(os.path.join(data, file))] # iterate through /data directory, only process files
    games_total = None # where the sum of the games is going
    for file in files:
        file_path = os.path.join(data,file) # get file name and directory
        game = np.load(file_path, allow_pickle=True) # load the file
        if games_total is None:
            games_total = game # initialize games_total sum array
        else:
            games_total += game
    num_games = len(files)
    if average:
        return np.divide(games_total, num_games), num_games
    return games_total, num_games # divide each individual element by the number of games played
