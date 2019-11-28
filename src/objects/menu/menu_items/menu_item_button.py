import pygame

from src.objects.menu.menu_items.menu_item_selectable_label import MenuItemSelectableLabel


class MenuItemButton(MenuItemSelectableLabel):
    KEYS_PRESS = (pygame.K_SPACE, pygame.K_RETURN)

    def __init__(self, game_object, text_object, selected_text_wrapper="{}", selected_color=None, func=None):
        super().__init__(game_object, text_object, selected_text_wrapper, selected_color)

        self.on_press = func

    def press(self):
        if self.on_press:
            self.on_press()

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.KEYS_PRESS:
                self.press()
                return
