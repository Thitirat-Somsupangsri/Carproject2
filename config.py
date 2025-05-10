import pygame as pg
import random


class Config:
    def __init__(self):
        self.__screen_width = 1300
        self.__screen_height = 850

        self.__background_tile_size = 16
        self.__road_tile_size = 64

        self.__bg_grid_width = self.__screen_width // self.__background_tile_size
        self.__bg_grid_height = self.__screen_height // self.__background_tile_size

        self.__road_grid_width = self.__screen_width // self.__road_tile_size
        self.__road_grid_height = self.__screen_height // self.__road_tile_size

        self.__background_images_intro = [
            pg.image.load("game_assets/Environment/green.png").convert(),
            pg.image.load("game_assets/Environment/flower.png").convert(),
            pg.image.load("game_assets/Environment/grass.png").convert(),
            pg.image.load("game_assets/Environment/hill.png").convert()
        ]

        self.__road_tile = pg.image.load('game_assets/Environment/Summer_road (64 x 64).png').convert()

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
        road_marking = pg.image.load('game_assets/Environment/Road_markings.png').convert()
        for y in range(max_y):
            for x in range(max_x):
                tile = self.__background_grid[y][x]
                screen.blit(tile, (x * self.__background_tile_size, y * self.__background_tile_size))
        if event == 'intro':
            screen.blit(road_marking, (1200,20))
        elif event == 'mode1':
            road_x_start = 836

            for y in range(self.__road_grid_height):
                pos_x = road_x_start
                pos_y = y * self.__road_tile_size
                screen.blit(self.__road_tile, (pos_x, pos_y))

        elif event == 'mode2':
            center = self.__screen_width // 2
            bot_lane_start = center + 10
            player_lane_start = center + 340

            for y in range(self.__road_grid_height):
                # bot lane
                bot_x = bot_lane_start
                bot_y = y * self.__road_tile_size
                screen.blit(self.__road_tile, (bot_x, bot_y))

                # player lane
                player_x = player_lane_start
                player_y = y * self.__road_tile_size
                screen.blit(self.__road_tile, (player_x, player_y))
