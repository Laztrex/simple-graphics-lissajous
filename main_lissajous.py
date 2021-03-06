#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import sys

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import rcParams
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

    reg_ex_lineedit = QtCore.QRegExp("^([0-9]{1,2})[.]([0-9]{1,5})?$")

    reg_ex_phase = QtCore.QRegExp(r"^([0-9]{1,2})[.]([0-9]{1,5})\s?"
                                  r"([0-9]{1,2})[.]([0-9]{1,5})\s?")

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

    os.makedirs(os.path.join(os.path.dirname(__file__), 'files', 'pics'), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'files', 'presets'), exist_ok=True)


class MplCanvas(FigureCanvas):

    def __init__(self, canvas_fig=None, mode=None, width=5, height=4):
        fig = plt.Figure(figsize=(width, height), frameon=True)
        super(MplCanvas, self).__init__(fig)
        if canvas_fig:
            canvas_fig.figure.clf()
            canvas_fig.axes = canvas_fig.figure.add_subplot(111, projection=mode)
            if mode is not None:
                canvas_fig.axes.get_proj = lambda: np.dot(Axes3D.get_proj(canvas_fig.axes),
                                                          np.diag([1.5, 1.2, 1.2, 1]))
                canvas_fig.axes.view_init(elev=90., azim=-90)
            self.axes = canvas_fig.axes.figure.get_axes()
        else:
            self.axes = fig.add_subplot(111)


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

        self.generator = LissajousGenerator()

        layout = Qt.QVBoxLayout(self.groupBox)
        layout.addWidget(self._fig)
        # toolbar = NavigationToolbar(self._fig, self)
        # layout.addWidget(toolbar)

        self.plot_lissajous_figure()

    def init_ui(self):
        """
        Инициализация qt-формы
        """

        self.setStyleSheet("QLineEdit { border: 1px solid; border-color:#dcdcdc; border-radius: 4px;} "
                           "QLineEdit:focus{border:1px solid gray; }")

        uic.loadUi(self.settings["paths"]["ui"], self)
        validation_form(self)

        self.freq_z_lineedit.setVisible(False)
        self.label_5.setVisible(False)

        self.setWindowTitle(self.settings["message"].format(self.settings["version"]))

        self.setWindowIcon(QtGui.QIcon(self.settings["paths"]["icon"]["main"]))

        Qt.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.freq_x_lineedit.setToolTip('This is a <b>frequency X</b>')
        self.freq_y_lineedit.setToolTip('This is a <b>frequency Y</b')
        self.freq_z_lineedit.setToolTip('This is a <b>frequency Z</b>')
        self.phase_lineedit.setToolTip('This is a <b>phase rel</b>. 0.5 = pi/2')

        self.plot_button.clicked.connect(self.plot_button_click_handler)
        self.save_button.clicked.connect(self.save_image_button_handler)
        self.proportion_button.clicked.connect(self.proportion_ratio_click_handler)
        self.radio_grid.clicked.connect(self.plot_lissajous_figure)
        self.checkBox_3D.clicked.connect(self.update_plt)
        self.save_json_button.clicked.connect(self.save_json_button_handler)
        self.load_json_button.clicked.connect(self.load_file_handler)
        self.lengthSlider.valueChanged.connect(self.length_change_handler)

    # def clearLayout(self, layout):
    #     while layout.count():
    #         child = layout.takeAt(0)
    #         if child.widget() is not None:
    #             child.widget().deleteLater()
    #         elif child.layout() is not None:
    #             self.clearLayout(child.layout())

    def update_plt(self):
        """
        Обновление фигуры. Используется при первом старте и переключении 2D <-> 3D
        """
        # if self.groupBox.layout():
        #     self.clearLayout(self.groupBox.layout())

        if self.checkBox_3D.isChecked():
            # rcParams['xtick.color'] = 'red'
            # rcParams['ytick.color'] = 'red'
            # rcParams['axes.labelcolor'] = 'red'
            # rcParams['axes.edgecolor'] = 'red'
            self.freq_z_lineedit.setVisible(True)
            self.label_5.setVisible(True)

            MplCanvas(self._fig, mode='3d')
        else:
            self.freq_z_lineedit.setVisible(False)
            self.label_5.setVisible(False)
            MplCanvas(self._fig)

        self.plot_lissajous_figure()

    def plot_button_click_handler(self):
        """
        Функция обработки нажатия кнопки «Обновить фигуру».
        Запускает процесс генерации фигуры после валидации входных данных
        """

        validation_form(self)
        settings = self.get_settings()

        title_str = ''
        values_ph = settings.get("phase").split()
        for ph, axs in zip(values_ph, ['x', 'y', ]):
            conv = float(ph).as_integer_ratio()

            title_str = title_str + f'f_{axs}={round(conv[0], 3) if 1 < conv[0] < 9 else ""}' \
                                    f'{["pi*", "pi/"][conv[0] < 9]}' \
                                    f'{round(conv[1], 3) if 1 < conv[1] < 9 else ph}\n'
        self.phase_lineedit.setToolTip(title_str.rstrip())

        self.plot_lissajous_figure(settings)

    def length_change_handler(self):
        """
        Функция обработки изменения длины фигуры
        """

        self.length_label.setText(str(self.lengthSlider.value()))

    def plot_radio_grid_func(self):
        """
        Функция проверки свитча «Сетка». Включает в отображение сетку и нумерацию осей
        """

        if self.radio_grid.isChecked():
            self._fig.axes.grid(b=True, linestyle=':', linewidth=1)
        else:
            self._fig.axes.grid(b=False)

        self.check_axes()

    def check_axes(self):
        """
        Проверка флага включения сетки на графике и установка осей
        """

        if self.radio_grid.isChecked():
            self._fig.axes.axis("on")
            self._fig.axes.set_xlabel('X', fontsize=10, color='black')
            self._fig.axes.set_ylabel('Y', fontsize=10, color='black')
            if isinstance(self._fig.axes, Axes3D):
                self._fig.axes.set_zlabel('Z', fontsize=10, color='black')
        else:
            self._fig.axes.axis("off")

        self._fig.axes.tick_params(axis='both', length=5, labelsize=8)

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
            "freq_z": float(self.freq_z_lineedit.text()),
            "phase": self.phase_lineedit.text(),
            "length": int(self.lengthSlider.value())
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

        self._fig.axes.figure.tight_layout()

        self._fig.draw()

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

    def write_line_edit(self, data):
        """
        Функция записи настроек с загруженного файла. На стеке - над «load_file_handler»
        :param data: словарь с ключами "freq_x", "freq_y", "phase"
            :type data: dict
        """

        self.freq_x_lineedit.setText(str(float(data.get("freq_x", '3'))))
        self.freq_y_lineedit.setText(str(float(data.get("freq_y", '2'))))
        self.freq_z_lineedit.setText(str(float(data.get("freq_z", '0'))))
        self.phase_lineedit.setText(str(float(data.get("phase", '2'))))

        index = self.color_combobox.findText(data.get("color", 'Синий'), QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.color_combobox.setCurrentIndex(index)

        index = self.width_combobox.findText(str(data.get("linewidth", '2')), QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.width_combobox.setCurrentIndex(index)

        self.lengthSlider.setValue(data.get("length", '10'))

        check_dimension = data.get("3D", False)
        self.checkBox_3D.setChecked(check_dimension)

        self.update_plt()

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
            self._fig.print_figure(path)

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

    def save_json_button_handler(self):
        """
        Функция обработки нажатия кнопки «Сохранить настройки»
        Путь к файлу указан в settings.py (settings_mpl["dirs"]["settings"])
        """

        path = self.files_handler(img=False)
        if path:
            d = self.get_settings(params=True)
            d.update(self.get_settings(params=False, dict_val=0))
            d.update({"3D": self.checkBox_3D.isChecked()})
            with open(path, 'w', encoding='utf-8') as write_file:
                json.dump(d, write_file, indent=2, ensure_ascii=False)


# class First(Qt.QMainWindow):
#     def __init__(self, parent=None):
#         super(First, self).__init__(parent)
#         try:
#             from settings import SETTINGS_MPL
#         except:
#             msg = Qt.QMessageBox()
#             msg.setIcon(Qt.QMessageBox.Critical)
#             msg.setText('Не найден файл настроек!')
#             msg.exec_()
#             sys.exit('File with settings was deleted!')
#         uic.loadUi(SETTINGS_MPL["paths"]["start"], self)
#
#         self.pushButton.clicked.connect(self.on_pushButton_clicked)
#         self.dialog = LissajousWindow(self)
#
#     def on_pushButton_clicked(self):
#         self.hide()
#         self.dialog.show()


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)

    main_window = LissajousWindow()

    main_window.show()

    app.exec_()
