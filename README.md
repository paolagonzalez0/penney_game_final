# Penney's Game Project

## Description
This project simulates Penney’s Game playing and scoring with both cards and tricks to determine the optimal starting sequences. When scoring the game with cards, there is a strategic advantage based on how sequences are chosen, despite the appearance of fairness. First, let your opponent choose their sequence and then you choose a sequence that is statistically more likely to appear before your opponent's sequence. For example, if the pattern of your opponent’s sequence is 123, your sequence should be ~212 to increase your chances of a win. This strategy for winning Penney’s game prompted the main research questions explored in this analysis, which include:
How does Penney’s game’s winner probability differ when we score based on trick counts rather than card counts? Why?
Does the winner probability change when ties are accounted for in each play?

A full explanation of the game and win strategy can be found in the following links:
https://en.wikipedia.org/wiki/Penney%27s_game 
https://www.datascienceassn.org/sites/default/files/Humble-Nishiyama%20Randomness%20Game%20-%20A%20New%20Variation%20on%20Penney%27s%20Coin%20Game.pdf


## Getting Started
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

## Folders and files included
- `data/`: The data generated (currently about 1 million entries per folder).
    - `cards`, `card_ties`, `tricks`, `trick_ties`: folders within the `data` folder, each containing .npy files that represent different games. `cards` stores results for cards, `card_ties` stores ties for cards, `tricks` stores results for tricks, and `tricks_ties` stores ties for tricks.
- `results/`: the .json file storing the current results
- `figures/`: Stores the results for the heatmaps.
- `main.py`: Contains the functions shown to the user

## Details

### Random data: `shuffle_deck`

### Scoring of data: `score_deck`

### Presentation of results