from src.game.entities.enemies import ENEMIES as ENEMY_LIST
from src.game.entities.items import DROP_LIST


class Stage:
    """
    Класс для хранения уровней.
    """
    FIELD_SIZE = 31, 13
    NAME = "Untitled stage"
    ENEMIES = tuple([0 for _ in range(len(ENEMY_LIST))])
    UPGRADES = tuple([0 for _ in range(len(DROP_LIST))])
    SOFT_WALL_NUMBER = 60
    TIME = 200
    ON_TIMEOUT = (0, 0, 0, 0, 0, 0, 0, 15)  # -> после окончания времени появится `карательный отряд`

    def __init__(self,
                 field_size=FIELD_SIZE,
                 name=NAME,
                 soft_wall_number=SOFT_WALL_NUMBER,
                 enemies=ENEMIES,
                 upgrades=UPGRADES,
                 time=TIME,
                 on_timeout=ON_TIMEOUT):
        """
        :param field_size: Размер поля уровня
        :param name: Название уровня
        :param soft_wall_number: Количество разрушаемых блоков
        :param enemies: Кортеж с числом врагов каждого типа
        :param upgrades: Кортеж с числом выпадаемых предметов каждого типа
        :param time: Время на уровень
        :param on_timeout: Враги, которые появятся после окончания уровня
        """
        self.field_size = tuple(field_size)
        self.name = name
        self.soft_wall_number = soft_wall_number
        self.enemies = tuple(enemies)  # смотреть -> src.game.enemies.ENEMIES
        if len(self.enemies) < len(ENEMY_LIST):
            self.enemies = self.enemies + tuple([0 for _ in range(len(ENEMY_LIST) - len(self.enemies))])
        self.upgrades = upgrades
        if len(self.upgrades) < len(DROP_LIST):
            self.upgrades = self.upgrades + tuple([0 for _ in range(len(DROP_LIST) - len(self.upgrades))])
        self.time = time
        self.enemies_on_timeout = tuple(on_timeout)

    # @property
    # def save_str(self):
    #     s = "{sz[0]} {sz[1]}\n" \
    #         "{name}\n" \
    #         "{swn}\n" \
    #         "{enemies}\n" \
    #         "{un}\n" \
    #         "{time}\n" \
    #         "{ot}\n".format(
    #         sz=self.field_size,
    #         name=self.name,
    #         swn=self.soft_wall_number,
    #         enemies=' '.join(map(str, self.enemies)),
    #         un=self.upgrades_number,
    #         time=self.time,
    #         ot=' '.join(map(str, self.enemies_on_timeout)),
    #     )
    #     return s

    # def save(self, file_path):
    #     if not os.path.exists(file_path):
    #         os.makedirs(os.path.dirname(file_path))
    #     with open(file_path, 'w') as f:
    #         f.write(self.save_str)
    #
    # @classmethod
    # def load(cls, file_path):
    #     with open(file_path, 'r') as f:
    #         lines = [line.strip() for line in f.readlines()]
    #
    #     size, name, swn, enemies, un, time, ot = lines
    #     size = tuple(map(int, size.split()))
    #     swn = int(swn)
    #     enemies = tuple(map(int, enemies.split()))
    #     un = int(un)
    #     time = int(time)
    #     ot = tuple(map(int, ot.split()))
    #
    #     return Stage(size, name, swn, enemies, un, time, ot)
