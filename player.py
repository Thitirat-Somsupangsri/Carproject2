import random


class Player:
    def __init__(self, name, car_image=None):
        self.name = name
        self.score = 0
        self.position = 0
        self.car_image = random.choice(car_image)

    def set_position(self, pos):
        self.position = pos

    def move(self):
        self.position += 1
        self.score += 1

    def reset_player(self):
        self.score = 0
        self.position = 0

    def draw(self, screen):
        screen.blit(self.car_image, (0, self.position))

    def update_score(self, screen, font):
        score_text = font.render(f"{self.name}: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))


class Bot:
    pass