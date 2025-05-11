import random

import pygame as pg
from random_vocabulary import Vocabulary
from bot_train import update_word_time_csv
from prob_character import WalkingProbs
from player import PlayerDataManager
from sfx import SoundEffects
import time
import csv


class Mode:
    def __init__(self, player, font, background):
        self.player = player
        self.font = font
        self.def_font = pg.font.Font("game_assets/Grand9K Pixel.ttf", 24)
        self.background = background

        self.vocabulary = Vocabulary('dictionary/filtered_dictionary.csv')
        self.current_word = self.vocabulary.random_word()

        self.input_border_color = (255, 255, 255)
        self.user_input = ''
        self.running = True
        self.flash_timer = 0
        self.flash_duration = 0.7
        self.waiting_for_flash = False

        self.screen_width, self.screen_height = (self.background.screen_width,
                                                 self.background.screen_height)
        self.car_y = self.screen_height // 2

        self.reveal_word_answer = ''

        self.hint_letter = 0

        self.answer_start_time = time.time()
        self.round_time = time.time()

        self.score_ratio = 1
        self.char_images = [
            pg.image.load("game_assets/character/Cop.png").convert_alpha(),
            pg.image.load("game_assets/character/Cop2.png").convert_alpha(),
            pg.image.load("game_assets/character/Cop3.png").convert_alpha()
        ]
        self.walk_prob = None
        self.hint_left = self.player.hint_left
        self.manager = PlayerDataManager()

    def stop(self):
        self.running = False

    def event(self, event):
        if event.type == pg.KEYDOWN:
            SoundEffects.get_instance().play("typing")
            if event.key == pg.K_RETURN:
                self.check_answer()
            elif event.key == pg.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif event.key == pg.K_UP and self.hint_left > 0:
                self.use_hint()
            else:
                self.user_input += event.unicode.lower()
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.walk_prob and self.walk_prob.check_click(event.pos):
                print("clicked")
                self.hint_left += 1

    def use_hint(self):
        if self.hint_letter < len(self.current_word['word']):
            self.user_input = ''
            self.hint_letter += 1
            self.hint_left -= 1


    def check_answer(self):
        user_answer = self.current_word['word'][0]
        for i in range(1,self.hint_letter+1):
            user_answer += self.current_word['word'][i]

        user_answer += self.user_input.strip().lower()[:len(self.current_word['word']) -1 - self.hint_letter]
        self.hint_letter = 0
        self.reveal_word_answer = self.current_word['word'].upper()
        if random.randint(1, 3) == 1:
            x = random.randint(100, 1200)
            y = random.randint(100, 700)
            self.walk_prob = WalkingProbs(x, y, self.char_images, (50, 1150, 50, 750))
        else:
            self.walk_prob = None

        print(f"answer: {user_answer} == {self.current_word['word']}")
        if self.current_word['word'] == user_answer:
            self.input_border_color = (0, 155, 0)
            if self == Mode2:
                self.score_ratio = 1
            self.player.score += 1 * self.score_ratio
            self.flash_timer = self.flash_duration
            time_taken = time.time() - self.answer_start_time
            update_word_time_csv(len(self.current_word['word']), time_taken)
            self.player.move()
            SoundEffects.get_instance().play("move")
            self.waiting_for_flash = True
            return True
        else:
            self.input_border_color = (155, 0, 0)

            self.flash_timer = self.flash_duration
            self.waiting_for_flash = True
            return False

    def update(self, delta_time):
        if self.walk_prob:
            self.walk_prob.update()
        if self.flash_timer > 0:
            self.flash_timer -= delta_time
            if self.flash_timer <= 0:
                self.input_border_color = (255, 255, 255)
                self.reveal_word_answer = ''

        if self.waiting_for_flash and self.flash_timer <= 0:
            self.user_input = ''
            self.current_word = self.vocabulary.random_word()
            self.answer_start_time = time.time()
            self.waiting_for_flash = False

    def draw(self, screen):
        if self.walk_prob:
            self.walk_prob.draw(screen)

        part_of_speech = self.current_word.get('part_of_speech', '')
        definition_text = f"Define ({part_of_speech}): {self.current_word['definition']}"

        small_font = pg.font.Font("game_assets/Grand9K Pixel.ttf", 24)
        words = definition_text.split(' ')
        lines = []
        current_line = ''
        max_width = screen.get_width() // 2 - 100

        # definition line
        for word in words:
            test_line = current_line + word + ' '
            if small_font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '
        lines.append(current_line)

        # definition box
        text_box_height = len(lines) * small_font.get_linesize() + 20
        transparency = pg.Surface((screen.get_width() // 2 - 60, text_box_height), pg.SRCALPHA)

        pg.draw.rect(transparency, (50, 50, 50, 128),
                         pg.Rect(0, 0, screen.get_width() // 2 - 60, text_box_height))
        screen.blit(transparency, (40, 80))
        y_offset = 90
        for line in lines:
            line_surface = small_font.render(line, True, (255, 255, 255))
            screen.blit(line_surface, (50, y_offset))
            y_offset += small_font.get_linesize()

        word = self.current_word['word']
        word_length = len(word)
        display_text = word[0].upper() + ' '
        if self.hint_letter > 0:
            for i in range(1, self.hint_letter + 1):
                display_text += self.current_word['word'][i].upper() + ' '
                word_length -= 1

        for i in range(word_length-1):
            if i < len(self.user_input):
                display_text += self.user_input[i].upper() + ' '
            else:
                display_text += '_ '


        # input box
        input_box = pg.Rect((80, 550, 500, 70))
        pg.draw.rect(screen, (255, 255, 255), input_box)
        pg.draw.rect(screen, self.input_border_color, input_box, 3)
        input_text_surface = self.font.render(display_text.strip(), True, (0, 0, 0))
        screen.blit(input_text_surface, (input_box.x + 10, input_box.y - 5))

        # answer
        font = pg.font.Font("game_assets/Grand9K Pixel.ttf", 30)
        answer = font.render(self.reveal_word_answer, True, (0, 0, 0))
        screen.blit(answer, (input_box.x + 20, 500))

        hint = font.render(f'Hint: {self.hint_left}', True, (250,250,250))
        screen.blit(hint, (1180, 10))


class Mode1(Mode):
    def __init__(self, player, font, background):
        super().__init__(player, font, background)
        self.mistakes = 0
        self.max_mistakes = 3
        self.move_distance = int(self.background.screen_height * 0.25)
        self.heart_image = pg.image.load('game_assets/hearts/heart.png').convert_alpha()
        self.blackheart_image = pg.image.load('game_assets/hearts/border.png').convert_alpha()
        self.def_font = pg.font.Font('game_assets/Grand9K Pixel.ttf', 24)
        self.streak = 0
        self.highest_streak = 0

    def check_answer(self):
        if super().check_answer():
            self.streak += 1
            if self.streak >= 3:
                self.score_ratio += 1
            if self.car_y < 0:
                self.car_y = self.screen_height

        else:
            SoundEffects.get_instance().play("beep")
            self.mistakes += 1
            if self.streak > self.highest_streak:
                self.highest_streak = self.streak
            self.streak = 0
            self.score_ratio = 1

        if self.mistakes >= self.max_mistakes:
            time_taken = time.time() - self.round_time
            self.time_played(time_taken)
            self.manager.update_mode1(self.player.name, self.player.score, self.highest_streak, time_taken, self.hint_left)
            self.stop()

    def time_played(self, duration):
        with open('stats/mode1_stats.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.player.name, round(duration, 2),self.player.score])

    def draw(self, screen):
        self.background.draw(screen, 'mode1')
        self.player.draw(screen, 890)
        super().draw(screen)
        font = pg.font.Font("game_assets/Grand9K Pixel.ttf", 26)
        self.player.update_score(screen, font, 100, 10)
        pos_heart_x, pos_heart_y = screen.get_width() * 0.8, 50

        for i in range(self.mistakes):
            screen.blit(self.blackheart_image, (pos_heart_x + ((3 - i - 1) * 65), pos_heart_y))

        for i in range(3 - self.mistakes):
            screen.blit(self.heart_image, (pos_heart_x + (i * 65), pos_heart_y))

        streak = font.render(f'Streak: {self.streak}', True, (255, 255, 255))
        screen.blit(streak, (1000, 10))

    def update(self, delta_time):
        super().update(delta_time)
        self.player.update(delta_time)


class Mode2(Mode):
    def __init__(self, player, bot, font, background):
        super().__init__(player, font, background)

        self.bot = bot

        self.total_time = 30
        self.elapsed_time = 0

        self.bot_x = self.screen_width // 2 + 394
        self.player_x = self.screen_width // 2 + 66

        self.player.position = self.screen_height // 2
        self.bot.position = self.screen_height // 2

        self.bot.start_new_word(len(self.current_word['word']))

        self.finish_line_image = pg.image.load("game_assets/Environment/finish.png").convert_alpha()
        self.finish_y = 450
        self.player_finish_visible = False
        self.bot_finish_visible = False

        self.winner = None
        self.winner_timer = 0
        self.winner_delay = 1.0

    def check_answer(self):
        if super().check_answer():
            if self.car_y < 0:
                self.car_y = self.screen_height
            if self.player.score >= 9:
                self.player_finish_visible = True
        self.bot.start_new_word(len(self.current_word['word']))

    def update(self, delta_time):
        super().update(delta_time)
        if self.bot.score >= 9:
            self.bot_finish_visible = True

        self.elapsed_time += delta_time

        bot_moved = self.bot.update(delta_time)
        self.player.update(delta_time)

        if bot_moved:
            SoundEffects.get_instance().play("move")
            self.current_word = self.vocabulary.random_word()
            self.user_input = ''
            self.bot.start_new_word(len(self.current_word['word']))

        if self.player.score == 2:
            self.winner = 'player'
            self.winner_timer += delta_time
            if self.winner_timer >= self.winner_delay:
                self.manager.update_mode2(self.player.name,self.player.hint_left,True)
                self.stop()
                return

        elif self.bot.score == 10:
            self.winner = 'bot'
            self.winner_timer += delta_time
            if self.winner_timer >= self.winner_delay:
                self.manager.update_mode2(self.player.name, self.hint_left)
                self.stop()
                return

        if self.elapsed_time >= self.total_time:
            if self.player.score > self.bot.score:
                self.winner = 'player'
                self.manager.update_mode2(self.player.name, self.hint_left,True)
            elif self.player.score < self.bot.score:
                self.winner = 'bot'
                self.manager.update_mode2(self.player.name,self.hint_left)
            self.stop()
            return

    def draw(self, screen):
        self.background.draw(screen, 'mode2')

        self.bot.draw(screen, self.bot_x)
        self.player.draw(screen, self.player_x)

        super().draw(screen)
        font = pg.font.Font("game_assets/Grand9K Pixel.ttf", 26)
        self.player.update_score(screen, font, self.player_x - 200)
        self.bot.update_score(screen, font, self.bot_x - 150)

        remaining_time = max(0, int(self.total_time - self.elapsed_time))
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        timer_text = font.render(f"Time Left: {minutes:02}:{seconds:02}",
                                 True, (255, 255, 255))
        screen.blit(timer_text, (100, 10))

        center = self.screen_width // 2
        bot_lane_start = center + 372
        player_lane_start = center + 42

        if self.player_finish_visible:
            screen.blit(
                self.finish_line_image,
                (player_lane_start, self.finish_y)
            )
        if self.bot_finish_visible:
            screen.blit(
                self.finish_line_image,
                (bot_lane_start, self.finish_y)
            )
