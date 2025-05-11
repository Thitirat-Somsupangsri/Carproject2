import pygame as pg
from player import Player, Bot, PlayerDataManager
from config import Config
from event import Mode1, Mode2
from sfx import SoundEffects
from tkinter import *
from tkinter import ttk
import time

class Game:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((1300, 850))
        self.bg = Config()
        self.__screen_width = self.bg.screen_width
        self.__screen_height = self.bg.screen_height
        pg.display.set_caption("Car Racing and Spelling Game")
        self.font = pg.font.Font("game_assets/Grand9K Pixel.ttf", 46)
        self.clock = pg.time.Clock()
        self.car_images = [pg.image.load(f"game_assets/Cars/Car{i}.png").convert_alpha() for i in range(1, 10)]
        self.player = Player(name="Player 1", car_image=self.car_images)
        self.mode = None
        self.mode_num = None
        self.running = True
        self.game_started = False
        self.game_over = False

    def enter_name(self):
        box_width = int(self.__screen_width * 0.5)
        box_height = int(self.__screen_height * 0.08)
        box_x = (self.__screen_width - box_width) // 2
        box_y = (self.__screen_height - box_height) // 2
        input_box = pg.Rect(box_x, box_y, box_width, box_height)

        color_inactive = pg.Color((235, 235, 235))
        color_active = pg.Color((175, 238, 238))
        color = color_inactive
        active = False
        text = ''
        cursor_show = True
        cursor = 0

        while True:
            self.bg.draw(self.screen, 'intro')
            pg.draw.rect(self.screen, color, input_box)
            pg.draw.rect(self.screen, (54, 69, 79), input_box, width=2)

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

            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return None

                if event.type == pg.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = True
                        color = color_active
                    else:
                        active = False
                        color = color_inactive

                if event.type == pg.KEYDOWN:
                    if active:
                        if event.key == pg.K_RETURN and text.strip():
                            return text.strip()
                        elif event.key == pg.K_BACKSPACE:
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
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return None
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        self.mode_num = 1
                        return 1
                    elif event.key == pg.K_2:
                        self.mode_num = 2
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

            pg.display.flip()
            self.clock.tick(30)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            else:
                self.mode.event(event)

    def game_over_screen(self):
        self.screen.fill((52, 73, 94))
        if self.mode_num == 1:
            self.display_text('Game Over', 350, 250)
            self.display_text(f'Score: {self.player.score}', 350, 300)
        elif self.mode_num == 2:
            if self.mode.winner is not None:
                self.display_text(f'{self.mode.winner} win !' , 350, 300)
            else:
                self.display_text(f"It's a tie !", 350, 300)
        self.display_text('Press R to Restart', 350, 400)
        self.display_text('Press Q to Exit', 350, 460)
        pg.display.flip()
        waiting = True
        while waiting is True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.run('restart')
                        return
                    if event.key == pg.K_q:
                        self.running = False
                        waiting = False

    def run(self,status='new'):
        if status == 'new':
            SoundEffects.get_instance().play("started")
            player_name, selected_mode = self.enter_name(), self.game_mode()
            self.player.name = player_name

        else:
            self.player.reset_player()
            selected_mode = self.game_mode()
        manager = PlayerDataManager()

        if str(self.player.name) in [str(key) for key in manager.data]:
            self.player.hint_left = int(PlayerDataManager().get_data(self.player.name, 'hints'))
            print(self.player.hint_left)
        else:
            self.player.hint_left = 0

        if selected_mode == 1:
            self.mode = Mode1(self.player, self.font, self.bg)
        elif selected_mode == 2:
            bot = Bot(name="Bot", car_image=self.car_images)
            self.mode = Mode2(self.player, bot, self.font, self.bg)

        self.start_game()
        self.game_over_screen()


class GameLauncher:
    def __init__(self, game):
        self.game = game
        self.game.grid_columnconfigure(0, weight=1)

        self.start_button = Button(self.game, text="Start Game", command=self.start_game,font=("Arial", 20))
        self.start_button.grid(row=1,sticky= 'nsew')

        self.leaderboard_button = Button(self.game, text="Leaderboard", command=self.show_leaderboard,font=("Arial", 20))
        self.leaderboard_button.grid(row=2,sticky= 'nsew')

    def start_game(self):
        self.game.destroy()
        game = Game()
        game.run()
        pg.quit()

    def show_leaderboard(self):
        leaderboard_window = Toplevel(self.game)
        leaderboard_window.title("Leaderboard")
        leaderboard_window.geometry("1000x400")
        manager = PlayerDataManager()
        tree = ttk.Treeview(leaderboard_window, columns=("Player", "Played Count Mode1", "Best Score Mode1",
                                                         "Avg Time Mode1", "Played Count Mode2",
                                                         "Total Wins Mode2", "Hints", "Highest Streak"),
                            show="headings")

        tree.heading("Player", text="Player")
        tree.heading("Played Count Mode1", text="Played Count Mode1")
        tree.heading("Best Score Mode1", text="Best Score Mode1")
        tree.heading("Avg Time Mode1", text="Avg Time Mode1")
        tree.heading("Played Count Mode2", text="Played Count Mode2")
        tree.heading("Total Wins Mode2", text="Total Wins Mode2")
        tree.heading("Hints", text="Hints")
        tree.heading("Highest Streak", text="Highest Streak")

        tree.column("Player", width=100, anchor="w")
        tree.column("Played Count Mode1", width=80, anchor="center")
        tree.column("Best Score Mode1", width=80, anchor="center")
        tree.column("Avg Time Mode1", width=80, anchor="center")
        tree.column("Played Count Mode2", width=80, anchor="center")
        tree.column("Total Wins Mode2", width=80, anchor="center")
        tree.column("Hints", width=80, anchor="center")
        tree.column("Highest Streak", width=80, anchor="center")

        sorted_players = manager.get_sorted_players()

        for username, stats in sorted_players[:5]:
            tree.insert("", "end", values=(username,
                                           stats['played count in mode1'],
                                           stats['best score in mode1'],
                                           stats['average time played in mode1'],
                                           stats['played count in mode2'],
                                           stats['total wins in mode2'],
                                           stats['hints'],
                                           stats['highest streak']))

        tree.pack(fill=BOTH, expand=True)


if __name__ == "__main__":
    root = Tk()
    root.title("Game Launcher")
    root.geometry(f"300x400")
    root.resizable(False, False)
    game = GameLauncher(root)
    root.mainloop()
