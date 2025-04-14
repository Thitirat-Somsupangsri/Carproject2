import pygame
import random

class Config:
    def __init__(self):
        self.__screen_width = 1400
        self.__screen_height = 900

        self.__background_tile_size = 16
        self.__road_tile_size = 64

        self.__bg_grid_width = self.__screen_width // self.__background_tile_size
        self.__bg_grid_height = self.__screen_height // self.__background_tile_size

        self.__road_grid_width = self.__screen_width // self.__road_tile_size
        self.__road_grid_height = self.__screen_height // self.__road_tile_size

        self.__background_images_intro = [
            pygame.image.load("game_assets/Environment/Desert.png").convert(),
            pygame.image.load("game_assets/Environment/cactus.png").convert(),
            pygame.image.load("game_assets/Environment/sand.png").convert(),
            pygame.image.load("game_assets/Environment/rock.png").convert()
        ]

        self.__road_tile = pygame.image.load('game_assets/Environment/Summer_road (64 x 64).png').convert()

        self.__background_probabilities = [0.91, 0.01, 0.07, 0.01]
        self.__background_grid = self.create_background_grid()

    @property
    def screen_height(self):
        return self.__screen_height

    @property
    def screen_width(self):
        return self.__screen_width

    def create_background_grid(self):
        grid = []
        for y in range(self.__bg_grid_height):
            row = []
            for x in range(self.__bg_grid_width):
                selected_tile = random.choices(self.__background_images_intro,
                                               self.__background_probabilities)[0]
                row.append(selected_tile)
            grid.append(row)
        return grid

    def draw(self, screen, event):
        max_y = min(self.__bg_grid_height, len(self.__background_grid))
        max_x = min(self.__bg_grid_width, len(self.__background_grid[0]))

        if event == 'intro':
            for y in range(max_y):
                for x in range(max_x):
                    tile = self.__background_grid[y][x]
                    screen.blit(tile, (x * self.__background_tile_size, y * self.__background_tile_size))

        elif event == 'mode1':
            for y in range(max_y):
                for x in range(max_x):
                    tile = self.__background_grid[y][x]
                    screen.blit(tile, (x * self.__background_tile_size, y * self.__background_tile_size))

            center_screen_x = self.__screen_width // 2

            road_width_pixels = self.__road_tile_size * 3
            road_x_start = center_screen_x - (road_width_pixels // 2)

            for y in range(self.__road_grid_height):
                for x in range(3):
                    pos_x = road_x_start + (x * self.__road_tile_size)
                    pos_y = y * self.__road_tile_size
                    screen.blit(self.__road_tile, (pos_x, pos_y))
