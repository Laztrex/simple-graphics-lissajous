import numpy as np
import os
import sys

from PyQt5 import QtCore, QtWidgets, QtTest

from termcolor import cprint

import unittest
from unittest.mock import patch, call

import lissajousgen
import main_lissajous

app = QtWidgets.QApplication(sys.argv)


class GlobalEngineTest(unittest.TestCase):

    def setUp(self):
        self.test_func = lissajousgen.LissajousGenerator()
        self.test_img = main_lissajous.LissajousWindow()
        cprint(f'Вызван {self.shortDescription()}', flush=True, color='cyan')

    def tearDown(self):
        cprint(f'Оттестировано. \n', flush=True, color='grey')

    def test_gen_sequence(self):
        """Тест генерации последовательностей"""
        self.test_func.set_resolution(10)
        self.assertEqual(self.test_func._resolution, 10)

        self.test_func.generate_figure(2, 3)
        values_1 = self.test_func.get_values()
        self.test_func.generate_figure(3, 2)
        values_2 = self.test_func.get_values()
        self.assertEqual(np.all(values_1), np.all(values_2))

        self.test_func.generate_figure(2, 3)
        values_1 = self.test_func.get_values()
        self.test_func.generate_figure(2, 3)
        values_2 = self.test_func.get_values()
        self.assertEqual(np.all(values_1), np.all(values_2))

    @patch('lissajousgen.LissajousGenerator.get_values', return_value=(1, 1))
    @patch('lissajousgen.LissajousGenerator.generate_figure')
    @patch('matplotlib.axes.Axes.plot')
    def test_form(self, mock_plt, mock_gen, mock_val):
        """Тест манипуляции с формой окна"""
        self.test_img.freq_x_lineedit.setText('3')
        self.test_img.freq_y_lineedit.setText('2')
        self.test_img.phase_lineedit.setText('1')
        self.test_img.color_combobox.setCurrentIndex(2)
        self.test_img.width_combobox.setCurrentIndex(2)

        QtTest.QTest.mouseClick(self.test_img.plot_button, QtCore.Qt.LeftButton)
        mock_gen.assert_has_calls([call(freq_x=3.0, freq_y=2.0, phase=1.0)])

        mock_plt.assert_has_calls([call(1, 1, color='crimson', linewidth=3)])


if __name__ == '__main__':
    unittest.main()
