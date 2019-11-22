from os.path import join


class Directory:
    RESOURCES_DIR = join("resources")

    IMAGE_DIR = join(RESOURCES_DIR, "images")
    SOUNDS_DIR = join(RESOURCES_DIR, "sounds")
    FONT_DIR = join(RESOURCES_DIR, "fonts")

    TEXTURES_DIR = IMAGE_DIR


FONT_OLD = join(Directory.FONT_DIR, "arcade-classic.ttf")
FONT_NEW = join(Directory.FONT_DIR, "bm.ttf")


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
