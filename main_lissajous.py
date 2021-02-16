#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import sys

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d.axes3d import Axes3D

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


class MplCanvas(FigureCanvas):

    def __init__(self, canvas_fig=None, mode=None, width=5, height=4, dpi=100):
        fig = plt.Figure(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(fig)
        if canvas_fig:
            canvas_fig.figure.clf()
            canvas_fig.axes = canvas_fig.figure.add_subplot(111, projection=mode)
            if mode is not None:
                canvas_fig.axes.get_proj = lambda: np.dot(Axes3D.get_proj(canvas_fig.axes),
                                                          np.diag([1.2, 1.2, 1.2, 1]))
            self.axes = canvas_fig.axes
        else:
            self.axes = fig.add_subplot(111)

        if canvas_fig and isinstance(canvas_fig.axes, Axes3D):
            canvas_fig.axes.mouse_init()


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

        self._fig = MplCanvas()

        # toolbar = NavigationToolbar(self._fig, self)
        layout = Qt.QVBoxLayout(self.groupBox)
        # layout.addWidget(toolbar)
        layout.addWidget(self._fig)
        self.generator = LissajousGenerator()

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
        self.radio_grid.clicked.connect(self.plot_lissajous_figure)
        self.checkBox_3D.clicked.connect(self.update_plt)
        self.save_json_button.clicked.connect(self.save_json_button_handler)
        self.load_json_button.clicked.connect(self.load_file_handler)

    def update_plt(self):
        if self.checkBox_3D.isChecked():
            MplCanvas(self._fig, mode='3d')
        else:
            MplCanvas(self._fig)

        self.plot_lissajous_figure()

    def plot_button_click_handler(self):
        """
        Функция обработки нажатия кнопки «Обновить фигуру».
        Запускает процесс генерации фигуры после валидации входных данных
        """

        validation_form(self)
        settings = self.get_settings()
        self.plot_lissajous_figure(settings)

    def plot_radio_grid_func(self):
        """
        Функция проверки свитча «Сетка». Включает в отображение сетку и нумерацию осей
        """
        if self.radio_grid.isChecked():
            self._fig.axes.grid(b=True, color='b', linestyle='-')
        else:
            self._fig.axes.grid(b=False)

    def get_settings(self, params=True, dict_val=1):
        """
        Функция возвращает словарь параметров согласно флагу params
        :param params: Флаг категории параметров
            :type params: bool
        :param dict_val: 1 - вернуть значение словаря из settings, 0 - вернуть значение combobox
        :return: dict, параметры фигуры, если params=True, иначе - параметры отображения
        """

        return {
            "freq_x": float(self.freq_x_lineedit.text()),
            "freq_y": float(self.freq_y_lineedit.text()),
            "phase": float(self.phase_lineedit.text()),
        } if params \
            else {"color": [self.color_combobox.currentText(),
                            self.settings["color_map"].get(self.color_combobox.currentText(), 'Синий')][dict_val],
                  "linewidth": int(self.width_combobox.currentText())}

    def plot_lissajous_figure(self, settings=None):
        """
        Функция отрисовки фигуры
        :param settings: словарь с параметрами фигуры
            :type settings: dict
        """

        if not isinstance(settings, dict):
            settings = self.get_settings()

        self._fig.axes.lines.clear()

        if self.checkBox_3D.isChecked():
            self.generator.generate_figure(**settings, mode='3d')
        else:
            self.generator.generate_figure(**settings)

        values = self.generator.get_values()
        self._fig.axes.plot(*values,
                            **self.get_settings(params=False))

        self.plot_radio_grid_func()
        self.check_grid_is_checked(*values)

        self._fig.axes.figure.tight_layout()

        self._fig.draw()

    def check_grid_is_checked(self, x, y, z=None):
        """
        Проверка флага включения сетки на графике
        :param x: Массив координат
            :type x: numpy.ndarray
        :param y: Массив координат
            :type y: numpy.ndarray
        """
        if self.radio_grid.isChecked():
            self._fig.axes.axis("on")
            # self._fig.axes.set_xlabel('X Label')
            # self._fig.axes.set_ylabel('Y Label')
            self._fig.axes.set_xlim(min(x), max(x))
            self._fig.axes.set_ylim(min(y), max(y))
            if z is not None:
                # self._fig.axes.set_zlabel('Z Label')
                self._fig.axes.set_zlim(min(z), max(z))
        else:
            self._fig.axes.axis("off")

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
            d.update(self.get_settings(params=False, dict_val=0))
            with open(path, 'w', encoding='utf-8') as write_file:
                json.dump(d, write_file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)

    main_window = LissajousWindow()

    main_window.show()

    app.exec_()
