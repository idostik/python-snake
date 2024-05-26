"""imports"""
import pytest
from pygame.math import Vector2
import warnings

from src import grid, helpers
from src.config import GRID_SIZE


@pytest.mark.parametrize(
    ['a', 'b', 'dist'],
    [(Vector2(0, 0), Vector2(4, 10), 14),
     (Vector2(3, 4), Vector2(3, 6), 2),
     (Vector2(-1, 5), Vector2(2, 11), 9),
     (Vector2(4, 10), Vector2(4, 10), 0),
     (Vector2(5, -2), Vector2(14, 21), 32)]
)
def test_distance(a, b, dist):
    """Test distance calculation"""
    res = helpers.distance(a, b)
    assert res == dist


@pytest.mark.parametrize(
    ["pos", "is_out"],
    [
        (Vector2(0, 0), False),
        (Vector2(GRID_SIZE, 0), True),
        (Vector2(5, GRID_SIZE), True),
        (Vector2(GRID_SIZE - 1, 0), False)
    ]
)
def test_out_of_bounds(pos, is_out):
    """Test out_of_bounds function"""
    res = helpers.out_of_bounds(pos)
    assert is_out == res


@pytest.fixture
def obstacle_grid():
    """Creates grid for testing"""
    if GRID_SIZE < 11:
        return
    g = grid.Grid()

    """
    Add obstacles like this:

      0   1   2   3   4   5   6   7   8   9   10
    +---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   | X | 0
    +---+---+---+---+---+---+---+---+---+---+---+
    | X | X | X |   |   |   |   |   |   |   | X | 1
    +---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   | X | X | X |   |   |   | X | 2
    +---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   | X |   |   |   |   | X | 3
    +---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   | X |   |   |   |   | X | 4
    +---+---+---+---+---+---+---+---+---+---+---+
    |   | X | X |   |   |   |   |   | X | X | X | 5
    +---+---+---+---+---+---+---+---+---+---+---+
    |   | X |   |   |   | X |   |   |   |   | X | 6
    +---+---+---+---+---+---+---+---+---+---+---+
    |   | X |   |   |   | X | X |   |   |   | X | 7
    +---+---+---+---+---+---+---+---+---+---+---+
    |   | X |   |   |   |   |   | X | X | X | X | 8
    +---+---+---+---+---+---+---+---+---+---+---+
    |   | X |   |   |   |   |   | X |   |   | X | 9
    +---+---+---+---+---+---+---+---+---+---+---+
    | X | X | X | X | X | X | X | X | X | X | X | 10
    +---+---+---+---+---+---+---+---+---+---+---+
      0   1   2   3   4   5   6   7   8   9   10
    """
    # position of obstacles from above
    obstacles = [
        Vector2(0, 1), Vector2(1, 1), Vector2(1, 2),
        Vector2(4, 2), Vector2(5, 2), Vector2(6, 2),
        Vector2(5, 3), Vector2(5, 4), Vector2(1, 5),
        Vector2(2, 5), Vector2(1, 6), Vector2(1, 7),
        Vector2(1, 8), Vector2(1, 9), Vector2(8, 5),
        Vector2(9, 5), Vector2(5, 6), Vector2(5, 7),
        Vector2(6, 7), Vector2(7, 8), Vector2(8, 8),
        Vector2(9, 8), Vector2(7, 9), Vector2(10, 0),
        Vector2(10, 1), Vector2(10, 2), Vector2(10, 3),
        Vector2(10, 4), Vector2(10, 4), Vector2(10, 5),
        Vector2(10, 6), Vector2(10, 7), Vector2(10, 8),
        Vector2(10, 9), Vector2(10, 10), Vector2(9, 10),
        Vector2(8, 10), Vector2(7, 10), Vector2(6, 10),
        Vector2(5, 10), Vector2(4, 10), Vector2(3, 10),
        Vector2(2, 10), Vector2(1, 10), Vector2(0, 10),
    ]

    for obst in obstacles:
        g.change_tile("enemy", obst, None, False)

    return g

@pytest.mark.parametrize(
    ['start', 'end', 'length'],
    [
        (Vector2(0, 0), Vector2(0, 2), 9),
        (Vector2(0, 0), Vector2(6, 3), 12),
        (Vector2(0, 0), Vector2(9, 9), None),
        (Vector2(0, 0), Vector2(1, 0), 2),
        (Vector2(9, 9), Vector2(6, 9), None),
        (Vector2(0, 0), Vector2(9, 6), 16),
        (Vector2(0, 9), Vector2(2, 9), 15),
        (Vector2(2, 9), Vector2(0, 9), 15),
        (Vector2(6, 8), Vector2(7, 7), 11),
        (Vector2(7, 7), Vector2(6, 8), 11),
        (Vector2(5, 5), Vector2(5, 5), 1),
        (Vector2(0, 0), Vector2(0, 1), None),
    ]
)
def test_shortest_path(obstacle_grid, start, end, length):
    """Test pathfinding"""
    if GRID_SIZE < 11:
        warnings.warn(UserWarning(
            "\nPlease set grid size >= 11 in order to test correctly\n"))
        return
    path = obstacle_grid.shortest_path(start, end)
    if not path:
        assert not length
    else:
        assert len(path) == length
        assert path[0] == start
        assert path[-1] == end


@pytest.mark.parametrize(
    ['pos', "neighbours"],
    [
        (Vector2(0, 0), [Vector2(1, 0)]),
        (Vector2(8, 1), [Vector2(8, 0), Vector2(8, 2),
                         Vector2(7, 1), Vector2(9, 1)]),
        (Vector2(0, 6), [Vector2(0, 5), Vector2(0, 7)]),
        (Vector2(6, 8), [Vector2(6, 9), Vector2(5, 8)]),
        (Vector2(3, 5), [Vector2(3, 4), Vector2(3, 6), Vector2(4, 5)]),
        (Vector2(2, 6), [Vector2(2, 7), Vector2(3, 6)]),
        (Vector2(9, 9), [Vector2(8, 9)]),
        (Vector2(8, 9), [Vector2(9, 9)]),
        (Vector2(7, 8), [Vector2(7, 7), Vector2(6, 8)]),
    ]
)
def test_get_walkable_neigbhours(obstacle_grid, pos, neighbours):
    """Test if function returns correct neighbours"""
    if GRID_SIZE < 11:
        warnings.warn(UserWarning(
            "\nPlease set grid size >= 11 in order to test correctly\n"))
        return
    res = obstacle_grid.get_walkable_neighbours(pos)
    assert len(res) == len(neighbours)
    for n in res:
        assert n in neighbours