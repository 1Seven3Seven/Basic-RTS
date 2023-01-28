from AStar import Node

from .EnvironmentData import GridSquareTerrain, GridSquareStructures


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
