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

    Tree node:          3
    Stone node:         3

    Wood wall node:     7
    Stone wall node:    12

    Wood spawner node:  1
    Stone spawner node: 1

When a node is changed the weights of all connections are changed.
The weight for a connection between two nodes is the largest weight of the two according to the above info.

When entities move from node to node their speed depends on the weight between those nodes.
"""

from enum import Enum, auto

from AStar import Node, NodeGenerator


class GridSquareTypes(Enum):
    """
The state that each grid square can be.
    """

    CLEAR = auto()

    TREE = auto()
    STONE = auto()

    WOOD_WALL = auto()
    STONE_WALL = auto()

    WOOD_SPAWNER = auto()
    STONE_SPAWNER = auto()


TypeToWeight = {
    GridSquareTypes.CLEAR: 1,

    GridSquareTypes.TREE: 3,
    GridSquareTypes.STONE: 3,

    GridSquareTypes.WOOD_WALL: 7,
    GridSquareTypes.STONE_WALL: 12,

    GridSquareTypes.WOOD_SPAWNER: 1,
    GridSquareTypes.STONE_SPAWNER: 1
}


class GridSquare(Node):
    """
A node that contains information about the state of the grid square.
    """

    def __init__(self, x_position: int, y_position: int):
        super().__init__(x_position, y_position)

        # The current type of the grid square
        self.type: GridSquareTypes = GridSquareTypes.CLEAR


class Environment:
    def __init__(self, x_width: int, y_width: int):
        self.grid = NodeGenerator.Grid(x_width, y_width, node_class=GridSquare)

    def __getitem__(self, coords: tuple[int, int]) -> GridSquare:
        """
Returns the GridSquare at the corresponding coordinates.
        :param coords: The coordinates of the grid square to lookup.
        :return: The grid square at the coordinates
        """

        return self.grid.__getitem__(coords)

    # region - Properties

    @property
    def x_size(self):
        return self.grid.x_size

    @property
    def y_size(self):
        return self.grid.y_size

    # endregion - Properties
