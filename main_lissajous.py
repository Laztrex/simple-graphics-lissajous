#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

import PyQt5.QtWidgets as Qt
from PyQt5 import uic, QtGui, QtCore

from lissajousgen import LissajousGenerator


def validation_form(form):
    """
    Функция валидации входных параметров.
    Проверка проводится с помощью регулярных выражений и класса QRegExpValidator
    :param form: Экземпляр основного класса LissajousWindow
        :type form: LissajousWindow object
    """
    reg_ex_lineedit = QtCore.QRegExp("^[1-9]{1,2}[0]$.[1-9]{1,2}$")
    reg_ex_phase = QtCore.QRegExp(r"^[1-9]{1,2}[0]")

    freq_x_validator = QtGui.QRegExpValidator(reg_ex_lineedit, form.freq_x_lineedit)
    freq_y_validator = QtGui.QRegExpValidator(reg_ex_lineedit, form.freq_y_lineedit)
    phase_validator = QtGui.QRegExpValidator(reg_ex_phase, form.phase_lineedit)

    form.freq_x_lineedit.setValidator(freq_x_validator)
    form.freq_y_lineedit.setValidator(freq_y_validator)
    form.phase_lineedit.setValidator(phase_validator)


def check_paths():
    """
    Проверка рекомендуемо-необходимых директорий
    """
    os.makedirs(os.path.normpath(os.path.dirname(__file__) + '/files/pics'), exist_ok=True)
    os.makedirs(os.path.normpath(os.path.dirname(__file__) + '/files/presets'), exist_ok=True)


class LissajousWindow(Qt.QMainWindow):
    """
    Python 3.7.5

    Основной класс Qt-style формы приложения для построения фигур Лиссажу.
    Проект будет дополняться в глубину (3D, анимации) и в ширину (новые параметры взаимодействия с интерфейсом)

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            from settings import SETTINGS_MPL
        except:
            msg = Qt.QMessageBox()
            msg.setIcon(Qt.QMessageBox.Critical)
            msg.setText('Не найден файл настроек!')
            msg.exec_()
            sys.exit('File with settings was deleted!')

        self.settings = SETTINGS_MPL
        check_paths()

        self.init_ui()

        self.generator = LissajousGenerator()

        self._fig = plt.Figure(figsize=(6, 5), dpi=100)
        self._ax = self._fig.add_subplot(1, 1, 1)

        self._fc = FigureCanvas(self._fig)
        layout = Qt.QVBoxLayout(self.groupBox)
        layout.addWidget(self._fc)

        self.plot_lissajous_figure()

    def init_ui(self):
        self.setStyleSheet("QLineEdit { border: 1px solid; border-color:#dcdcdc; border-radius: 4px;} "
                           "QLineEdit:focus{border:1px solid gray; }")

        uic.loadUi(self.settings["paths"]["ui"], self)
        validation_form(self)

        self.setWindowTitle(self.settings["message"].format(self.settings["version"]))

        self.setWindowIcon(QtGui.QIcon(self.settings["paths"]["icon"]["main"]))

        self.plot_button.clicked.connect(self.plot_button_click_handler)
        self.save_button.clicked.connect(self.save_image_button_handler)
        self.proportion_button.clicked.connect(self.proportion_ratio_click_handler)
        self.radio_grid.clicked.connect(self.plot_radio_grid_handler)
        self.save_json_button.clicked.connect(self.save_json_button_handler)
        self.load_json_button.clicked.connect(self.load_file_handler)

    def plot_button_click_handler(self):
        """
        Функция обработки нажатия кнопки «Обновить фигуру».
        Запускает процесс генерации фигуры после валидации входных данных
        """
        validation_form(self)
        settings = self.get_settings()
        self.plot_lissajous_figure(settings)

    def plot_radio_grid_handler(self):
        """
        Функция обработки нажатия свитча «Сетка». Включает в отображение сетку и нумерацию осей
        """
        if self.radio_grid.isChecked():
            self._ax.grid(True)
        else:
            self._ax.grid(False)
        self.plot_lissajous_figure()

    def get_settings(self, params=True):
        """
        Функция возвращает словарь параметров согласно флагу params
        :param params: Флаг категории параметров
            :type params: bool
        :return: dict, параметры фигуры, если params=True, иначе - параметры отображения
        """
        return {
            "freq_x": float(self.freq_x_lineedit.text()),
            "freq_y": float(self.freq_y_lineedit.text()),
            "phase": float(self.phase_lineedit.text()),
        } if params \
            else {"color": self.settings["color_map"].get(self.color_combobox.currentText(), 'Синий'),
                  "linewidth": int(self.width_combobox.currentText())}

    def plot_lissajous_figure(self, settings=None):
        """
        Функция отрисовки фигуры
        :param settings: словарь с параметрами фигуры
            :type settings: dict
        """
        if settings is None:
            settings = self.get_settings()

        for line in self._ax.lines:
            line.remove()

        self.generator.generate_figure(**settings)
        x_arr, y_arr = self.generator.get_values()
        self._ax.plot(x_arr, y_arr,
                      **self.get_settings(params=False))

        self.check_grid_is_checked(x_arr, y_arr)

        plt.tight_layout()

        self._fc.draw()

    def check_grid_is_checked(self, x, y):
        """
        Проверка флага включения сетки на графике
        :param x: Массив координат
            :type x: numpy.ndarray
        :param y: Массив координат
            :type y: numpy.ndarray
        """
        if self.radio_grid.isChecked():
            self._ax.axis("on")
            self._ax.set_xlim(min(x), max(x))
            self._ax.set_ylim(min(y), max(y))
        else:
            self._ax.axis("off")

    def files_handler(self, mode='save', img=True):
        """
        Функция-помощник для манипуляциями с файлами. Сохранение/Открытие файла
        :param mode: флаг обработки. 'save' - Сохранение, 'load' (или пока любой другой) - Загрузка
            :type mode: str
        :param img: Флаг сохранения настроек/картинки
            :type img: bool
        :return: Если путь не найден - None
                 Иначе - директория файла
        """
        if mode == 'save':
            file_path, _ = Qt.QFileDialog.getSaveFileName(*self.settings["dirs"][["settings", "images"][img]])
        else:
            file_path, _ = Qt.QFileDialog.getOpenFileName(*self.settings["dirs"]["settings"])

        if not file_path:
            return

        return file_path

    def load_file_handler(self):
        """
        Функция обработки нажатия кнопки «Загрузить настройки»
        По умолчанию директория указана в settings.py (settings_mpl["paths"]["files"])
        """
        path_to_file = self.files_handler(mode='load')
        if path_to_file:
            with open(path_to_file, 'r', encoding='utf-8') as open_file:
                loaded_settings = json.load(open_file)
            self.write_line_edit(loaded_settings)

    def write_line_edit(self, data):
        """
        Функция записи настроек с загруженного файла. На стеке - над «load_file_handler»
        :param data: словарь с ключами "freq_x", "freq_y", "phase"
            :type data: dict
        """
        self.freq_x_lineedit.setText(str(int(data.get("freq_x", '3'))))
        self.freq_y_lineedit.setText(str(int(data.get("freq_y", '2'))))
        self.phase_lineedit.setText(str(int(data.get("phase", '2'))))

        index = self.color_combobox.findText(data.get("color", 'Синий'), QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.color_combobox.setCurrentIndex(index)

        index = self.width_combobox.findText(str(data.get("linewidth", '2')), QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.width_combobox.setCurrentIndex(index)

        self.plot_lissajous_figure()

    def proportion_ratio_click_handler(self):
        """
        Функция обработки нажатия кнопки «Выровнять»
        Выравнивание соотношения сторон 4к3
        """
        h = min(self.height(), self.width())
        self.resize(h + 280, h)

    def save_image_button_handler(self):
        """
        Функция обработки нажатия кнопки «Сохранить фигуру в файл»
        Путь к файлу указан в settings.py (settings_mpl["dirs"]["images"])
        """
        path = self.files_handler()
        if path:
            self._fig.savefig(path)

    def save_json_button_handler(self):
        """
        Функция обработки нажатия кнопки «Сохранить настройки»
        Путь к файлу указан в settings.py (settings_mpl["dirs"]["settings"])
        """
        path = self.files_handler(img=False)
        if path:
            d = self.get_settings(params=True)
            d.update(self.get_settings(params=False))
            with open(path, 'w') as write_file:
                json.dump(d, write_file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)

    main_window = LissajousWindow()

    main_window.show()

    app.exec_()
