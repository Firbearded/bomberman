from src.game import Game


def main(*args, **kwargs):
    g = Game(*args, **kwargs)
    g.main_loop()


if __name__ == '__main__':
    main()
