# Connect4AI
An implementation of Minimax, Alpha-Beta and Monte Carlo Tree Search to play Connect 4

## Requirement
You can install all the libraries needed using pip:

```bash
pip install -r requirements.txt
```
## Usage
To play the game, run the `src/graphics.py` file.

You can choose to play against another human or against one of the AI.

```bash
python -m src.graphics
```

## Project Structure

Here is the layout of this project:

<pre>
Connect4AI
│
├── src
│   ├── AIs
│   │   ├── alphaBeta.py
│   │   ├── mcts.py
│   │   ├── Q_learning.py
│   │   └── minmax.py
│   │
│   ├── Statistics
│   │   ├── backup.py
│   │   ├── scoring_selection.py
│   │   ├── statistics.py
│   │   └── statistics_alphabeta.py
│   │
│   ├── score.py
│   ├── Game.py
│   ├── Player.py
│   └── graphics.py
│
└── tests
    └── test_score_calculation.py
</pre>

## Q Learning
To train the Q Learning IA with 1 000 000 games, run the `src/AIs/Q_learning.py` file.

```bash
python -m src.AIs.Q_learning
```

## Testing
To run the tests for Connect4AI, navigate to the project directory and run the following commands:

```bash
python -m tests.test_score_calculation
```

## License
This project is licensed under the terms of the GPL-3.0 license.
