# Penney's Game Project

## Description
This project simulates Penney’s Game playing and scoring with both cards and tricks to determine the optimal starting sequences. When scoring the game with cards, there is a strategic advantage based on how sequences are chosen, despite the appearance of fairness. First, let your opponent choose their sequence and then you choose a sequence that is statistically more likely to appear before your opponent's sequence. For example, if the pattern of your opponent’s sequence is 123, your sequence should be ~212 to increase your chances of a win. This strategy for winning Penney’s game prompted the main research questions explored in this analysis, which include:
How does Penney’s game’s winner probability differ when we score based on trick counts rather than card counts? Why?
Does the winner probability change when ties are accounted for in each play?

A full explanation of the game and win strategy can be found in the following links:

https://en.wikipedia.org/wiki/Penney%27s_game

https://www.datascienceassn.org/sites/default/files/Humble-Nishiyama%20Randomness%20Game%20-%20A%20New%20Variation%20on%20Penney%27s%20Coin%20Game.pdf


## Getting Started

An example for how to run this program can be found in final_run.ipynb.

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
- `src/`: Folder containing backend python script code for penney project.
    - `main.py`: Contains the functions shown to the user.
    - `processing.py`: Contains the functions and code used for the processing task.
    - `visualization.py`: Contains the functions and code used for the visualization task.

## Details

### Random data: `shuffle_deck`
To generate the random decks, the `shuffle_deck` function creates a numpy ndarray with 26 zeroes and 26 ones (a zero represents a black card, and a one represents a red card). Using numpy's random number generator object, it sets a seed if the user has specified it, and then shuffles the deck. This creates an array, which is then converted to a string.  The `play_n_games` function will run this function for every iteration of n, before calculating the results.

### Scoring of data: `score_deck`, `calculate_winner`, `play_one_deck`

The `score_deck` function takes in the 52 character array produced by `shuffle_deck` along with the 3 pattern sequences from both players. It calcuates the number cards and tricks won by each player for a specific deck. The `calculate_winner` function takes in the outputs from `score_deck` and calculates the winner for both the cards and tricks variations, along with counting for ties in both variations. Finally, `play_one_deck` runs both the `score_deck` and `calculate_winner` functions and stores the results for the play in 4 numpy files, the winner of cards, the winner of tricks, if there was a tie in cards, and if there was a tie in tricks. This raw data can be found under the "data" folder.

### Calculating probabilities: `sum_games`

To calculate the win/tie probabilities, `sum_games` iterates through all the files in each folder stored under "data" and sums the raw results. It then returns the summations (or the average) of a given folder "cards", "tricks", "card_ties", or "trick_ties" along with an integer representing the number of games played/stored in the file.

### Running main program: 

To run the entire process, the `play_n_games` was created 

### Presentation of results

