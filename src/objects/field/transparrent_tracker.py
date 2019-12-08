from src.objects.field.tracker import Tracker


class TransparrentTracker(Tracker):  # Нужен, чтобы проходящие сквозь стены мобы могли видеть игрока сквозь стены
    def can_walk_at(self, tile):
        return self.field_object.tile_at(tile).wallpass
