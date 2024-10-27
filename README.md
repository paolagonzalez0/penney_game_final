# Penney's Game Project

###  "In poker and in life, the game isn’t about the cards you’re dealt but how you play them." - Anon

## Description
Penney's game is a card game where two players choose a pattern (like red, black, black) and play cards from the deck until that pattern appears. Scores can be calculated using cards (the number of total cards up until a pattern is found) or tricks (the number of times the pattern is found).

This project simulates Penney’s Game with both cards and tricks to determine the optimal starting sequences. There is a strategic advantage based on how sequences are chosen, despite the appearance of fairness. First, let your opponent choose their sequence. Then, choose a sequence that is statistically more likely to appear before your opponent's sequence by following this pattern: (not second choice) (first choice) (second choice). For example, if the pattern of your opponent’s sequence is 121, your sequence should be 112 to increase your chances of a win. This strategy prompted the main research questions explored in this analysis, which include:
- How does Penney’s game’s win probability differ when we score based on trick counts rather than card counts? Why?
- Does the winner probability change when ties are accounted for in each play?
- Does scoring by tricks or total cards have an impact on any particular game?
- If the players select their sequences privately, do strategies exist that are better than randomly guessing?

A full explanation of the game and win strategy can be found in the following links:

https://en.wikipedia.org/wiki/Penney%27s_game

https://www.datascienceassn.org/sites/default/files/Humble-Nishiyama%20Randomness%20Game%20-%20A%20New%20Variation%20on%20Penney%27s%20Coin%20Game.pdf


## Getting Started

An example for how to run this program can be found in final_run.ipynb.

*Warning: downloading the data directory is a computationally expensive process and is not nessecarily recommended.*

To begin, you'll need to import the `main` file.
```
import src.main as main
```

### Run a specified number of games using `run_n_games`
```
main.run_n_games(n=5, data='data/')
```
#### Options:
- `n`: the number of games to play
- `data`: the path to your data folder. If you don't have a data folder, just input the name you want your data folder to have, and `play_n_games` will make it for you.

### Visualize and compare results using `make_heatmap_package`

```
main.make_heatmap_package()
```

## Folders and files included
- `data/`: The data generated (currently about 1 million entries per folder).
    - `cards`, `card_ties`, `tricks`, `trick_ties`: folders within the `data` folder, each containing .npy files that represent different games. `cards` stores results for cards, `card_ties` stores ties for cards, `tricks` stores results for tricks, and `tricks_ties` stores ties for tricks.
- `results/`: the .json file storing the current results
- `figures/`: Stores the results for the heatmaps.
- `src/`: Folder containing backend python script code for penney project.
    - `main.py`: Contains the functions shown to the user.
    - `processing.py`: Contains the functions and code used for the simulation and processing tasks.
    - `visualization.py`: Contains the functions and code used for the visualization task.

## Details

### Random data: `shuffle_deck`
To generate the random decks, the `shuffle_deck` function creates a numpy ndarray with 26 zeroes and 26 ones (a zero represents a black card, and a one represents a red card). Using numpy's random number generator object, it sets a seed if the user has specified it, and then shuffles the deck. This creates an array, which is then converted to a string.  The `play_n_games` function will run this function for every iteration of n, before calculating the results.

### Scoring of data: `score_deck`, `calculate_winner`, `play_one_deck`
The `score_deck` function takes in the 52 character string produced by `shuffle_deck` along with the 3 pattern sequences from both players. It calculates the number of cards and tricks won by each player for a specific deck. It does this by iterating through the deck, noting when each sequence appears, and updating the number of cards or tricks that player has from that game. The `calculate_winner` function takes in the outputs from `score_deck` and calculates the winner for both the cards and tricks variations, counting for ties in both variations. Finally, `play_one_deck` runs both the `score_deck` and `calculate_winner` functions for all possible combinations and stores the results for the play in 4 numpy arrays, representing results for each combination: one for the cards winner, one for whether a tie occurred for cards, one for the tricks winner, and one for whether a tie occurred for tricks. In this scenario, the player "me" is player two, and wins are labeled as a 1. If the other player wins, the same space is labeled as a 0. This raw data can be found under the "data" directory.

### Calculating probabilities: `sum_games`
To calculate the win/tie probabilities, `sum_games` iterates through all the files in a given directory and sums the raw results. It then returns the average of a given directory, along with an integer representing the number of games played/stored in the directory.

### Putting it all together: `play_n_games`
To run the entire process, the `play_n_games` will generate random data, score the plays, and calculate the win and tie probabilities for all simulations. Data is generated independently for each of the 56 possible matchups, rather than assuming symmetry. It writes the final JSON results file storing an 8x8 list of lists for the cards, tricks, card_ties, and trick_ties probabilities. This file is then stored in the "results" directory. This file also returns the results formatted for the visualization task.

### Visualization: `create_heatmap`, `make_heatmap_package`, `save_figures`
To visualize the results, the `create_heatmap` and `make_heatmap_package` functions create the final heatmaps. `create_heatmap` will create the heatmap for a single variation (cards or tricks), while `make_heatmap_package` creates heatmaps for both variations. These functions then save the heatmaps as PNG and HTML files (using `save_figures`) in the "figures" directory. To create a single heatmap using `create_heatmap`, the `get_data` function loads in the final simulation results from the JSON file. Next, we reformat the data (either cards/card_ties or tricks/trick_ties) using `format_data`. The labels for the heatmap are generated using `make_annots`. Finally, we input the data and labels into `make_heatmap` and return the visualization.

### Final Output
This program produces two heatmaps to compare the win probabilities of the two variations of Penney's game. These visualizations can be found in the "figures" directory. Each heatmap cell represents the win probability of each pair of 3-pattern sequences used by the player and their opponent. The darker the cell, the more likely it is for the player to win and vice versa. Since both players cannot have the same pattern, the diagonal (where the players have identical patterns) is grayed out. By putting the cards and tricks heatmaps next to one another, we can easily compare the final win results. There is some symmetry about the visualization, but we decided to include the entirety of the calculated results to ensure no assumptions were made about the data.
