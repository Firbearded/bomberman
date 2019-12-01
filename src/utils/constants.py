from os.path import join


class Path:
    """ Класс с константами. Тут хранятся пути до папок и файлов """
    RESOURCES_DIR = join("resources")

    IMAGE_DIR = join(RESOURCES_DIR, "images")
    TEXTURES_DIR = IMAGE_DIR

    SOUNDS_DIR = join(RESOURCES_DIR, "sounds")

    FONT_DIR = join(RESOURCES_DIR, "fonts")
    FONT_OLD = join(FONT_DIR, "arcade-classic.ttf")
    FONT_NEW = join(FONT_DIR, "bm.ttf")
    FONT = FONT_OLD

    SAVE_DIR = join(RESOURCES_DIR, "savedata")

    STAGE_SAVE = join(SAVE_DIR, 'stage.sav')
    HIGHSCORES_SAVE = join(SAVE_DIR, 'highscores.sav')
    SETTINGS_SAVE = join(SAVE_DIR, 'settings.ini')


class Color:
    """ Класс с константами цветов """
    WHITE = 255, 255, 255
    LIGHT_GREY = 192, 192, 192
    GREY = 128, 128, 128
    DARK_GREY = 64, 64, 64
    BLACK = 0, 0, 0

    MAROON = 128, 0, 0
    RED = 255, 0, 0
    PINK = 250, 190, 190

    BROWN = 170, 110, 40
    ORANGE = 245, 130, 48
    APRICOT = 255, 215, 180

    OLIVE = 128, 128, 0
    YELLOW = 255, 255, 25
    BEIGE = 255, 250, 200

    LIME = 210, 245, 60
    GREEN = 60, 180, 75
    MINT = 170, 255, 195

    TEAL = 0, 128, 128
    CYAN = 70, 240, 240

    NAVY = 0, 0, 128
    BLUE = 0, 130, 200

    PURPLE = 145, 30, 180
    LAVENDER = 230, 190, 255

    MAGENTA = 240, 50, 230

    @staticmethod
    def random_color():
        """ Получить случайный цвет из тех, что выше """
        from random import choice
        d = Color.__dict__
        return d[choice([key for key in d.keys() if key[:1].isupper()])]

    @staticmethod
    def full_random_color():
        """ Получить вообще случайный цвет """
        from random import randint
        return randint(0, 255), randint(0, 255), randint(0, 255)

    @staticmethod
    def byte_to_share(color):
        """
        Перевод восьмибитных цветов в доли.
        128, 255, 255 -> 0.5, 1, 1
        """
        r, g, b = color
        return r / 255, g / 255, b / 255
