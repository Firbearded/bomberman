import pygame


class SimpleAnimation:
    """
    пример:           `cur_state`;  `cur_index` of current `animation_dict[`cur_state`][1]
    animation_dict = { 'standing': (0, (image_standing, ),
                       'walking': (200, (image_walking1, image_walking2),
                     }
    """
    def __init__(self, animation_dict, current_state):
        self.animation_dict = animation_dict
        self.current_state = current_state  # 'standing'
        self.current_index = 0              #
        self.start_time = pygame.time.get_ticks()

    @property
    def current_anim(self):
        return self.animation_dict[self.current_state]

    @property
    def current_image(self):
        return self.animation_dict[self.current_state][1][self.current_index]

    def set_state(self, key):
        if self.current_state == key:
            return
        self.current_state = key
        self.current_index = 0
        # print("ANIM {}: {}".format(self, self.current_state))

    def process_logic(self):
        delay, image_list = self.current_anim
        if delay <= 0: return
        delta_time = pygame.time.get_ticks() - self.start_time
        if delta_time >= delay:
            x = delta_time // delay
            print("ANIM {}: {} {} {}".format(self, self.current_index, x, len(image_list)))
            self.current_index = (self.current_index + x) % len(image_list)
            self.start_time += x * delay
            print("ANIM {}: next image in anim - {}".format(self, self.current_index))
            print("ANIM {}: {} {} {}".format(self, self.current_index, x, len(image_list)))
