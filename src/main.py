from src.objects.game import Game
from src.utils.vector import Point
from src.objects.field import Field


def main():
    g = Game()

    o = g.objects
    o.append(Field(g, Point(0, 0), (19, 13), (32, 32)))

    g.main_loop()


if __name__ == '__main__':
    main()
