"Imports"
from src.config import GRID_SIZE


def out_of_bounds(vector):
    """Checks if point is outside of playing grid"""
    if vector.x >= GRID_SIZE or vector.y >= GRID_SIZE or vector.x < 0 or vector.y < 0:
        return True
    return False


def distance(a, b):
    """Returns manhatten distance between two vectors"""
    return abs(a.x - b.x) + abs(a.y - b.y)
