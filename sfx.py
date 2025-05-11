import pygame as pg


class SoundEffects:
    __instance = None

    def __init__(self):
        if SoundEffects.__instance == None:
            pg.mixer.init(frequency=44100, channels=2)
            self.__instance = self
            print("Sound effects initialized")
            self.__effects = {"move": pg.mixer.Sound('game_assets/sfx/car-engine-335601.mp3'),
                              "typing": pg.mixer.Sound('game_assets/sfx/keyboard-typing-one-short-1-292590.mp3'),
                              "beep": pg.mixer.Sound('game_assets/sfx/negative_beeps-6008.mp3'),
                              "clicked": pg.mixer.Sound('game_assets/sfx/beep-329314.mp3'),
                              "started": pg.mixer.Sound('game_assets/sfx/car-engine-start-44357.mp3')
                              }

        else:
            raise Exception()

    @staticmethod
    def get_instance():
        if SoundEffects.__instance == None:
            SoundEffects.__instance = SoundEffects()
        return SoundEffects.__instance

    def play(self, effect):
        if effect in self.__effects:
            self.__effects[effect].play()
