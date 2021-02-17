#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import time


class LissajousGenerator:
    """
    Генерирует фигуры Лиссажу с заданными параметрами
    """

    def __init__(self, resolution=500):
        self._resolution = resolution
        self.x = None
        self.y = None
        self.z = None

    def update_values(self, x, y, z):
        """
        Функция обновления массивов координат x, y.
        Введена временная задержка
        :param x: массив координат x
            :type x: numpy.ndarray
        :param y: массив координат y
            :type y: numpy.ndarray
        """

        self.x = x
        self.y = y
        self.z = z

    def get_values(self):
        """
        Возврат массивов значений координат точек x и y сгенерированной фигуры
        """
        coords = [self.x, self.y, self.z]
        return coords[:2] if self.z is None else coords

    def set_resolution(self, resolution):
        """
        Установка количества точек в кривой
        :param resolution: параметр сглаживания
            :type resolution: int
        """

        self._resolution = resolution

    def generate_figure(self, freq_x, freq_y, phase=2., a=1, b=1, mode='2d'):
        """
        Функция генерирует фигуру (массивы x и y координат точек) с заданными частотами.
        :param freq_x: Частота массива x
            :type freq_x: float
        :param freq_y: Частота массива y
            :type freq_y: float
        :param phase: Сдвиг фаз
            :type phase: float
        :param a: Амплитуда колебания x
            :type a: int
        :param b: Амплитуда колебания y
            :type b: int
        """

        dimension = {'2d': np.linspace(0, 2 * np.pi, self._resolution),
                     '3d': np.linspace(-6 * np.pi, 6 * np.pi, self._resolution)}
        phi = np.pi / phase
        t = dimension.get(mode, '2d')
        x = a * np.sin(freq_x * t + phi)
        y = b * np.sin(freq_y * t)

        self.update_values(x, y, [None, t][mode == '3d'])
