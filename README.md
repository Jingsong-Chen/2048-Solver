Assignment 2: 2048
=========

Your task is to implement a game AI for the 2048 game based on simple expectimax search. The base game engine is using the code from [here](https://gist.github.com/lewisjdeane/752eeba4635b479f8bb2). 

Due date
-----
Feb-3 11:00pm Pacific Time. 

Grading
-----

1. Documentation (1 points)

Comment your code generously. 

2. Functionality (13 points)

Model the AI player as a max player, and the computer as a chance player (picking a random open spot and place a 2-tile). So you need to implement the expectimax algorithm to compute decisions for the AI player. 

You can play the game manually using the arrow keys. Pressing Enter will let AI play the game, and pressing Enter again will stop the AI player. In the starter code, the AI is always taking the "up" action in every step. 

You will be graded according to whether you have correctly implemented the following functions/classes. 

- Game simulator (3 points)

You can mostly copy/paste the game engine code to create a game simulator. It will be used to return the game state (and evaluate its score) after the player makes any move from any reasonable game state. 

- Construct a depth-3 game tree (4 points)

Explicitly construct a game tree from any state of the game (like the tree you see in the slides). The tree depth is required to be at least 3, that is, it can represent all the game states of a player-computer-player sequence (the player makes a move, the computer place a tile, and then the player makes another move). 

- Compute expectimax values and optimal moves (6 points)

Compute the expectimax values of all the nodes in the game tree, and return the optimal move for the player. 

Once you have implemented this AI correctly, you should see depth-3 search reaching 512 tiles and a score over 5000 quite often, as shown in the movie file. 

Extra credits (3 points)
------
While depth-3 search gives ok performance, it can apparently be improved by searching more depth. As the tree gets bigger, you may need to pay attention to the efficiency of your code -- a naive (recursive) implementation of depth-5 search may make each decision so slow that you do not want to watch it play. 

You get up to 3 extra points if you can engineer the AI to reach 2048 very often, while each step is reasonably smooth when running on a laptop. 

There are two ways to do this: you could either try optimizing the implementation of a depth-5 tree, or design a good value function to evaluate the terminal node of the depth-3 trees. You could do both as well. 

Note
------
- You can press "u" at the end of a game to undo the previous move and see the previous configuration. Check more keyboard options by reading the code. 
- Make sure to start immediately. You can see that significantly more code is required compared to Assignment 1.
