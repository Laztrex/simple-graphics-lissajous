#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import PyQt5.QtWidgets as qt
from PyQt5 import uic, QtGui, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import json

from lissajousgen import LissajousGenerator


def validation_form(form):
    reg_ex_lineedit = QtCore.QRegExp("[0-9].[0-9]+")
    input_validator_1 = QtGui.QRegExpValidator(reg_ex_lineedit, form.freq_x_lineedit)
    input_validator_2 = QtGui.QRegExpValidator(reg_ex_lineedit, form.freq_y_lineedit)
    form.freq_x_lineedit.setValidator(input_validator_1)
    form.freq_y_lineedit.setValidator(input_validator_2)


# TODO: RegExp
class LissajousWindow(qt.QMainWindow):
    def __init__(self):
        super(LissajousWindow, self).__init__()

        self.settings = self.give_settings()

        self.generator = LissajousGenerator(resolution=100)

        uic.loadUi("main_window.ui", self)
        validation_form(self)

        self.setWindowTitle(f"Генератор фигур Лиссажу. Версия {self.settings.get('version', 'alpha')}. CC BY-SA 4.0 "
                            f"Lazarev")

        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + "icon.bmp"))
        #
        # self._fig = plt.figure(figsize=(4, 3), dpi=72, tight_layout=True)
        self._fig = plt.Figure(figsize=(5, 4), dpi=100)
        self._ax = self._fig.add_subplot(1, 1, 1)

        self._fc = FigureCanvas(self._fig)
        layout = qt.QVBoxLayout(self.groupBox)
        layout.addWidget(self._fc)

        self.plot_lissajous_figure()

        self.plot_button.clicked.connect(self.plot_button_click_handler)
        self.save_button.clicked.connect(self.save_button_click_handler)
        self.proportion_button.clicked.connect(self.proportion_ratio_click_handler)
        self.radio_grid.clicked.connect(self.plot_radio_grid_handler)

    def plot_button_click_handler(self):
        """
        Обработчик нажатия на кнопку применения настроек
        """
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
            # "a": float(self.amp_a_lineedit.text()),
            # "b": float(self.amp_b_lineedit.text())
        } if params \
            else {"color": self.settings["color_map"].get(self.color_combobox.currentText(), 'black'),
                  "linewidth": int(self.width_combobox.currentText())}

    def plot_lissajous_figure(self, settings=None):
        """
        Обновление фигуры
        """
        # Удаляем устаревшие данные с графика
        if settings is None:
            check_settings = self.get_settings()
            settings = self.settings if not check_settings else check_settings

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

    def save_button_click_handler(self):
        """
        Обработчик нажатия на кнопку сохранения настроек
        """
        file_path, _ = qt.QFileDialog.getSaveFileName(None, "Сохранение изображения", "C:\\",
                                                      "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if file_path == "":
            return

        # raise NotImplementedError("Тут всего одной строчки не хватает.")
        self._fig.savefig(file_path)

    def proportion_ratio_click_handler(self):
        """
        Выравнивание соотношения сторон
        """
        h = min(self.height(), self.width())
        self.resize(h + 294, h)

    @staticmethod
    def give_settings(file="files/mpl.json"):
        with open(file, mode="r", encoding="utf-8") as f:
            return json.load(f)


if __name__ == "__main__":
    app = qt.QApplication(sys.argv)

    main_window = LissajousWindow()

    main_window.show()
    sys.exit(app.exec_())
