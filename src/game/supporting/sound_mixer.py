from queue import Queue

import pygame


class SoundMixer:
    FREQUENCY = 44100
    SIZE = -16
    CHANNELS = 2
    BUFFER = 2048

    CHANNEL_NAMES = MUSIC_CHANNEL, EFFECTS_CHANNEL, BACKGROUND_CHANNEL = "music", "effects", "background"
    _DELAY = 10

    def __init__(self, ):
        pygame.mixer.pre_init(self.FREQUENCY, self.SIZE, self.CHANNELS, self.BUFFER)
        self._volume = 1.

    def init(self, sound_dict, channel_names=CHANNEL_NAMES):
        self._sound_dict = sound_dict
        self.channels = {name: Channel(index, self._sound_dict) for index, name in enumerate(channel_names)}

    def new_channel(self, name):
        self.channels[name] = Channel(len(self.channels), self._sound_dict)

    def process_logic(self):
        for channel in self.channels.values():
            channel.process_logic()

        pygame.time.wait(self._DELAY)

    def main_loop(self):
        while True:
            self.process_logic()

    def set_volume(self, volume):
        for channel in self.channels.values():
            channel._main_volume = volume
            channel.set_volume()


class Channel:
    def __init__(self, id, sound_dict, sound_list=(), looped=False):
        self._channel = pygame.mixer.Channel(id)
        self._sound_dict = sound_dict
        self._sound_list = list(sound_list)

        self._queue = Queue()
        for sound_name, loop in sound_list:
            self._queue.put((sound_name, loop))

        self._volume = 1
        self._main_volume = 1
        self._last_sound = None

        self._looped = looped
        self._muted = False
        self._paused = False

        self.volume = property(self.get_volume, self.set_volume)
        self.looped = property(self.is_looped, self.set_looped)
        self.muted = property(self.is_muted, self.set_mute)
        self.paused = property(self.is_paused, self.set_pause)

    def get_volume(self):
        return self._volume

    def set_volume(self, value=None):
        if value is None:
            value = self._volume
        self._volume = float(value)
        self._channel.set_volume(self._volume * (not self.is_muted()))
        if self._last_sound:
            self._last_sound.set_volume(self._main_volume)

    def is_looped(self):
        return self._looped

    def set_looped(self, b):
        self._looped = bool(b)

    def is_muted(self):
        return self._muted

    def mute(self):
        self._muted = True
        self.set_volume()

    def unmute(self):
        self._muted = False
        self.set_volume()

    def set_mute(self, b):
        self._muted = bool(b)
        self.set_volume()

    def is_paused(self):
        return self._paused

    def pause(self):
        self._channel.pause()
        self._paused = True

    def unpause(self):
        self._channel.unpause()
        self._paused = False

    def toggle_pause(self):
        if self._paused:
            self.unpause()
        else:
            self.pause()

    def set_pause(self, b):
        if bool(b):
            self.pause()
        else:
            self.unpause()

    @property
    def is_busy(self):
        return self._channel.get_busy()

    def play(self, sound_name, loops=0):
        sound = self._sound_dict[sound_name]
        sound.set_volume(self._main_volume)
        self.set_volume()
        self._last_sound = sound
        self._channel.play(sound, loops=loops)

    def sound_play(self, sound_name, loops=0):
        sound = self._sound_dict[sound_name]
        sound.set_volume(self._volume * self._main_volume)
        sound.play(loops=loops)

    def sound_stop(self, sound_name):
        sound = self._sound_dict[sound_name]
        sound.stop()
        sound.set_volume(1)

    def stop(self):
        self._channel.stop()
        del self._queue
        self._queue = Queue()

    def add_sound_to_queue(self, sound_name, loops=0):
        self._queue.put((sound_name, loops))

    def process_logic(self):
        if not self.is_busy and not self._queue.empty():
            q = self._queue.get()
            self.play(*q)
            if self.is_looped():
                self._queue.put(q)

