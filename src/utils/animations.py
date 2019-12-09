from time import time


class SimpleAnimation:
    """
    Класс для анимаций.
    пример:           `cur_state`;  `cur_index` of current `animation_dict[`cur_state`][1]
    animation_dict = { 'standing': (0, (image_standing, ),
                       'walking': (200, (image_walking1, image_walking2),
                     }
    """
    def __init__(self, animation_dict, current_state):
        self.animation_dict = animation_dict
        self.current_state = current_state
        self.current_index = 0
        self.start_time = time() * 1000

    @property
    def current_animation(self):
        return self.animation_dict[self.current_state]

    @property
    def current_image(self):
        return self.animation_dict[self.current_state][1][self.current_index]

    @property
    def current_delay(self):
        return self.animation_dict[self.current_state][0]

    @property
    def current_length(self):
        return len(self.animation_dict[self.current_state][1])

    def set_state(self, key):
        if self.current_state == key:
            return
        self.current_state = key
        self.current_index = 0

    def process_logic(self):
        delay, image_list = self.current_animation
        if delay <= 0: return
        delta_time = time() * 1000 - self.start_time
        if delta_time >= delay:
            x = int(delta_time // delay)
            self.current_index = (self.current_index + x) % len(image_list)
            self.start_time += x * delay
