import os
import sys
import matplotlib
from termcolor import cprint
import unittest
from math import asin, pi
from unittest.mock import patch
import lissajousgen
from PyQt5 import QtCore, QtWidgets, QtTest

from main import LissajousWindow
from lissajousgen import LissajousGenerator

app = QtWidgets.QApplication(sys.argv)


# [os.path.join(*os.getcwd().split('\\')[:-1])]

def opa(x, y, *args, **kwargs):
    print(x, y)


class GlobalEngineTest(unittest.TestCase):
    def setUp(self):
        self.test_func = LissajousGenerator()
        self.test_img = LissajousWindow()

    def tearDown(self):
        cprint(f'Оттестировано. \n', flush=True, color='grey')

    def test_gen_sequence(self):
        self.test_func.set_resolution(500)
        self.assertEqual(self.test_func._resolution, 500)

        out_x, out_y = self.test_func.generate_figure(3, 2)
        print(asin(out_x[2] - out_x[1]))

    @patch('lissajousgen.LissajousGenerator.generate_figure', return_value=(1, 1))
    @patch('matplotlib.axes.Axes.plot', side_effect=opa)
    def test_save_img(self, mock_plt, mock_gen):
        self.test_img.freq_x_lineedit.setText('3')
        self.test_img.freq_y_lineedit.setText('2')
        self.test_img.phase_lineedit.setText('pi/2')
        self.test_img.color_combobox.setCurrentIndex(2)
        self.test_img.width_combobox.setCurrentIndex(2)
        #
        QtTest.QTest.mouseClick(self.test_img.plot_button, QtCore.Qt.LeftButton)
        print(mock_gen)
        pass


    def test_validate_form(self):
        pass
