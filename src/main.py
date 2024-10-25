import itertools
import pandas as pd
import numpy as np
import os
import src.processing as processing
import src.visualization as visualization
import json

def shuffle_deck(seed:None):
    '''Generates a single shuffled deck'''
    rng = np.random.default_rng(seed = seed)
    deck = np.ndarray.flatten((np.stack((np.ones(26), np.zeros(26)), axis= 0).astype(int)))
    rng.shuffle(deck)
    return ''.join(map(str, deck))

def results_for_viz(x):
    """
    Takes in results from play_n_games() function. Reformats results of simulations for heatmap visualization.
    """
    x['cards'] = x['cards'].tolist()
    x['tricks'] = x['tricks'].tolist()
    x['card_ties'] = x['card_ties'].tolist()
    x['trick_ties'] = x['trick_ties'].tolist()

    data_folder = 'results'
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    with open(os.path.join(data_folder,'results.json'), 'w') as json_file:
        json.dump(x, json_file, indent=4)

def play_n_games(n, data):
    """
    Runs 
    n: number of games user would like to simulate
	data: data folder to store results for each iteration

    """
    if not os.path.exists(data):
        os.makedirs(os.path.join(data,'cards'))
        os.makedirs(os.path.join(data,'card_ties'))
        os.makedirs(os.path.join(data,'tricks'))
        os.makedirs(os.path.join(data,'trick_ties'))

    for i in range(n):
        deck = shuffle_deck(None)
        processing.play_one_deck(data = data, deck = deck)

    filename = ['cards', 'card_ties', 'tricks', 'trick_ties']
    results = {}
    n_games = []

    for folder in filename:
        results[folder], g_num = processing.sum_games(f'{data}/{folder}', True)
        n_games.append(g_num)
    results['n'] = n_games[0]
    # Reformat and save results for viz
    results_for_viz(results)
    return results

def create_final_heatmap():
    data = visualization.get_data()

    ##creating/formatting simulated data for team 1 card_win probabilities and making appropriate annotations 
    cards_t1 = visualization.format_data(np.array(data['cards']), countwins=True)
    card_ties_t1 = visualization.format_data(np.array(data['card_ties']), countwins=True)  
    ct1_annots = visualization.make_annots(cards_t1, card_ties_t1)

    # Create a single map for the card_win probabilties
    fig1, ax1 = visualization.make_heatmap(data=cards_t1, annots=ct1_annots, title="My Chance of Winning (By Cards)", n=data['n'])