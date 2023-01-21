import sys
from time import perf_counter_ns

import pygame
from pygame.locals import *

from Environment import Environment, GridSquareTerrain


def upon_exit():
    """
Function to be called upon wanting the pygame screen to close.
    """

    pygame.display.quit()
    sys.exit("Pygame screen close")


def main():
    # region - Initializing pygame
    pygame.init()
    pygame.display.set_caption("FPS: 000")
    window_size = (1280, 720)
    screen = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()
    # endregion - Initializing pygame

    # Environment
    env = Environment(100, 100)
    env.generate_terrain()

    # Colours
    colours = {
        GridSquareTerrain.CLEAR: (70, 110, 45),
        GridSquareTerrain.HILL: (50, 80, 50),
        GridSquareTerrain.MOUNTAIN: (50, 55, 70),
        GridSquareTerrain.SNOW: (255, 255, 255)
    }

    # Environment map
    env_map = pygame.Surface((env.x_size, env.y_size))
    for x in range(env.x_size):
        for y in range(env.y_size):
            env_map.set_at((x, y), colours[env[x, y].terrain])

    # Environment map scale and position
    scale = 3
    position = [window_size[0] / 2 - env.x_size * scale / 2, window_size[1] / 2 - env.y_size * scale / 2]

    # Timings
    current_time = perf_counter_ns()
    old_time = current_time

    # Main loop
    while True:
        scale_changed = False
        for event in pygame.event.get():
            if event.type == QUIT:
                upon_exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    upon_exit()

            if event.type == MOUSEWHEEL:
                scale_changed = True
                scale_changed_by = event.y
                scale += event.y / 10


        screen.fill((0, 0, 0))

        """BELOW"""
        pressed = pygame.key.get_pressed()

        if pressed[K_a]:
            position[0] += 1 * scale
        if pressed[K_d]:
            position[0] -= 1 * scale
        if pressed[K_w]:
            position[1] += 1 * scale
        if pressed[K_s]:
            position[1] -= 1 * scale

        new_size = (round(env.x_size * scale), round(env.y_size * scale))

        if scale_changed:
            position[0] += (old_size[0] - new_size[0]) / 2
            position[1] += (old_size[1] - new_size[1]) / 2

        screen.blit(pygame.transform.scale(env_map, new_size), position)

        old_size = new_size
        """ABOVE"""

        pygame.display.flip()
        current_time = perf_counter_ns()
        fps = round(1_000_000_000 / (current_time - old_time))
        clock.tick(60)
        old_time = current_time
        pygame.display.set_caption(f"FPS: {fps}")



if __name__ == "__main__":
    main()
