import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import json

# Settings for the individual figures
FIG_HIGH = 8
FIG_WIDE = 8

TITLE_SIZE = 18
LABEL_SIZE = 14
TICKLABEL_SIZE = 12
TICK_SIZE = 10
ANNOT_SIZE = 8


def get_data() -> np.ndarray:
    '''
    Read the JSON file with 5 items in the 'results' folder and return the file contents.
    '''
    file_path = os.path.join('results', 'results.json')

    # Load the JSON file
    with open(file_path, 'r') as json_file:
        x = json.load(json_file)

    return x

def format_data(array: np.ndarray, countwins= False) -> np.ndarray:
    '''
    Cleans the array of probabilities in decimal form to return whole numbers 
    representing the percent out of 100 and fill the 'nonsense' diagonal with None. 
    The diagonal is filled with None so gray is displayed along the diagonal in the visualization.
    '''
    #takes the original decimal probabilities and puts them in the whole number format of percent and fills the 'nonsense' diagonal

    array = array.astype(float)
    if countwins:
        temp = np.flip((np.round((array)*100,0)),0)
    else:
        temp = np.flip((np.round(array)), 0)
        
    flipped = fill_diag(temp, np.nan)
    return flipped

def fill_diag(array: np.ndarray, filler) -> np.ndarray:
    '''
    Sets the diagonal going up (left to right across) to whatever the user specifies as filler. 
    Done when making annotations (filler = "") and when formatting the data (filler=None)
    '''
    
    flipped = np.flip(array, 0)
    np.fill_diagonal(flipped, filler)
    return np.flip(flipped,0)



def make_annots(wins : np.ndarray,ties: np.ndarray) -> np.ndarray:
    '''
    Uses two 8x8 arrays for wins and ties respectively to return one array of strings in the form win(tie)
    The input arrays will need to already have gone through the format_data function or be in that format already
    '''
    annots = []
    for i in range(8):
        row = []
        for j in range(8):
            row.append(f'{str(wins[i,j])[:-2]} ({str(ties[i,j])[:-2]})')
        annots.append(row)
    annots=fill_diag(annots, "")
    return np.array(annots)

def make_heatmap(data: np.ndarray,
                 annots: np.ndarray,
                 title:str,
                 n: int,
                 hide_y: bool = False,
                 cbar_single: bool = True,
                 ax: plt.Axes = None
                ) -> [plt.Figure, plt.Axes]:
    '''
    If ax is None, create a new figure.
    Otherwise, add the heatmap to the provided ax.
    '''
    
    if ax is None:
        # Create a new figure
        fig, ax = plt.subplots(1, 1, figsize=(FIG_WIDE, FIG_HIGH))
    else:
        # Get the parent figure
        fig = ax.get_figure()

    #seqs= ['BBB','BBR','BRB','BRR','RBB','RBR','RRB','RRR'] #if letters are desired tick labels

    seqs = [f'{i:b}'.zfill(3) for i in range(8)] ##if numbers are desired tick labels

    settings = {
        'vmin': 0,
        'vmax': 100,
        'linewidth': .5,
        'cmap': 'Blues',
        'cbar': False,
        'annot': annots,
        'annot_kws': {"size": ANNOT_SIZE},
        'fmt': ''
    }

    
    sns.heatmap(data=data, ax=ax,  **settings)
    ax.set_xlabel('Me', fontsize=LABEL_SIZE)
    ax.set_ylabel('Opponent', fontsize=LABEL_SIZE)
    ax.set_xticklabels(seqs, fontsize=TICK_SIZE)
    ax.set_yticklabels(seqs[::-1], fontsize=TICK_SIZE)
    ax.set_facecolor('#DBDBDB')

    '''
    If a standalone plot is being created, the colorbar should be adjusted in this make_heatmap function 
    If bundled heatmaps are being made, the colorbar will be adjusted in the make_heatmap_package function to avoid double colorbars
    '''

    if cbar_single: 

        cbar_ax = fig.add_axes([.95, 0.11, 0.035, .77])
        cb = fig.colorbar(ax.collections[0], cax=cbar_ax)
        #adjusting the tickmark sizes on colorbar 
        cb.ax.tick_params(labelsize=TICK_SIZE)
        cb.outline.set_linewidth(.2)

    ax.set_title(title+'\n(n='+str(n)+')', fontsize=TITLE_SIZE)
    
    if hide_y: ### for bundled heatmaps, both the yticks and axis title should be hidden on 2nd subplot
        ax.set_yticks([])
        ax.set_ylabel(None)
     
    return fig, ax

def create_final_heatmap():
    data = get_data()

    ##creating/formatting simulated data for team 1 card_win probabilities and making appropriate annotations 
    cards_t1 = format_data(np.array(data['cards']), countwins=True)
    card_ties_t1 = format_data(np.array(data['card_ties']), countwins=True)  
    ct1_annots = make_annots(cards_t1, card_ties_t1)

    # Create a single map for the card_win probabilties
    fig1, ax1 = make_heatmap(data=cards_t1, annots=ct1_annots, title="My Chance of Winning (By Cards)", n=data['n'])