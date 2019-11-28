from time import time


def _now_time():
    return time() * 1000


class TimerObject(object):
    def __init__(self, delay, looped=False):
        """
        :param delay: время в ms
        :param looped: зациклен ли
        """
        self._delay = delay
        self._start_time = 0
        self._running = False
        self._looped = looped

    def start(self):
        self._running = True
        self._start_time = _now_time()

    def stop(self):
        self._running = False

    def on_timeout(self):
        pass

    def timer_logic(self):
        if self._running:
            if _now_time() - self._start_time >= self._delay:
                self.stop()
                if self.is_looped:
                    self.start()

                self.on_timeout()

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, delay):
        self._delay = float(delay)

    @property
    def is_running(self):
        return self._running

    @property
    def is_timeout(self):
        return not self.is_running

    @property
    def is_looped(self):
        return self._looped

    def set_looped(self, b):
        self._looped = bool(b)

    @property
    def remaining(self):
        return _now_time() - self._start_time
