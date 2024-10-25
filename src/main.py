import itertools
import pandas as pd
import numpy as np
import os
import src.processing as processing
import src.visualization as visualization
import json
import matplotlib.pyplot as plt
# import mpld3

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

def create_cards_heatmap(ax: plt.Axes = None):
    data = visualization.get_data()

    cards_t1 = visualization.format_data(np.array(data['cards']), countwins=True)
    card_ties_t1 = visualization.format_data(np.array(data['card_ties']), countwins=True)
    ct1_annots = visualization.make_annots(cards_t1, card_ties_t1)

    # Create the heatmap on the provided axis
    fig1, ax1 = visualization.make_heatmap(data=cards_t1, annots=ct1_annots, title="My Chance of Winning (By Cards)", n=data['n'], cbar_single=False, ax=ax)
    if not os.path.exists('figures'):
        os.makedirs('figures')
    fig1.savefig('figures/cards_heatmap.png', bbox_inches='tight')
    # mpld3.save_html(fig1, 'figures/cards_heatmap.html')
    return fig1, ax1

def create_tricks_heatmap(ax: plt.Axes = None):
    data = visualization.get_data()

    tricks_t1 = visualization.format_data(np.array(data['tricks']), countwins=True)
    trick_ties_t1 = visualization.format_data(np.array(data['trick_ties']), countwins=True)
    tt1_annots = visualization.make_annots(tricks_t1, trick_ties_t1)

    # Create the heatmap on the provided axis
    fig2, ax2 = visualization.make_heatmap(data=tricks_t1, annots=tt1_annots, title="My Chance of Winning (By Tricks)", n=data['n'], cbar_single=False, ax=ax, hide_y=True)
    if not os.path.exists('figures'):
        os.makedirs('figures')
    fig2.savefig('figures/tricks_heatmap.png', bbox_inches='tight')
    # mpld3.save_html(fig2, 'figures/tricks_heatmap.html')
    return fig2, ax2

def make_heatmap_package() -> [plt.Figure, plt.Axes]:
    '''
    Create a 1x2 grid of heatmaps based on the given data, with shared colorbar.
    '''
    
    # Create a 1x2 grid for the heatmaps
    fig, ax = plt.subplots(1, 2, 
                           figsize=(8*2, 8), 
                           gridspec_kw={'wspace': 0.05})
    
    # Create the heatmaps directly on the axes of the subplot
    create_cards_heatmap(ax=ax[0])
    create_tricks_heatmap(ax=ax[1])
    
    # Add a shared colorbar for the whole figure
    cbar_ax = fig.add_axes([0.92, 0.3, 0.02, 0.4])  # Adjust as needed
    fig.colorbar(ax[0].collections[0], cax=cbar_ax)
    if not os.path.exists('figures'):
        os.makedirs('figures')
    fig.savefig('figures/pkg_heatmap.png', bbox_inches='tight')
    # mpld3.save_html(fig, 'figures/pkg_heatmap.html')
    return fig, ax

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
