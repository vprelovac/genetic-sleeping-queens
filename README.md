# Genetic Sleeping Queens

This is an exploration of AI strategies for card game "Sleeping Queens". Beside the heuristic strategy, I also wanted to experiment with using genetic algorithms. 



## Usage

To play vs an AI.

```
python main.py -p1 "Genetic AI"
```

Options are "Easy AI" , "Hard AI", "Genetic AI" (best).

Let two AIs play against each other:

```
python main.py -p1 "Genetic AI" -p2 "Hard AI"  -num 20000
```

To run a genetic algorithm:

```
 python main.py -ga
```

Tune fitness, parent selection crossover and mutation in genetic_algorithm.py.

Copy the best strategy to main.py. This is the optimal strategy the algorithm surfaced:

```
best_strategy = {
        'put_queen_to_sleep_weight': 7, 'steal_queen_weight': 6, 'awaken_queen_weight': 5, 'discard_equation_weight': 4,
        'play_jester_weight': 3,  'discard_pair_weight': 2, 'discard_single_weight': 1
    }
```

This means that the most powerful card in Sleeping Queens is... the Sleeping Potion! And that you should play Jester only as a last resort really.
