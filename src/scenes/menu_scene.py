from src.scenes.base_scene import Scene
from src.objects.menu import MenuItem
from src.objects.menu import Menu
from src.objects.text import Text
from src.utils.constants import Color


class MenuScene(Scene):

    def additional_logic(self):
        items = create_menu_items()
        #self.game.set_scene(self.game.GAME_SCENE_INDEX)
        menu = Menu(Scene.game, (0, 0), items)

    def create_menu_items(self):
        items = []
        #start
        text1 = MenuItem(Text(Scene.game, (0,0), 'Start', None, 20, Color.WHITE, True))
        text2 = MenuItem(Text(Scene.game, (0,0), 'Start', None, 20, Color.RED, True))
        items.append(MenuItem(text1, text2))
        #Exit
        text1 = MenuItem(Text(Scene.game,(0,0), 'Exit', None, 20, Color.WHITE, True))
        text2 = MenuItem(Text(Scene.game,(0,0), 'Exit', None, 20, Color.RED, True))
        items.append(MenuItem(text1, text2))
        return items

