"""
The environment is grid based.

Environment objects
    Two resources will spawn:
        Trees
        Stone Despots

    The environment can be modified by placing structures:
        Wood walls
        Stone walls

        Wood spawner
        Stone spawner


Environment weights based on objects:
    Clear node:         1

    Tree node:          2
    Stone node:         -

    Wood wall node:     5
    Stone wall node:    10

    Wood spawner node:  -
    Stone spawner node: -

When a node is changed the weights of all connections are changed.
The weight for a connection between two nodes is the largest weight of the two according to the above info.
"""
from enum import Enum, auto

import AStar


class GridSquareTypes(Enum):
    """
The things that each grid square can be.
    """
    CLEAR = auto()

    TREE = auto()
    STONE = auto()

    WOOD_WALL = auto()
    STONE_WALL = auto()

    WOOD_SPAWNER = auto()
    STONE_SPAWNER = auto()


class GridSquare(AStar.Node):
    def __init__(self, x_position: int, y_position: int):
        super().__init__(x_position, y_position)

        # The current type of the grid square
        self.type: GridSquareTypes = GridSquareTypes.CLEAR


class Environment:
    def __init__(self):
        pass
