import random
from math import sqrt

from perlin_noise import PerlinNoise

from . import BaseGenerator
from .. import Environment
from ..EnvironmentData import GridSquareTerrain, GridSquareStructures


class TreeGenerator(BaseGenerator):
    """
Allows for the generation of trees for the given environment.
    """

    def __init__(self,
                 environment: Environment,
                 seed: int = 1,
                 octaves: list[int] | None = None,
                 player_base_radius: int = 30,
                 player_base_tree_chance: float = 0.2,
                 player_base_min_num_trees: int = 100,
                 player_base_max_num_trees: int = 250,
                 clear_terrain_base_chance: float = 0.1,
                 hill_terrain_base_chance: float = 0.05,
                 mountain_terrain_base_chance: float = 0.001,
                 snow_terrain_base_chance: float = -1.
                 ):
        """
Negative values for the base terrain chances means don't spawn trees on that type of terrain.
    The default for snow is -1, so don't spawn trees on snow.
        :param environment: The environment to generate the trees for.
        :param seed: The seed to use when using random numbers.
        :param octaves: The octaves to use when generating the noise map, in order of strength: 0.5 then 0.25 ...
        Default is [5, 10]
        :param player_base_radius: The radius for different spawn chances of trees.
        :param player_base_tree_chance: The spawn chance of trees, regardless of terrain, around a player base.
        Overrides the terrain chances if larger than or equal to 0.
        If negative then this is ignored.
        :param player_base_min_num_trees: The minimum number of trees around a player base.
        :param player_base_max_num_trees: The maximum number of trees around a player base.
        :param clear_terrain_base_chance: The base chance for spawning trees on a clearing.
        :param hill_terrain_base_chance: The base chance for spawning trees on a hill.
        :param mountain_terrain_base_chance: The base chance for spawning trees on a mountain.
        :param snow_terrain_base_chance: The base chance for spawning trees on snow.
        """

        super().__init__(environment)

        self._seed: int = seed
        self._octaves: list[int] = octaves if octaves is not None else [5, 10]

        self._player_base_radius: int = player_base_radius
        self._player_base_tree_chance: float = player_base_tree_chance
        self._player_base_min_num_trees: int = player_base_min_num_trees
        self._player_base_max_num_trees: int = player_base_max_num_trees

        self._clear_terrain_base_chance: float = clear_terrain_base_chance
        self._hill_terrain_base_chance: float = hill_terrain_base_chance
        self._mountain_terrain_base_chance: float = mountain_terrain_base_chance
        self._snow_terrain_base_chance: float = snow_terrain_base_chance

        self.sanity_check()

    # region - Getters
    @property
    def seed(self) -> int:
        return self._seed

    @property
    def octaves(self) -> list[int]:
        return self._octaves.copy()

    @property
    def player_base_radius(self) -> int:
        return self._player_base_radius

    @property
    def player_base_tree_chance(self) -> float:
        return self._player_base_tree_chance

    @property
    def player_base_min_num_trees(self) -> int:
        return self._player_base_min_num_trees

    @property
    def player_base_max_num_trees(self) -> int:
        return self._player_base_max_num_trees

    @property
    def clear_terrain_base_chance(self) -> float:
        return self._clear_terrain_base_chance

    @property
    def hill_terrain_base_chance(self) -> float:
        return self._hill_terrain_base_chance

    @property
    def mountain_terrain_base_chance(self) -> float:
        return self._mountain_terrain_base_chance

    @property
    def snow_terrain_base_chance(self) -> float:
        return self._snow_terrain_base_chance

    # endregion - Getters

    # region - Setters
    @seed.setter
    def seed(self, new_seed: int):
        assert isinstance(new_seed, int), "Seed must be a positive integer"
        assert new_seed > 0, "Seed must be a positive integer"

        self._seed = new_seed
        self.make_out_of_date()

    @octaves.setter
    def octaves(self, new_octaves: list[int]):
        assert isinstance(new_octaves, list), "Octaves must be a list of positive integers"
        assert new_octaves, "Octaves must be a list of positive integers"
        assert [None for octave in new_octaves if octave > 0], "Octaves must be a list of positive integers"

        self._octaves = new_octaves.copy()
        self.make_out_of_date()

    @player_base_radius.setter
    def player_base_radius(self, new_radius: int):
        assert isinstance(new_radius, int), "Player base radius must be a positive integer"
        assert new_radius > 0, "Player base radius must be a positive integer"

        self._player_base_radius = new_radius
        self.make_out_of_date()

    @player_base_tree_chance.setter
    def player_base_tree_chance(self, new_chance: float):
        assert isinstance(new_chance, float), "Base tree chance must be a float in the range (-inf, 1]"
        assert new_chance <= 1, "Base tree chance must be a float in the range (-inf, 1]"

        self._player_base_tree_chance = new_chance
        self.make_out_of_date()

    @player_base_min_num_trees.setter
    def player_base_min_num_trees(self, new_min: int):
        assert isinstance(new_min, int), "Min number of trees must be a positive integer"
        assert new_min >= 0, "Min number of trees must be a positive integer"

        self._player_base_min_num_trees = new_min
        self.make_out_of_date()

    @player_base_max_num_trees.setter
    def player_base_max_num_trees(self, new_max: int):
        assert isinstance(new_max, int), "Max number of trees must be a positive integer larger than or equal to the " \
                                         "min"
        assert new_max >= self._player_base_min_num_trees, "Max number of trees must be a positive integer larger " \
                                                           "than or equal to the min"

        self._player_base_max_num_trees = new_max
        self.make_out_of_date()

    @clear_terrain_base_chance.setter
    def clear_terrain_base_chance(self, new_chance: float):
        assert isinstance(new_chance, float), "Base clearing chance must be a float in the range (-inf, 1]"
        assert 0 <= new_chance <= 1, "Base clearing chance must be a float in the range (-inf, 1]"

        self._clear_terrain_base_chance = new_chance
        self.make_out_of_date()

    @hill_terrain_base_chance.setter
    def hill_terrain_base_chance(self, new_chance: float):
        assert isinstance(new_chance, float), "Base hill chance must be a float in the range (-inf, 1]"
        assert new_chance <= 1, "Base hill chance must be a float in the range (-inf, 1]"

        self._hill_terrain_base_chance = new_chance
        self.make_out_of_date()

    @mountain_terrain_base_chance.setter
    def mountain_terrain_base_chance(self, new_chance: float):
        assert isinstance(new_chance, float), "Base mountain chance must be a float in the range (-inf, 1]"
        assert new_chance <= 1, "Base mountain chance must be a float in the range (-inf, 1]"

        self._mountain_terrain_base_chance = new_chance
        self.make_out_of_date()

    @snow_terrain_base_chance.setter
    def snow_terrain_base_chance(self, new_chance: float):
        assert isinstance(new_chance, float), "Base snow chance must be a float in the range (-inf, 1]"
        assert new_chance <= 1, "Base snow chance must be a float in the range (-inf, 1]"

        self._snow_terrain_base_chance = new_chance
        self.make_out_of_date()

    # endregion - Setters

    def sanity_check(self):
        """
A quick sanity check to see if all variables make sense.
Runs a bunch of asserts checking for correct values.
Honestly I think this is unnecessary.
        """

        self.save_out_of_date()

        self.seed = self._seed
        self.octaves = self._octaves
        self.player_base_radius = self._player_base_radius
        self.player_base_tree_chance = self._player_base_tree_chance
        self.player_base_min_num_trees = self._player_base_min_num_trees
        self.player_base_max_num_trees = self._player_base_max_num_trees
        self.clear_terrain_base_chance = self._clear_terrain_base_chance
        self.hill_terrain_base_chance = self._hill_terrain_base_chance
        self.mountain_terrain_base_chance = self._mountain_terrain_base_chance
        self.snow_terrain_base_chance = self._snow_terrain_base_chance

        self.return_out_of_date()

    def generate_noise_map(self):
        """
Generates the noise map using the information stored.
Should be called after changing any values.
        """

        # Mr Clean
        self.noise_map.clear()

        # Terrain base chances
        for y in range(self.environment.y_size):
            for x in range(self.environment.x_size):
                terrain = self.environment[x, y].terrain

                if terrain == GridSquareTerrain.CLEAR:
                    if self._clear_terrain_base_chance < 0:
                        self.noise_map[x, y] = float('-inf')
                    else:
                        self.noise_map[x, y] = self._clear_terrain_base_chance

                elif terrain == GridSquareTerrain.HILL:
                    if self._hill_terrain_base_chance < 0:
                        self.noise_map[x, y] = float('-inf')
                    else:
                        self.noise_map[x, y] = self._hill_terrain_base_chance

                elif terrain == GridSquareTerrain.MOUNTAIN:
                    if self._mountain_terrain_base_chance < 0:
                        self.noise_map[x, y] = float('-inf')
                    else:
                        self.noise_map[x, y] = self._mountain_terrain_base_chance

                elif terrain == GridSquareTerrain.SNOW:
                    if self._snow_terrain_base_chance < 0:
                        self.noise_map[x, y] = float('-inf')
                    else:
                        self.noise_map[x, y] = self._snow_terrain_base_chance

                # Player Base, base chance
                if self._player_base_tree_chance < 0:
                    continue

                for location in self.environment.player_base_locations:
                    distance = sqrt((location[0] - x) ** 2 + (location[1] - y) ** 2)

                    if distance < self._player_base_radius:
                        self.noise_map[x, y] = self._player_base_tree_chance

        # Perlin noise time
        all_noise = [PerlinNoise(octaves=octave, seed=self._seed) for octave in self._octaves]

        for y in range(self.environment.y_size):
            for x in range(self.environment.x_size):
                for i, noise in enumerate(all_noise, start=2):
                    self.noise_map[x, y] += noise([x / self.environment.x_size, y / self.environment.y_size]) / i

        # Normalise
        self.noise_map.normalise_values(make_min_0=False)

        # Now in date
        self.make_in_date()

    def generate(self):
        """
Sets the structure parameter in grid squares if a random number is less than the noise value.
Ignores any grid squares that already have a structure.
        """

        assert self.is_out_of_date is False, "Current noise map is out of date, please call generate_noise_map before " \
                                             "this"
                                             
        # Kinda seedy
        random.seed(self._seed)

        # Generate the trees
        for y in range(self.environment.y_size):
            for x in range(self.environment.x_size):
                number = random.random()

                if self.environment[x, y].terrain == GridSquareTerrain.RIVER:
                    continue

                if self.environment[x, y].structure != GridSquareStructures.NONE:
                    continue

                if number < self.noise_map[x, y]:
                    self.environment[x, y].structure = GridSquareStructures.TREE

        # Check for the min and max number of trees
        for location in self.environment.player_base_locations:
            grid_squares_with_trees = []

            y_min = location[1] - self._player_base_radius
            y_min = y_min if y_min > 0 else 0
            y_max = location[1] + self._player_base_radius + 1
            y_max = y_max if y_max < self.environment.y_size else self.environment.y_size

            x_min = location[0] - self._player_base_radius
            x_min = x_min if x_min > 0 else 0
            x_max = location[0] + self._player_base_radius + 1
            x_max = x_max if x_max < self.environment.y_size else self.environment.x_size

            for y in range(y_min, y_max):
                for x in range(x_min, x_max):
                    distance = sqrt((location[0] - x) ** 2 + (location[1] - y) ** 2)

                    if distance > self._player_base_radius:
                        continue

                    if self.environment[x, y].structure == GridSquareStructures.TREE:
                        grid_squares_with_trees.append(self.environment[x, y])

            # Too many trees
            if len(grid_squares_with_trees) > self._player_base_max_num_trees:
                # Get the number of trees to remove
                num_to_remove = len(grid_squares_with_trees) - self._player_base_max_num_trees

                # Shuffle trees
                random.shuffle(grid_squares_with_trees)

                # Remove trees
                for i in range(num_to_remove):
                    grid_squares_with_trees[i].structure = GridSquareStructures.NONE

            # Too little trees
            elif len(grid_squares_with_trees) < self._player_base_min_num_trees:
                # Get the number of trees to add
                num_to_add = self._player_base_min_num_trees - len(grid_squares_with_trees) + 1

                # Get all grid squares with no structures
                grid_squares_with_no_structures = []

                for y in range(y_min, y_max):
                    for x in range(x_min, x_max):
                        distance = sqrt((location[0] - x) ** 2 + (location[1] - y) ** 2)

                        if distance > self._player_base_radius:
                            continue

                        if self.environment[x, y].structure == GridSquareStructures.NONE:
                            grid_squares_with_no_structures.append(self.environment[x, y])

                # Prevent index errors
                if num_to_add > len(grid_squares_with_no_structures):
                    num_to_add = len(grid_squares_with_no_structures)

                # Shuffle and add
                random.shuffle(grid_squares_with_no_structures)
                for i in range(num_to_add):
                    grid_squares_with_no_structures[i].structure = GridSquareStructures.TREE
