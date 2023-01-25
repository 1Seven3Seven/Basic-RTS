from AStar import NodeGenerator

from .EnvironmentData import GridSquareStructures
from .GridSquare import GridSquare


class Environment:
    def __init__(self, width: int, height: int):
        self.grid: NodeGenerator.Grid = NodeGenerator.Grid(width, height, node_class=GridSquare)

        self.player_base_locations: list[tuple[int, int]] = []

    # region - __Dunders__

    def __getitem__(self, coords: tuple[int, int]) -> GridSquare:
        """
Returns the GridSquare at the corresponding coordinates.
        :param coords: The coordinates of the grid square to lookup.
        :return: The grid square at the coordinates
        """

        return self.grid.__getitem__(coords)

    # endregion - __Dunders__

    # region - Properties

    @property
    def x_size(self):
        return self.grid.x_size

    @property
    def y_size(self):
        return self.grid.y_size

    # endregion - Properties

    def set_player_base(self, x_location: int, y_location: int):
        """
Sets the nodes at the given location to a player base.
Player bases are a 2x2 sized structure and the location is the top left.
Please don't set bases where there are already bases, this is undefined behaviour.
        :param x_location: The x location of the top left of the player base.
        :param y_location: The y location of the top left of the player base.
        """

        assert x_location >= 0, "x location must be larger than 0"
        assert x_location < self.grid.x_size, f"x location must be less than the x size {self.grid.x_size}"
        assert y_location >= 0, "y location must be larger than 0"
        assert y_location < self.grid.y_size, f"y location must be less than the y size {self.grid.y_size}"

        self.player_base_locations.append((x_location, y_location))

        for y in range(y_location, y_location + 2):
            for x in range(x_location, x_location + 2):
                self.grid[x, y].structure = GridSquareStructures.PLAYER_BASE

    def update_node_connections(self):
        """
Updates the weights on all node connections based off of the terrain and structure values.
        """

        ...
