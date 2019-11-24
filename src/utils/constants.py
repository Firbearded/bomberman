from os.path import join


class Path:
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


class Color:
    WHITE = 255, 255, 255
    LIGHT_GRAY = 200, 200, 200
    BLACK = 0, 0, 0

    RED = 255, 0, 0
    GREEN = 0, 255, 0
    BLUE = 0, 0, 255

    CYAN = 0, 255, 255
    MAGENTA = 255, 0, 255
    YELLOW = 255, 255, 0

    ORANGE = 255, 165, 0
