"""Imports"""
from collections import deque
import numpy as np
from pygame.math import Vector2

from src.helpers import out_of_bounds
from src.config import PLAYER_START_POS, ENEMY_START_POS, GRID_SIZE


class Food:
    """Food that snake can eat and then increase in size"""

    is_spawned = False
    pos = Vector2(0, 0)

    def __init__(self, grid, screen):
        self.grid = grid
        self.screen = screen
        self.try_to_spawn()

    def try_to_spawn(self):
        """If food is not already spawned, spawn it on randomly (create and display it on the screen)"""
        while not Food.is_spawned:
            x = np.random.randint(0, GRID_SIZE)
            y = np.random.randint(0, GRID_SIZE)
            if self.grid.get_tile(Vector2(x, y)).walkable:
                Food.is_spawned = True
                Food.pos = Vector2(x, y)
                self.grid.change_tile("food", Food.pos, self.screen)

    def get_pos(self):
        """Returns position of the food"""
        return self.pos


class Snake:
    """Base snake class"""

    def __init__(self, grid, screen):
        self.direction = Vector2(1, 0)
        self.last_direction = self.direction
        self.grid = grid
        self.screen = screen
        self.body = deque()

    def get_snake_len(self):
        """Returns number of tiles the snake is made of"""
        return len(self.body)

    def change_direction(self, new_direction):
        """Tries to change snake direction"""
        # direction can't be change by 180 degrees
        if new_direction == -self.last_direction:
            return
        self.direction = new_direction


class PlayerSnake(Snake):
    """Snake controlled by the player"""

    def __init__(self, grid, screen):
        Snake.__init__(self, grid, screen)
        self.body.append(PLAYER_START_POS)
        self.grid.change_tile("player", PLAYER_START_POS, self.screen)

    def move(self):
        """
        Moves the snake in a direction that the snake currently has.
        Returns true if the move is ok, and false if snake died during that move.
        """
        # crete new snake piece in the place he moved to
        new_snake_piece = self.body[-1] + self.direction
        self.last_direction = self.direction
        self.body.append(new_snake_piece)

        # snake moved out of bounds
        if out_of_bounds(new_snake_piece):
            return False

        tile_under_head = self.grid.get_tile(new_snake_piece)

        # check for collision
        if not tile_under_head.walkable:
            return False

        # check for food
        has_eaten = False
        if tile_under_head.type == "food":
            has_eaten = True
            Food.is_spawned = False

        #change in grid
        self.grid.change_tile("player", new_snake_piece, self.screen)
        if not has_eaten:
            to_delete = self.body.popleft()
            self.grid.change_tile("nothing", to_delete, self.screen)

        return True  # move succesful


class EnemySnake(Snake):
    """Snake controlled by the computer."""

    def __init__(self, grid, screen):
        Snake.__init__(self, grid, screen)
        self.direction = Vector2(-1, 0)
        self.body.append(ENEMY_START_POS)
        self.grid.change_tile("enemy", ENEMY_START_POS, self.screen)

    def move(self):
        """Move enemy snake in direction of the shortest path to the food."""
        head = self.body[-1]

        def dir_to_neigbour(neighbour):
            """Returns a direction to a given neighbouring Tile"""
            if neighbour == head + Vector2(1, 0):
                return Vector2(1, 0)
            if neighbour == head + Vector2(-1, 0):
                return Vector2(-1, 0)
            if neighbour == head + Vector2(0, 1):
                return Vector2(0, 1)
            if neighbour == head + Vector2(0, -1):
                return Vector2(0, -1)
            raise Exception("Given point isn't a neighbour")

        # try to find shortest path to the food
        path = self.grid.shortest_path(head, Food.pos)
        if path:
            self.direction = dir_to_neigbour(path[1])
        # Create new snake piece in the direction of movement
        new_snake_piece = head + self.direction
        self.last_direction = self.direction
        self.body.append(new_snake_piece)

        # snake moved out of bounds
        if out_of_bounds(new_snake_piece):
            return False

        tile_under_head = self.grid.get_tile(new_snake_piece)

        # check for collision
        if not tile_under_head.walkable:
            return False

        # check for food
        has_eaten = False
        if tile_under_head.type == "food":
            has_eaten = True
            Food.is_spawned = False

        #change in grid
        self.grid.change_tile("enemy", new_snake_piece, self.screen)

        # remove last snake piece if no food was consumed
        if not has_eaten:
            to_delete = self.body.popleft()
            self.grid.change_tile("nothing", to_delete, self.screen)

        return True  # move succesful
