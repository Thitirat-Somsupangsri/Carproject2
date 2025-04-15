import random
import csv


class Player:
    def __init__(self, name, car_image=None):
        self.name = name
        self.score = 0
        self.position = 450
        self.car_image = random.choice(car_image)
        self.target_position = None
        self.moving = False
        self.speed = 200

    def move(self):
        if not self.moving:
            self.target_position = self.position - 200
            self.moving = True

    def reset_player(self):
        self.score = 0
        self.position = 0

    def draw(self, screen,x):
        screen.blit(self.car_image, (x, self.position))

    def update_score(self, screen, font,x,y = 10):
        score_text = font.render(f"{self.name}: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (x, y))

    def update(self, delta_time):
        if self.moving and self.target_position is not None:
            distance = self.speed * delta_time
            if self.position - distance <= self.target_position:
                self.position = self.target_position
                self.moving = False
                if self.position < 0:
                    self.position = 900
            else:
                self.position -= distance


class Bot(Player):
    def __init__(self, name, car_image=None):
        super().__init__(name, car_image)
        self.data_file = 'word_time_data.csv'
        self.word_time_data = self.load_data()
        self.target_time = None
        self.current_time = 0
        self.active = False

    def load_data(self):
        data = {}
        with open(self.data_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                length = int(row['word_length'])
                average_time = float(row['average_time'])
                data[length] = average_time
        return data

    def estimate_time(self, word_length):
        average_time = self.word_time_data.get(word_length, 30)
        lower_bound = max(1, average_time - 10)
        upper_bound = average_time + 15
        return random.uniform(lower_bound, upper_bound)

    def start_new_word(self, word_length):
        self.target_time = self.estimate_time(word_length)
        self.current_time = 0
        self.active = True

    def update(self, delta_time):
        if self.active and self.target_time is not None:
            self.current_time += delta_time
            if self.current_time >= self.target_time:
                self.move()
                self.score += 1
                if self.position < 0:
                    self.position = 900
                self.active = False
                return True
        super().update(delta_time)
