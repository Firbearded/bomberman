from time import time


def _now_time():
    return time() * 1000


class TimerObject(object):
    """ Класс объекта-таймера """
    def __init__(self, delay, looped=False):
        """
        :param delay: время в ms
        :param looped: зациклен ли
        :type delay: int
        :type looped: bool
        """
        self._delay = delay
        self._start_time = 0
        self._running = False
        self._looped = looped

    def start(self):
        """ Запустить таймер """
        self._running = True
        self._start_time = _now_time()

    def stop(self):
        """ Остановить таймер """
        self._running = False

    def on_timeout(self):
        """
        Метод, вызываемый по истечению времени на таймере.
        Его можно заменить на нужную функцию:
        some_timer = TimerObject(...)
        some_timer.on_timeout = func
        """
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
        """ Задержка таймера """
        return self._delay

    @delay.setter
    def delay(self, delay):
        self._delay = float(delay)

    @property
    def is_running(self):
        """ Активен ли таймер """
        return self._running

    @property
    def is_timeout(self):
        """ Не активен ли таймер """
        return not self.is_running

    @property
    def is_looped(self):
        """ Зациклен ли таймер """
        return self._looped

    def set_looped(self, b):
        self._looped = bool(b)

    @property
    def remaining(self):
        """ Сколько времени осталось до истечения времени """
        return _now_time() - self._start_time
