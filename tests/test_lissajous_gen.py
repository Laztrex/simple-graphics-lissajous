import unittest

class GlobalEngineTest(unittest.TestCase):
    def setUp(self):
        self.get_weather_test = \
            ImageMaker(city='Ставрополь')
        cprint(f'Вызван {self.shortDescription()}', flush=True, color='cyan')

    def tearDown(self):
        cprint(f'Оттестировано. \n', flush=True, color='grey')
