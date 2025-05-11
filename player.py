import random
import csv
import json
import os


class Player:
    def __init__(self, name, car_image=None):
        self.name = name
        self.score = 0
        self.position = 450
        self.car_image = random.choice(car_image)
        self.target_position = None
        self.moving = False
        self.speed = 200
        self.hint_left = 0

    def move(self):
        if not self.moving:
            self.target_position = self.position - 200
            self.moving = True

    def reset_player(self):
        self.score = 0
        self.position = 450

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
        self.data_file = 'stats/word_time_data.csv'
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
        lower_bound = max(5, average_time - 10)
        upper_bound = average_time + 15
        return random.uniform(lower_bound, upper_bound)

    def start_new_word(self, word_length):
        self.current_time = 0
        self.target_time = self.estimate_time(word_length)
        self.active = True

    def update(self, delta_time):
        if self.active and self.target_time is not None:
            self.current_time += delta_time
            if self.current_time >= self.target_time:
                self.score += 1
                self.move()
                if self.position < 0:
                    self.position = 750
                self.active = False
                return True
        super().update(delta_time)


class PlayerDataManager:
    def __init__(self, filename="stats/player_data.json"):
        self.filename = filename
        self.data = self.__load()

    def __load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                return json.load(file)
        return {}

    def __save(self):
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4)

    def add_player(self, username):
        if username not in self.data:
            self.data[username] = {
                'played count in mode1': 0,
                'best score in mode1': 0,
                'average time played in mode1': 0,
                'played count in mode2': 0,
                'total wins in mode2': 0,
                'hints': 0,
                'highest streak': 0
            }

    def get_data(self, username, data):
        return self.data[username][data]

    def update_mode1(self, username, score, streak, duration, hint):
        self.add_player(username)
        player = self.data[username]

        player['played count in mode1'] += 1
        player['hints'] = hint

        if score > player['best score in mode1']:
            player['best score in mode1'] = score

        prev_total = player['average time played in mode1'] * (player['played count in mode1'] - 1)
        player['average time played in mode1'] = round((prev_total + duration) / player['played count in mode1'], 2)

        if streak > player['highest streak']:
            player['highest streak'] = streak

        self.__save()

    def update_mode2(self, username, hint, won=False,):
        self.add_player(username)
        player = self.data[username]
        player['hints'] = hint
        player['played count in mode2'] += 1
        if won:
            player['total wins in mode2'] += 1

        self.__save()
