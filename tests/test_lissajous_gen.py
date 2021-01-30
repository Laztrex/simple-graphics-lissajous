from termcolor import cprint
import unittest
from math import asin, pi

from main import LissajousWindow
from lissajousgen import LissajousGenerator


class GlobalEngineTest(unittest.TestCase):
    def setUp(self):
        self.test_func = LissajousGenerator()

    def tearDown(self):
        cprint(f'Оттестировано. \n', flush=True, color='grey')

    def test_gen_sequence(self):
        self.test_func.set_resolution(500)
        self.assertEqual(self.test_func._resolution, 500)

        out_x, out_y = self.test_func.generate_figure(1, 2)
        print(asin(out_x[2] - out_x[1]))

    def test_save_img(self):
        pass

    def test_validate_form(self):
        pass
