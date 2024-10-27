import itertools
import pandas as pd
import numpy as np
import os
import src.processing as processing
import src.visualization as visualization
import json
from typing import Tuple
import matplotlib.pyplot as plt
import mpld3
from matplotlib.ticker import PercentFormatter

def shuffle_deck(seed:int):
    '''Generates a single shuffled deck of 0s and 1s. 

    Argumements: 
    seed (int): Seed to ensure reproducibility

    Output:
    A string of 52 characters where each character is either '0' or '1', representing a shuffled deck.
    '''
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

def play_n_games(n: int, data: str, initial_seed: int = 0):
    """
    Runs simulations for n games, saving results to the specified data folder.
    
    Parameters:
    - n (int): Number of games to simulate.
    - data (str): Folder to store results for each iteration.
    - initial_seed (int): Starting seed value for random number generation.
    """
    if not os.path.exists(data):
        os.makedirs(os.path.join(data,'cards'))
        os.makedirs(os.path.join(data,'card_ties'))
        os.makedirs(os.path.join(data,'tricks'))
        os.makedirs(os.path.join(data,'trick_ties'))

    for i in range(n):
        deck = shuffle_deck(seed=initial_seed + i)
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

def save_figures(figures, output_html):
    """
    Save figures as images and embed them in an HTML file.
    
    :param figures: List of Matplotlib figures to save
    :param output_html: Output HTML file name
    """
    # Save the figure as a PNG file in the 'figures' folder
    filename = output_html.replace('.html', '.png')
    figures.savefig(filename, bbox_inches='tight')

    # Create HTML
    html_content = html_content = mpld3.fig_to_html(figures)

    # Save the HTML to a file
    with open(output_html, 'w') as f:
        f.write(html_content)


def create_heatmap(variation: str, ax: plt.Axes = None, hide_y: bool = False, pkg: bool = False):
    # Ensure 'figures' directory exists
    if not os.path.exists('figures'):
        os.makedirs('figures')
    
    # Load and format data
    data = visualization.get_data()
    
    # Determine specifications based on either cards or tricks
    if variation == 'cards':
        t1_data = visualization.format_data(np.array(data['cards']), countwins=True)
        ties_data = visualization.format_data(np.array(data['card_ties']), countwins=True)
        title = "My Chance of Winning (By Cards)"
        filename = 'figures/cards_heatmap.html'
    elif variation == 'tricks':
        t1_data = visualization.format_data(np.array(data['tricks']), countwins=True)
        ties_data = visualization.format_data(np.array(data['trick_ties']), countwins=True)
        title = "My Chance of Winning (By Tricks)"
        filename = 'figures/tricks_heatmap.html'
    else:
        raise ValueError("Invalid data_type specified. Use 'cards' or 'tricks'.")

    # Generate annotations
    annots = visualization.make_annots(t1_data, ties_data)

    # Create heatmap
    fig, ax = visualization.make_heatmap(data=t1_data, annots=annots, title=title, n=data['n'], cbar_single=False, ax=ax, hide_y=hide_y)
    ax.set_aspect('equal', adjustable='box')
    
    if not pkg:
        cbar = fig.colorbar(ax.collections[0], ax=ax)
        cbar.ax.yaxis.set_major_formatter(PercentFormatter(xmax=100))
        save_figures(fig, filename)

    return fig, ax

def make_heatmap_package() -> [plt.Figure, plt.Axes]:
    '''
    Create a 1x2 grid of heatmaps based on the given data, with shared colorbar.
    '''
    
    # Create a 1x2 grid for the heatmaps
    fig, ax = plt.subplots(1, 2, 
                           figsize=(8*2, 8), 
                           gridspec_kw={'wspace': 0.05})
    
    # Create the heatmaps directly on the axes of the subplot
    create_heatmap('cards', ax=ax[0],pkg=True)
    create_heatmap('tricks',ax=ax[1], hide_y=True,pkg=True)
    
    # Add a shared colorbar for the whole figure
    cbar_ax = fig.add_axes([0.92, 0.3, 0.02, 0.4])  
    colorbar = fig.colorbar(ax[0].collections[0], cax=cbar_ax)
    colorbar.ax.yaxis.set_major_formatter(PercentFormatter(xmax=100))

    if not os.path.exists('figures'):
        os.makedirs('figures')
    save_figures(fig, 'figures/pkg_heatmap.html')
    fig.savefig('figures/pkg_heatmap.png', bbox_inches='tight')
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
    deck_len = len(deck) - 2

    while i < deck_len:
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
