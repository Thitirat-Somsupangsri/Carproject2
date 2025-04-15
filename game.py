import pygame
from player import Player,Bot
from config import Config
from event import Mode1, Mode2


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1300,850))
        self.bg = Config()
        self.__screen_width = self.bg.screen_width
        self.__screen_height = self.bg.screen_height
        pygame.display.set_caption("Car Racing and Spelling Game")
        self.font = pygame.font.Font("game_assets/Grand9K Pixel.ttf", 46)
        self.clock = pygame.time.Clock()
        self.car_images = [pygame.image.load(f"game_assets/Cars/Car{i}.png").convert_alpha() for i in range(1, 10)]
        self.player = Player(name="Player 1", car_image=self.car_images)
        self.mode = None
        self.running = True
        self.game_started = False
        self.game_over = False

    def enter_name(self):
        box_width = int(self.__screen_width * 0.5)
        box_height = int(self.__screen_height * 0.08)
        box_x = (self.__screen_width - box_width) // 2
        box_y = (self.__screen_height - box_height) // 2
        input_box = pygame.Rect(box_x, box_y, box_width, box_height)

        color_inactive = pygame.Color((235, 235, 235))
        color_active = pygame.Color((175, 238, 238))
        color = color_inactive
        active = False
        text = ''
        cursor_show = True
        cursor = 0

        while True:
            self.bg.draw(self.screen, 'intro')
            pygame.draw.rect(self.screen, color, input_box)
            pygame.draw.rect(self.screen, (54, 69, 79), input_box, width=2)

            cursor += 1
            if cursor >= 30:
                cursor_show = not cursor_show
                cursor = 0

            display_text = text
            if active and cursor_show:
                display_text += "|"

            txt_surface = self.font.render(display_text, True, (0, 0, 0))
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            self.display_text("Enter player name:", box_x, box_y - 100)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = True
                        color = color_active
                    else:
                        active = False
                        color = color_inactive

                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN and text.strip():
                            return text.strip()
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
            self.clock.tick(60)

    def game_mode(self):
        while True:
            self.bg.draw(self.screen, 'intro')
            self.display_text("Choose Mode:", 100, 200)
            self.display_text("Press 1: Mode 1 (Survival)", 100, 300)
            self.display_text("Press 2: Mode 2 (Race with Bot)", 100, 360)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 1
                    elif event.key == pygame.K_2:
                        return 2

            self.clock.tick(60)

    def display_text(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))

    def start_game(self):
        self.game_started = True
        self.game_over = False

        while self.running and self.mode.running:
            delta_time = self.clock.get_time() / 1000.0

            self.mode.draw(self.screen)
            self.handle_events()
            self.mode.update(delta_time)

            pygame.display.flip()
            self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.mode.event(event)

    def game_over_screen(self):
        self.screen.fill((0, 0, 0))
        self.display_text("Game Over", 350, 250)
        self.display_text(f"Score: {self.player.score}", 350, 300)
        if self.mode == 2:
            self.display_text("", 350, 300)
        pygame.display.flip()
        pygame.time.wait(2000)

    def run(self):
        player_name, selected_mode = self.enter_name(), self.game_mode()
        if player_name and selected_mode:
            self.player.name = player_name

            if selected_mode == 1:
                self.mode = Mode1(self.player, self.font, self.bg)
                print(self.mode)
            elif selected_mode == 2:
                bot = Bot(name="Bot", car_image=self.car_images)
                self.mode = Mode2(self.player, bot, self.font, self.bg)

        self.start_game()
        self.game_over_screen()


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
