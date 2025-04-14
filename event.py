import pygame
from random_vocabulary import Vocabulary

class Mode:
    def __init__(self, player, font, background):
        self.player = player
        self.font = font
        self.def_font = pygame.font.Font("game_assets/Grand9K Pixel.ttf", 24)
        self.background = background

        self.vocabulary = Vocabulary('dictionary/filtered_dictionary.csv')
        self.current_word = self.vocabulary.random_word()
        self.word_length = len(self.current_word['word'])

        self.user_input = ''
        self.running = True

        self.screen_width, self.screen_height = (self.background.screen_width,
                                                 self.background.screen_height)
        self.car_x = self.screen_width // 2 - self.player.car_image.get_width() // 2
        self.car_y = self.screen_height // 2

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
        print(f"Checking answer: {user_answer} == {self.current_word['word']}")
        if self.current_word['word'] == user_answer:
            return True
        else:
            return False


    def update(self):
        pass

    def draw(self, screen):
        part_of_speech = self.current_word.get('part_of_speech', '')
        definition_text = f"Define ({part_of_speech}): {self.current_word['definition']}"

        small_font = pygame.font.Font("game_assets/Grand9K Pixel.ttf", 24)
        words = definition_text.split(' ')
        lines = []
        current_line = ''
        max_width = screen.get_width() - 100

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
        transparency = pygame.Surface((screen.get_width() - 80, text_box_height), pygame.SRCALPHA)

        pygame.draw.rect(transparency, (50, 50, 50, 128), pygame.Rect(0,0, screen.get_width() - 80, text_box_height))
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
        input_box = pygame.Rect((80, 300, 450, 50))
        pygame.draw.rect(screen, (255, 255, 255), input_box)
        pygame.draw.rect(screen, (107, 142, 35), input_box, 2)
        input_text_surface = self.font.render(display_text.strip(), True, (0,0,0))
        screen.blit(input_text_surface, (input_box.x + 10, input_box.y - 5))


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
            self.car_y -= self.move_distance
            self.player.score += 1
            if self.car_y < 0:
                self.car_y = self.screen_height
        else:
            self.mistakes += 1

        self.user_input = ''
        self.current_word = self.vocabulary.random_word()

        if self.mistakes >= self.max_mistakes:
            self.stop()

    def draw_text_wrapped(self, surface, text, font, color, x, y, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''

        for word in words:
            test_line = current_line + word + ' '
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '
        lines.append(current_line)

        for idx, line in enumerate(lines):
            line_surface = font.render(line, True, color)
            surface.blit(line_surface, (x, y + idx * font.get_linesize()))

    def draw(self, screen):
        self.background.draw(screen, 'mode1')
        screen.blit(self.player.car_image, (self.car_x, self.car_y))
        super().draw(screen)
        pos_heart_x, pos_heart_y = screen.get_width() * 0.85, 20

        for i in range(self.mistakes):
            screen.blit(self.blackheart_image, (pos_heart_x + ((3-i-1) * 65),pos_heart_y))

        for i in range(3-self.mistakes):
            screen.blit(self.heart_image, (pos_heart_x + (i * 65),pos_heart_y))

        mistakes_text = self.font.render(f"Hearts: ", True, (199, 21, 133))
        screen.blit(mistakes_text, (pos_heart_x - 180, pos_heart_y))


class Mode2(Mode):
    pass
