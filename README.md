# Snake against AI

This was my semestral project for Python programming course. I recycled my highschool idea of 2 player snake game and rewritten it in python.

The game is based on a classical game of snake, however there are two snakes at once. One is controlled by the player, the other by AI. The goal is to outlast the other snake.

### Controlls
After running the game, start by pressing spacebar. The snake is controlled by arrows (the player is a blue snake int he top left corner). You can end the game with the escape key.

### Game rules
Snakes move in a regular time intervals in a chosen direction. If the snake collides (either with himself, oponent or the wall), he loses. Move intervals of the two snakes are offset, so that collisions are allways conclusive. If snake pick ups food that randomly spawns on the playing field, he grows longer. If one snake is greatly longer than the other, he loses.

### Requirements
For the program to work, you need to install cuple of packages. Everything is in the virtual environment *environment.yml*. I used [miniconda]([url](https://docs.anaconda.com/free/miniconda/)) for managing the environment - with miniconda you can activate the environment by running ```conda activate pyt_sem```. When installing for the first time you might need to update the environment by running ```conda env update``` after activating the environment.

### Run the game
After activation of the virtual environment you can run the game from within the *sem* directory by running ```python3 snake_game```. 

### Tests
There is also a couple of tests included. You can run all of them by running the ```pytest``` command in the *sem* directory.
