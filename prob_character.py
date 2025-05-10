import random
import time
import pygame as pg


class WalkingProbs:
    def __init__(self, x, y, images, move_area, duration=5):
        self.__x = x
        self.__y = y
        self.__images = images
        self.image_index = 0
        image_rect = self.__images[0].get_rect(topleft=(self.__x, self.__y))
        self.rect = pg.Rect(self.__x - 10, self.__y - 10, image_rect.width + 100, image_rect.height + 100)

        self.move_area = move_area
        self.start_time = time.time()
        self.duration = duration
        self.active = True
        self.clicked = False

        self.speed = 1.5
        self.direction = random.choice(["up", "down", "left", "right"])
        self.change_dir_timer = 0

        self.last_frame_time = time.time()
        self.frame_interval = 0.15

    def update(self):
        if not self.active:
            return

        if time.time() - self.start_time > self.duration:
            self.active = False
            return

        if self.direction == "up":
            self.__y -= self.speed
        elif self.direction == "down":
            self.__y += self.speed
        elif self.direction == "left":
            self.__x -= self.speed
        elif self.direction == "right":
            self.__x += self.speed

        if time.time() - self.last_frame_time >= self.frame_interval:
            self.image_index = (self.image_index + 1) % len(self.__images)
            self.last_frame_time = time.time()
        self.rect.topleft = (self.__x - 10, self.__y - 10)

    def draw(self, screen):
        if self.active:
            screen.blit(self.__images[self.image_index], (self.__x, self.__y))

    def check_click(self, pos):
        if self.active and self.rect.collidepoint(pos):
            self.active = False
            self.clicked = True
            return True
        return False
