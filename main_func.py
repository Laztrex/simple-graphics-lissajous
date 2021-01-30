#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import sys

import PyQt5.QtWidgets as Qt
from PyQt5 import uic, QtGui, QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from lissajousgen import LissajousGenerator


def validation_form(form):
    reg_ex_lineedit = QtCore.QRegExp("^[1-9]{1,}$.[1-9]{1,}$")
    reg_ex_phase = QtCore.QRegExp(r"^[1-9]{1,}")
    input_validator_1 = QtGui.QRegExpValidator(reg_ex_lineedit, form.freq_x_lineedit)
    input_validator_2 = QtGui.QRegExpValidator(reg_ex_lineedit, form.freq_y_lineedit)
    input_phase = QtGui.QRegExpValidator(reg_ex_phase, form.phase_lineedit)
    form.freq_x_lineedit.setValidator(input_validator_1)
    form.freq_y_lineedit.setValidator(input_validator_2)
    form.phase_lineedit.setValidator(input_phase)


class LissajousWindow(Qt.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(LissajousWindow, self).__init__(*args, **kwargs)

        try:
            from settings import settings_mpl
        except:
            msg = Qt.QMessageBox()
            msg.setIcon(Qt.QMessageBox.Critical)
            msg.setText('Не найден файл настроек!')
            msg.exec_()
            sys.exit('Delete file with settings!')

        self.settings = settings_mpl

        self.generator = LissajousGenerator(resolution=100)

        uic.loadUi(os.path.dirname(__file__) + "\main_window.ui", self)
        validation_form(self)

        self.setWindowTitle(f"Генератор фигур Лиссажу. Версия {self.settings.get('version', 'alpha')}. CC BY-SA 4.0 "
                            f"Lazarev")

        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + "files/icon.bmp"))

        self._fig = plt.Figure(figsize=(5, 4), dpi=100)
        self._ax = self._fig.add_subplot(1, 1, 1)

        self._fc = FigureCanvas(self._fig)
        layout = Qt.QVBoxLayout(self.groupBox)
        layout.addWidget(self._fc)

        self.plot_lissajous_figure()

        self.plot_button.clicked.connect(self.plot_button_click_handler)
        self.save_button.clicked.connect(self.save_image_button_handler)
        self.proportion_button.clicked.connect(self.proportion_ratio_click_handler)
        self.radio_grid.clicked.connect(self.plot_radio_grid_handler)
        self.save_json_button.clicked.connect(self.save_json_button_handler)
        self.load_json_button.clicked.connect(self.load_file_handler)

    def plot_button_click_handler(self):
        """
        Обработчик нажатия на кнопку применения настроек
        """
        validation_form(self)
        settings = self.get_settings()
        self.plot_lissajous_figure(settings)

    def plot_radio_grid_handler(self):
        """Обработка флага сетки"""
        if self.radio_grid.isChecked():
            self._ax.grid(True)
        else:
            self._ax.grid(False)
        self.plot_lissajous_figure()

    def get_settings(self, params=True):
        return {
            "freq_x": float(self.freq_x_lineedit.text()),  # TODO обработка входа
            "freq_y": float(self.freq_y_lineedit.text()),  # была ошибка x-y
            "phase": self.phase_lineedit.text(),
        } if params \
            else {"color": self.settings["color_map"].get(self.color_combobox.currentText(), 'black'),
                  "linewidth": int(self.width_combobox.currentText())}

    def plot_lissajous_figure(self, settings=None):
        """
        Обновление фигуры
        """
        if settings is None:
            settings = self.get_settings()

        for line in self._ax.lines:
            line.remove()

        x_arr, y_arr = self.generator.generate_figure(**settings)
        self._ax.plot(x_arr, y_arr,
                      **self.get_settings(params=False))

        if self.radio_grid.isChecked():
            self._ax.axis("on")
            self._ax.set_xlim(min(x_arr), max(x_arr))
            self._ax.set_ylim(min(y_arr), max(y_arr))
        else:
            self._ax.axis("off")

        plt.tight_layout()

        self._fc.draw()

    def files_handler(self, mode='save', img=True):
        """
        Обработчик нажатия на кнопку сохранения настроек
        """
        if mode == 'save':
            file_path, _ = Qt.QFileDialog.getSaveFileName(*self.settings["messages"][["settings", "images"][img]])
        else:
            file_path, _ = Qt.QFileDialog.getOpenFileName(*self.settings["messages"]["settings"])

        if not file_path:
            return

        return file_path

    def load_file_handler(self):
        """
        Обработчик нажатия на кнопку загрузки настроек
        """

        path_to_file = self.files_handler(mode='load')
        if path_to_file:
            with open(path_to_file, 'r') as open_file:
                loaded_settings = json.load(open_file)
            self.write_line_edit(loaded_settings)

    def write_line_edit(self, data):
        self.freq_x_lineedit.setText(str(data["freq_x"]))
        self.freq_y_lineedit.setText(str(data["freq_y"]))
        self.phase_lineedit.setText(data["phase"])
        self.plot_lissajous_figure()

    def proportion_ratio_click_handler(self):
        """
        Выравнивание соотношения сторон
        """
        h = min(self.height(), self.width())
        self.resize(h + 294, h)

    def save_image_button_handler(self):
        path = self.files_handler()
        if path:
            self._fig.savefig(path)

    def save_json_button_handler(self):
        path = self.files_handler(img=False)
        if path:
            d = self.get_settings(params=True)
            with open(path, 'w') as write_file:
                json.dump(d, write_file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)

    main_window = LissajousWindow()

    main_window.show()

    app.exec()
