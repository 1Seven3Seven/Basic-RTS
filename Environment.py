"""
The environment is grid based.

Environment objects:
    Terrain:
        Hills
        Mountains
        Rivers

    The resources that will spawn:
        Trees
        Stone Despots
        
    Player bases (unchangeable):
        Player 1 base
        Player 2 base
        ...

    The environment can be modified by placing structures:
        Wood walls
        Stone walls

        Wood spawner
        Stone spawner


Node weights based on objects:
    Train:
        Clear node:             1
        
        Hill node:              6
        Mountain node:          20
        River node:             10

    Structures:
        Tree node:              2
        Stone node:             2
        
        Player x base node:     1
    
        Wood wall node:         8
        Stone wall node:        12
    
        Wood spawner node:      1
        Stone spawner node:     1
        
Stone deposits are much more likely on mountains and hills.
Trees and stone deposits are impossible on river.
    
The player bases are a 2x2 object, each one can spawn one worker.

When a node is changed the weights of all connections are changed.
The weight for a connection between two nodes is the largest weight of the two according to the above info.
    By that I mean the candidate weights are the sum of the terrain and structure weight.

When entities move from node to node their speed depends on the weight between those nodes.

Around a Player base, there should be a minimum number of trees and stone deposits.
There will be a minimum range for stone deposits.
e.g.
    A minimum of 100 trees will spawn in a 30 node radius.
    A minimum of 3 stone deposits will spawn between 20 and 45 nodes away.
"""

from enum import Enum, auto

from AStar import Node, NodeGenerator


class GridSquareTerrain(Enum):
    """
The terrain that each grid square can have.
    """
    
    CLEAR = auto()
    
    HILL = auto()
    MOUNTAIN = auto()
    RIVER = auto()
    

TerrainToWeight = {
    GridSquareTerrain.CLEAR: 1,
    
    GridSquareTerrain.HILL: 6,
    GridSquareTerrain.MOUNTAIN: 20,
    GridSquareTerrain.RIVER: 10
}


class GridSquareStructures(Enum):
    """
The structures that each grid can have.
    """

    NONE = auto()

    TREE = auto()
    STONE = auto()
    
    PLAYER_BASE = auto()

    WOOD_WALL = auto()
    STONE_WALL = auto()

    WOOD_SPAWNER = auto()
    STONE_SPAWNER = auto()


StructureToWeight = {
    GridSquareStructures.NONE: 1,

    GridSquareStructures.TREE: 3,
    GridSquareStructures.STONE: 3,
    
    GridSquareStructures.PLAYER_BASE: 1,

    GridSquareStructures.WOOD_WALL: 7,
    GridSquareStructures.STONE_WALL: 12,

    GridSquareStructures.WOOD_SPAWNER: 1,
    GridSquareStructures.STONE_SPAWNER: 1
}


class GridSquare(Node):
    """
A node that contains information about the state of the grid square.
    """

    def __init__(self, x_position: int, y_position: int):
        super().__init__(x_position, y_position)
        
        # The terrain of the grid square
        self.terrain: GridSquareTerrain = GridSquareTerrain.CLEAR

        # The current structure of the grid square
        self.structure: GridSquareStructures = GridSquareStructures.NONE


class Environment:
    def __init__(self, width: int, height: int):
        self.grid: NodeGenerator.Grid = NodeGenerator.Grid(width, height, node_class=GridSquare)

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

