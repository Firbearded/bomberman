from src.objects.base_classes.base_objects.timer_object import TimerObject
from src.objects.base_classes.entity import Entity
from src.objects.field.tiles import CATEGORY, TILES
from src.objects.supporting.animation import SimpleAnimation
from src.utils.decorators import protect
from src.utils.vector import Point


class BreakingWall(Entity, TimerObject):
    """
    Сущность уничтожающейся стены.
    Нужна для анимации разрушения.
    """
    SPRITE_CATEGORY = CATEGORY
    SPRITE_NAMES = ('break_wall', 'break_wall1', 'break_wall2', 'break_wall3')
    COLOR = TILES[2].color

    def __init__(self, field_object, pos: Point, delay):
        from src.objects.field.field_class import Field

        Entity.__init__(self, field_object, round(pos))
        TimerObject.__init__(self, delay)
        self.field_object.tile_set(pos, Field.TILE_UNREACHABLE_EMPTY)  # Ставим под себя невидимую стену

        self.animation = self.create_animation()
        self.start()

    @protect
    def create_animation(self):
        if not self.game_object.images: return

        sprites = [self.field_object.tile_images[i] for i in BreakingWall.SPRITE_NAMES]
        animation_delay = int(self.delay / len(sprites))
        animation_dict = {'standard': (animation_delay, sprites)}
        return SimpleAnimation(animation_dict, 'standard')

    def on_timeout(self):
        from src.objects.field.field_class import Field

        self.field_object.tile_set(self.pos, Field.TILE_EMPTY)  # Когда время выходит, то убираем невидимую клетку
        self.field_object.try_drop_item(self.pos)               # Пытаемся дропнуть вещь
        self.field_object._soft_number -= 1                     # Уменьшаем количество ломаемых стен

        self.destroy()

    def additional_logic(self):
        self.timer_logic()
