import pygame
from random_vocabulary import Vocabulary
from bot_train import update_word_time_csv
import time


class Mode:
    def __init__(self, player, font, background):
        self.player = player
        self.font = font
        self.def_font = pygame.font.Font("game_assets/Grand9K Pixel.ttf", 24)
        self.background = background

        self.vocabulary = Vocabulary('dictionary/filtered_dictionary.csv')
        self.current_word = self.vocabulary.random_word()
        self.word_length = len(self.current_word['word'])

        self.input_border_color = (255, 255, 255)
        self.user_input = ''
        self.running = True
        self.flash_timer = 0
        self.flash_duration = 0.7
        self.waiting_for_flash = False

        self.screen_width, self.screen_height = (self.background.screen_width,
                                                 self.background.screen_height)
        self.car_y = self.screen_height // 2

        self.reveal_word = ''

        self.answer_start_time = time.time()

    def stop(self):
        self.running = False

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.check_answer()
            elif event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            else:
                self.user_input += event.unicode.lower()

    def check_answer(self):
        user_answer = self.current_word['word'][0] + self.user_input.strip().lower()
        self.reveal_word = self.current_word['word'].upper()
        print(f"Checking answer: {user_answer} == {self.current_word['word']}")
        if self.current_word['word'] == user_answer:
            self.input_border_color = (0, 155, 0)
            self.player.score += 1
            self.flash_timer = self.flash_duration
            time_taken = time.time() - self.answer_start_time
            word_length = len(self.current_word['word'])
            update_word_time_csv(word_length, time_taken)
            self.player.move()
            self.waiting_for_flash = True
            return True
        else:
            self.input_border_color = (155, 0, 0)
            self.flash_timer = self.flash_duration
            self.waiting_for_flash = True
            return False

    def update(self, delta_time):
        if self.flash_timer > 0:
            self.flash_timer -= delta_time
            if self.flash_timer <= 0:
                self.input_border_color = (255, 255, 255)
                self.reveal_word = ''

        if self.waiting_for_flash and self.flash_timer <= 0:
            self.user_input = ''
            self.current_word = self.vocabulary.random_word()
            self.answer_start_time = time.time()
            self.waiting_for_flash = False

    def draw(self, screen):
        part_of_speech = self.current_word.get('part_of_speech', '')
        definition_text = f"Define ({part_of_speech}): {self.current_word['definition']}"

        small_font = pygame.font.Font("game_assets/Grand9K Pixel.ttf", 24)
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
        transparency = pygame.Surface((screen.get_width() // 2 - 60, text_box_height), pygame.SRCALPHA)

        pygame.draw.rect(transparency, (50, 50, 50, 128),
                         pygame.Rect(0,0, screen.get_width() // 2 - 60, text_box_height))
        screen.blit(transparency, (40, 80))
        y_offset = 90
        for line in lines:
            line_surface = small_font.render(line, True, (255, 255, 255))
            screen.blit(line_surface, (50, y_offset))
            y_offset += small_font.get_linesize()

        word = self.current_word['word']
        word_length = len(word)
        display_text = word[0].upper() + ' '

        for i in range(1, word_length):
            if i <= len(self.user_input):
                display_text += self.user_input[i - 1].upper() + ' '
            else:
                display_text += '_ '

        # input box
        input_box = pygame.Rect((80, 500, 500, 70))
        pygame.draw.rect(screen, (255, 255, 255), input_box)
        pygame.draw.rect(screen, self.input_border_color, input_box, 3)
        input_text_surface = self.font.render(display_text.strip(), True, (0,0,0))
        screen.blit(input_text_surface, (input_box.x + 10, input_box.y - 5))

        font = pygame.font.Font("game_assets/Grand9K Pixel.ttf", 32)
        answer = font.render(self.reveal_word, True, (0,0,0))
        screen.blit(answer, (input_box.x + 20, 430))


class Mode1(Mode):
    def __init__(self, player, font, background):
        super().__init__(player, font, background)
        self.mistakes = 0
        self.max_mistakes = 3
        self.move_distance = int(self.background.screen_height * 0.25)
        self.heart_image = pygame.image.load('game_assets/hearts/heart.png').convert_alpha()
        self.blackheart_image = pygame.image.load('game_assets/hearts/border.png').convert_alpha()
        self.def_font = pygame.font.Font('game_assets/Grand9K Pixel.ttf', 24)

    def check_answer(self):
        if super().check_answer():
            if self.car_y < 0:
                self.car_y = self.screen_height
        else:
            self.mistakes += 1

        if self.mistakes >= self.max_mistakes:
            self.stop()

    def draw(self, screen):
        self.background.draw(screen, 'mode1')
        self.player.draw(screen, 890)
        super().draw(screen)
        font = pygame.font.Font("game_assets/Grand9K Pixel.ttf", 26)
        self.player.update_score(screen, font, 1050 ,70)
        pos_heart_x, pos_heart_y = screen.get_width() * 0.8, 20

        for i in range(self.mistakes):
            screen.blit(self.blackheart_image, (pos_heart_x + ((3-i-1) * 65),pos_heart_y))

        for i in range(3-self.mistakes):
            screen.blit(self.heart_image, (pos_heart_x + (i * 65),pos_heart_y))

        '''
        mistakes_text = self.font.render(f"Hearts: ", True, (199, 21, 133))
        screen.blit(mistakes_text, (pos_heart_x - 180, pos_heart_y))
        '''

    def update(self, delta_time):
        super().update(delta_time)
        self.player.update(delta_time)


class Mode2(Mode):
    def __init__(self, player, bot, font, background):
        super().__init__(player, font, background)

        self.bot = bot

        self.total_time = 180
        self.elapsed_time = 0

        self.move_distance = 50

        self.bot_x = self.screen_width // 2 + 400
        self.player_x = self.screen_width // 2 + 70

        self.player.position = self.screen_height // 2
        self.bot.position = self.screen_height // 2

        self.bot.start_new_word(len(self.current_word['word']))

    def check_answer(self):
        if super().check_answer():
            if self.car_y < 0:
                self.car_y = self.screen_height
            if self.player.score == 20:
                print("Player wins by reaching finish line!")
                self.stop()
                return

            self.bot.start_new_word(len(self.current_word['word']))

    def update(self, delta_time):
        super().update(delta_time)
        self.elapsed_time += delta_time

        bot_moved = self.bot.update(delta_time)
        self.player.update(delta_time)

        if bot_moved:
            self.current_word = self.vocabulary.random_word()
            self.bot.start_new_word(len(self.current_word['word']))

        if (self.bot.score == 20 or self.player.score == 20
                or self.elapsed_time >= self.total_time):
            self.stop()
            return

    def draw(self, screen):
        self.background.draw(screen, 'mode2')

        self.bot.draw(screen,self.bot_x)
        self.player.draw(screen,self.player_x)

        super().draw(screen)
        font = pygame.font.Font("game_assets/Grand9K Pixel.ttf", 26)
        self.player.update_score(screen,font, self.player_x-200)
        self.bot.update_score(screen, font, self.bot_x - 150)

        remaining_time = max(0, int(self.total_time - self.elapsed_time))
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        timer_text = font.render(f"Time Left: {minutes:02}:{seconds:02}",
                                      True, (255, 255, 255))
        screen.blit(timer_text, (100, 10))

