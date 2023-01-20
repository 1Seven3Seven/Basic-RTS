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

Trees are most common on clear terrain.
Trees are a little less common on hilly terrain.
Trees are uncommon on mountain terrain.
Trees never appear on snow or river.

Stone deposits are uncommon on clear terrain.
Stone deposits are more common on hilly terrain.
Stone deposits are much more likely on mountains.
Stone never appears on snow or river.

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
from math import sqrt

from AStar import Node, NodeGenerator
from perlin_noise import PerlinNoise


class GridSquareTerrain(Enum):
    """
The terrain that each grid square can have.
    """

    CLEAR = auto()

    HILL = auto()
    MOUNTAIN = auto()
    SNOW = auto()
    RIVER = auto()


TerrainToWeight = {
    GridSquareTerrain.CLEAR: 1,

    GridSquareTerrain.HILL: 6,
    GridSquareTerrain.MOUNTAIN: 20,
    GridSquareTerrain.SNOW: 30,

    GridSquareTerrain.RIVER: 10
}

TerrainToValue = {
    GridSquareTerrain.CLEAR: 0,

    GridSquareTerrain.HILL: 6,
    GridSquareTerrain.MOUNTAIN: 20,
    GridSquareTerrain.SNOW: 30,

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

        self.terrain_seed: int | None = None
        self.terrain_octaves: list[int] | None = None
        self.terrain_noise_map: list[list[float]] | None = None
        self.terrain_heights: dict[GridSquareTerrain, float] | None = None
        self.terrain_generated: bool = False

        self.player_base_locations: list[tuple[int, int]] = []

        self.natural_structure_seed: int | None = None
        self.natural_structure_octaves: list[int] | None = None
        self.tree_noise_map: list[list[float]] | None = None

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

    # region - Environment setup functions

    def re_generate_terrain(self):
        """
Re-generated the terrain based off of the saved information after generate terrain is called.
Should reset everything to the starting state.
        """

        assert self.terrain_generated, "generate terrain must be called first"

        # Setup
        all_noise = [PerlinNoise(octaves=octave, seed=self.terrain_seed) for octave in self.terrain_octaves]
        center_x, center_y = self.grid.x_size / 2, self.grid.y_size / 2
        largest = sqrt(center_x * center_x + center_y * center_y)

        # Generate the picture
        self.terrain_noise_map = []
        for y in range(self.grid.y_size):
            row = []

            for x in range(self.grid.x_size):
                value = largest - sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                value /= largest

                for i, noise in enumerate(all_noise, start=2):
                    value += noise([x / self.grid.x_size, y / self.grid.y_size]) / i

                row.append(value)

            self.terrain_noise_map.append(row)

        # Normalise the picture to between 0 and 1
        abs_min_value = abs(min([min(row) for row in self.terrain_noise_map]))
        self.terrain_noise_map = [[pixel + abs_min_value for pixel in row] for row in self.terrain_noise_map]
        max_value = abs(max([max(row) for row in self.terrain_noise_map]))
        self.terrain_noise_map = [[pixel / max_value for pixel in row] for row in self.terrain_noise_map]

        # Set the terrain depending on the picture values
        for y in range(self.grid.y_size):
            for x in range(self.grid.x_size):
                value = self.terrain_noise_map[y][x]

                terrain_type = GridSquareTerrain.CLEAR
                if value > self.terrain_heights[GridSquareTerrain.SNOW]:
                    terrain_type = GridSquareTerrain.SNOW
                elif value > self.terrain_heights[GridSquareTerrain.MOUNTAIN]:
                    terrain_type = GridSquareTerrain.MOUNTAIN
                elif value > self.terrain_heights[GridSquareTerrain.HILL]:
                    terrain_type = GridSquareTerrain.HILL

                self.grid[x, y].terrain = terrain_type

    def generate_terrain(self,
                         seed: int = 0,
                         octaves: list[int] | None = None,
                         snow_height: float = 0.9,
                         mountain_height: float = 0.75,
                         hill_height: float = 0.5):
        """
Generates the terrain for the grid.
Saves the information used to generate the information.
        :param seed: The seed to use for the perlin noise generator.
        :param octaves: A list of the octaves to use when generating terrain, should be in increasing order.
        :param snow_height: The minimum value for snow, > mountain height and <= 1.
        :param mountain_height: The minimum value for mountains, > hill height and < snow height.
        :param hill_height: The minimum value for hills, >= 0 and < mountain height.
        """

        assert snow_height <= 1, "Snow height must be <= 1"
        assert snow_height > mountain_height, "Snow height must be larger than mountain height"
        assert mountain_height > hill_height, "Mountain height must be larger than hill height"
        assert hill_height >= 0, "Hill height must be >= 0"

        # Save all the information
        self.terrain_seed = seed

        self.terrain_octaves = [3, 6, 12, 24] if octaves is None else octaves

        self.terrain_heights[GridSquareTerrain.SNOW] = snow_height
        self.terrain_heights[GridSquareTerrain.MOUNTAIN] = mountain_height
        self.terrain_heights[GridSquareTerrain.HILL] = hill_height

        # Terrain has now been generated
        self.terrain_generated = True

        # Generate the terrain
        self.re_generate_terrain()

    def set_player_base(self, x_location: int, y_location: int):
        """
Sets the nodes at the given location to a player base.
Player bases are a 2x2 sized structure and the location is the top left.
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

    def re_generate_natural_structures(self):
        pass

    def generate_natural_structures(self,
                                    seed: int = 0,
                                    octaves: list[int] | None = None):
        """
Places the natural structures in the grid.
NOTE: Generate terrain should be run first.
NOTE: Player bases should be set first.
        """

        # Place trees randomly then check if the required number is near the player bases.
        # Do the same with rocks, although with much less chance

        pass

    # endregion - Environment setup functions
