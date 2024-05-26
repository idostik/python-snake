"""Imports"""
from queue import PriorityQueue
import numpy as np
import pygame
from pygame.math import Vector2

from src.config import TILE_SIZE, BACKGROUND_COLOR, ENEMY_COLOR, PLAYER_COLOR, FOOD_COLOR, GRID_SIZE
from src.helpers import distance, out_of_bounds


class TILE:
    """Class representing single tile on the grid"""

    def __init__(self, grid_x, grid_y, screen_pos, tile_type):
        self.grid_x = grid_x
        self.grid_y = grid_y
        # position in pixels
        self.screen_pos = screen_pos
        self.change_type(tile_type)

    def draw(self, screen):
        """Display this tile on the screen"""
        rect = pygame.Rect(self.screen_pos.x, self.screen_pos.y,
                           TILE_SIZE - 2, TILE_SIZE - 2)
        color = BACKGROUND_COLOR
        if self.type == "enemy":
            color = ENEMY_COLOR
        elif self.type == 'player':
            color = PLAYER_COLOR
        elif self. type == 'food':
            color = FOOD_COLOR

        pygame.draw.rect(screen, color, rect)

    def change_type(self, new_type):
        """Change the type of this tile"""
        self.type = new_type
        if new_type in ('player', 'enemy'):
            self.walkable = False
        else:
            self.walkable = True


class Grid:
    """Class representing the whole playing bord. Divided into Tiles"""

    # Creates numpy 2D array and fills it with tiles
    def __init__(self):
        self.grid = np.empty((GRID_SIZE, GRID_SIZE), dtype=object)
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                self.grid[y, x] = TILE(grid_x=x, grid_y=y, screen_pos=Vector2(
                    x * TILE_SIZE, y * TILE_SIZE), tile_type='nothing')

    def draw_all(self, screen):
        """Displays whole grid on the screen"""
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                self.grid[y, x].draw(screen)

    def change_tile(self, new_tile_type, pos, screen, draw=True):
        """Changes tile on a given position and displays it on the screen"""
        self.grid[int(pos.y), int(pos.x)].change_type(new_tile_type)
        if draw:
            self.grid[int(pos.y), int(pos.x)].draw(screen)

    def get_tile(self, pos):
        """Returns tile at given position"""
        return self.grid[int(pos.y), int(pos.x)]

    def get_walkable_neighbours(self, pos):
        """Returns list of all walkable neigbours (neigbouring tiles in four directions)"""
        neigbhours = []
        for n in [pos + Vector2(0, -1), pos + Vector2(0, 1), pos + Vector2(1, 0), pos + Vector2(-1, 0)]:
            if not out_of_bounds(n) and self.get_tile(n).walkable:
                neigbhours.append(n)
        return neigbhours

    def shortest_path(self, start, end):
        """
        Returns list of positions representing the shortest path between two points.
        The pathfinding is done using A* algorithm.
        """
        def reconstruct_path(predecessor_list, end):
            """Reconstructs path from predecessor list"""
            current = end
            path = []
            while current:
                path.append(Vector2(current))
                current = predecessor_list[current]
            path.reverse()
            return path

        start_tuple = (start.x, start.y)
        end_tuple = (end.x, end.y)
        # structure storing f_costs (manhatten distances from start to end)
        open_q = PriorityQueue()
        predecessors = {}
        # dict storing distances from the start
        g_cost_at = {}
        # the distance here doesn't matter, it will be the first tile examined anyways
        open_q.put((0, start_tuple))
        # predecessor of first tile doesn't exist
        predecessors[start_tuple] = None
        g_cost_at[start_tuple] = 0

        while not open_q.empty():
            # coordinates of tile with lowes f_cost
            current = open_q.get()[1]

            if current == end_tuple:
                return reconstruct_path(predecessors, end_tuple)

            for n in self.get_walkable_neighbours(Vector2(current)):
                # distance to a neigbour is allways 1
                new_g_cost = g_cost_at[current] + 1
                # if neighbour was not yet discovered or if we found a shorter path
                if (n.x, n.y) not in g_cost_at or new_g_cost < g_cost_at[(n.x, n.y)]:
                    # calulate new distances and add to queue, assign predecessor
                    g_cost_at[(n.x, n.y)] = new_g_cost
                    f_cost = new_g_cost + distance(n, end)
                    open_q.put((f_cost, (n.x, n.y)))
                    predecessors[(n.x, n.y)] = current

        # in this case path does not exist
        return None
