from src.scenes.base_scene import Scene


class MenuScene(Scene):
    def additional_logic(self):
        self.game.set_scene(self.game.GAME_SCENE_INDEX)
