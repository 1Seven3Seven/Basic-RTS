from time import perf_counter as pc

import matplotlib.pyplot as plt

from environment import Environment
from environment.EnvironmentData import GridSquareTerrain, GridSquareStructures
from environment.Generators import TerrainGenerator, TreeGenerator, StoneGenerator


def main():
    very_start = pc()

    # Environment
    start = pc()
    env = Environment(100, 100)
    env.set_player_base(1, 1)
    env.set_player_base(env.x_size - 3, env.y_size - 3)
    print("Environment Setup".ljust(30), pc() - start)

    # Terrain Generator
    start = pc()
    terrain_generator = TerrainGenerator(env, seed=1)
    terrain_generator.generate_noise_map()
    terrain_generator.generate()
    print("Terrain Generator".ljust(30), pc() - start)

    # Tree Generator
    start = pc()
    tree_generator = TreeGenerator(env, seed=1)
    tree_generator.generate_noise_map()
    tree_generator.generate()
    print("Tree Generator".ljust(30), pc() - start)

    # Stone Generator
    start = pc()
    stone_generator = StoneGenerator(env, seed=1)
    stone_generator.generate_noise_map()
    stone_generator.generate()
    print("Stone Generator".ljust(30), pc() - start)

    # Updating connections
    start = pc()
    env.update_node_connections()
    print("Updating Node Connections".ljust(30), pc() - start)

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

    # Drawing the environment
    start = pc()
    colour_map = [[(0, 0, 0) for _ in range(env.x_size)] for _ in range(env.y_size)]
    for y in range(env.y_size):
        for x in range(env.x_size):
            # Check for structure first
            if env[x, y].structure in structure_colours:
                colour_map[y][x] = structure_colours[env[x, y].structure]
                continue

            # Then terrain
            colour_map[y][x] = terrain_colours[env[x, y].terrain]
    print("Drawing Environment".ljust(30), pc() - start)

    print("Total Time".ljust(30), pc() - very_start)

    # Displaying the environment
    plt.imshow(colour_map)
    plt.show()


if __name__ == "__main__":
    main()
