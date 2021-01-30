import numpy as np
import time


# class issajous_figure:
#     """
#     Фигуры Лиссажу.
#     Задаётся набором точек с координатами x и y.
#     """
#
#     def __init__(self, x_array, y_array):
#         self.x_arr = x_array
#         self.y_arr = y_array


class LissajousGenerator:
    """
    Генерирует фигуры Лиссажу с заданными параметрами
    """

    def __init__(self, resolution=20):
        self._resolution = resolution

        # Эта задержка эмулирует процедуру инициализации следующей версии генератора.
        # Задержка будет убрана после обновления.
        # Пока не трогать.
        # P.S. В новом генераторе задержка будет только при инициализации.
        # Фигуры будут генерироваться так же быстро, как и сейчас.
        time.sleep(1)

    def set_resolution(self, resolution):
        """
        resolution определяет количество точек в кривой
        """
        self._resolution = resolution

    def generate_figure(self, freq_x, freq_y, phase='pi/2', a=1, b=1):
        """
        Генерирует фигуру (массивы x и y координат точек) с заданными частотами.
        """
        phi = eval('np.' + phase) if not phase.strip().replace('.', '').isnumeric() else float(phase)
        t = np.linspace(0, 2 * np.pi, self._resolution)
        x = a * np.sin(freq_x * t + phi)
        y = b * np.sin(freq_y * t)
        return x, y