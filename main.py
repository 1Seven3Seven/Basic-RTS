import matplotlib.pyplot as plt
from AStar import AStar

from Environment import Environment, TerrainGenerator, TreeGenerator, StoneGenerator
from Environment.EnvironmentData import GridSquareTerrain, GridSquareStructures


def main():
    # Environment
    env = Environment(100, 100)
    env.set_player_base(1, 1)
    env.set_player_base(env.x_size - 3, env.y_size - 3)

    # Terrain Generator
    terrain_generator = TerrainGenerator(env, seed=1)
    terrain_generator.generate_noise_map()
    terrain_generator.generate()

    # Tree Generator
    tree_generator = TreeGenerator(env, seed=1)
    tree_generator.generate_noise_map()
    tree_generator.generate()

    # Stone Generator
    stone_generator = StoneGenerator(env, seed=1)
    stone_generator.generate_noise_map()
    stone_generator.generate()

    # Updating connections
    env.update_node_connections()

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
    colour_map = [[(0, 0, 0) for _ in range(env.x_size)] for _ in range(env.y_size)]
    for y in range(env.y_size):
        for x in range(env.x_size):
            # Check for structure first
            if env[x, y].structure in structure_colours:
                colour_map[y][x] = structure_colours[env[x, y].structure]
                continue

            # Then terrain
            colour_map[y][x] = terrain_colours[env[x, y].terrain]

    # Pathfinding
    a_star = AStar(start=env[1, 1], end=env[env.x_size - 3, env.y_size - 3])
    path = a_star.find_path()
    for node in path:
        colour = list(colour_map[node.y_position][node.x_position])
        colour = [value - 75 if value - 75 > 0 else 0 for value in colour]
        colour_map[node.y_position][node.x_position] = tuple(colour)

    # Displaying the environment
    plt.imshow(colour_map)
    plt.show()


if __name__ == "__main__":
    main()
