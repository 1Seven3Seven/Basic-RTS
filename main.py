# ToDo: UI Time
# ToDo: Map creating tool
# ToDo: Create a save format for maps that is easily upgradable

import matplotlib.pyplot as plt

from environment import Environment
from environment.EnvironmentData import GridSquareTerrain, GridSquareStructures
from environment.Generators import TerrainGenerator, TreeGenerator, StoneGenerator, GeneratorHandler


def main():
    env = Environment(100, 100)
    env.set_player_base(1, 1)
    env.set_player_base(env.x_size - 3, env.y_size - 3)

    generator_handler = GeneratorHandler(
        terrain_generator := TerrainGenerator(env),
        tree_generator := TreeGenerator(env),
        stone_generator := StoneGenerator(env)
    )

    # generator_handler.generate_noise_maps()
    # generator_handler.generate()


    terrain_generator.generate_noise_map()
    terrain_generator.generate()

    tree_generator.generate_noise_map()
    stone_generator.generate_noise_map()
    tree_generator.generate()
    stone_generator.generate()

    # Colours
    terrain_colours = {
        GridSquareTerrain.CLEAR: (70, 110, 45),
        GridSquareTerrain.HILL: (50, 80, 50),
        GridSquareTerrain.MOUNTAIN: (50, 55, 70),
        GridSquareTerrain.SNOW: (255, 255, 255)
    }

    structure_colours = {
        GridSquareStructures.PLAYER_BASE: (255, 0, 0),
        GridSquareStructures.TREE: (0, 255, 0),
        GridSquareStructures.STONE: (0, 0, 255)
    }

    colour_map = [[(0, 0, 0) for _ in range(env.x_size)] for _ in range(env.y_size)]
    for y in range(env.y_size):
        for x in range(env.x_size):
            # Check for structure first
            if env[x, y].structure in structure_colours:
                colour_map[y][x] = structure_colours[env[x, y].structure]
                continue

            # Then terrain
            colour_map[y][x] = terrain_colours[env[x, y].terrain]

    # Displaying the environment
    plt.imshow(colour_map)
    plt.show()


if __name__ == "__main__":
    main()
