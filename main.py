#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import PyQt5.QtWidgets as qt
from PyQt5 import uic, QtGui, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import json

from lissajou.lissajousgen import LissajousGenerator

# Настройки фигуры по умолчанию
default_settings = {
    "freq_x": 1,
    "freq_y": 3,
    "color": "midnightblue",
    "width": 2
}  # TODO

# Цвета для matplotlib
with open("mpl.json", mode="r", encoding="utf-8") as f:
    mpl_color_dict = json.load(f)  # TODO


class ValidationForm(QtGui.QRegExpValidator):
    def __init__(self):
        super().__init__()


# TODO: RegExp
class LissajousWindow(qt.QMainWindow):
    def __init__(self):
        super(LissajousWindow, self).__init__()
        self.generator = LissajousGenerator(resolution=100)

        uic.loadUi("main_window.ui", self)
        reg_ex = QtCore.QRegExp("[0-9]+")
        input_validator = QtGui.QRegExpValidator(reg_ex, self.freq_x_lineedit)
        self.freq_x_lineedit.setValidator(input_validator)

        # Ставим версию и иконку
        with open("version.txt", "r") as file:
            version = file.readline()
        self.setWindowTitle("Генератор фигур Лиссажу. Версия {}. CC BY-SA 4.0 Ivanov".format(
            version  # TODO
        ))
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + "icon.bmp"))

        self._fig = plt.figure(figsize=(4, 3), dpi=72)
        self._ax = self._fig.add_subplot(1, 1, 1)

        self._fc = FigureCanvas(self._fig)
        layout = qt.QVBoxLayout(self.groupBox)
        layout.addWidget(self._fc)

        self.plot_lissajous_figure()

        self.plot_button.clicked.connect(self.plot_button_click_handler)
        self.save_button.clicked.connect(self.save_button_click_handler)
        # self.proportion_button.clicked.connect(self.proportion_ratio_click_handler)

    def plot_button_click_handler(self):
        """
        Обработчик нажатия на кнопку применения настроек
        """
        settings = self.get_settings()
        self.plot_lissajous_figure(settings)

    def get_settings(self, params=True):
        return {
            "freq_x": float(self.freq_x_lineedit.text()),  # TODO обработка входа
            "freq_y": float(self.freq_y_lineedit.text()),  # была ошибка x-y
            "phase": self.phase_lineedit.text(),
            "a": float(self.amp_a_lineedit.text()),
            "b": float(self.amp_b_lineedit.text())
        } if params \
            else {"color": mpl_color_dict[self.color_combobox.currentText()],
                  "linewidth": int(self.width_combobox.currentText())}

    def plot_lissajous_figure(self, settings=None):
        """
        Обновление фигуры
        """
        # Удаляем устаревшие данные с графика
        if settings is None:
            check_settings = self.get_settings()
            settings = default_settings if not check_settings else check_settings
        for line in self._ax.lines:
            line.remove()

        figure = self.generator.generate_figure(**settings)

        self._ax.plot(figure.x_arr, figure.y_arr,
                      **self.get_settings(params=False))

        # self._fc.resize(400, 300)
        # self._fc.move(20, 20)
        #
        # self.resize(650, 300)
        plt.axis("off")

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

    # def proportion_ratio_click_handler(self):
    #     """
    #     Выравнивание соотношения сторон
    #     """
    #     h, w = self.height(), self.width()
    #
    #     self.resize(max([h, w]) - 239, min([h, w]) - 9)


if __name__ == "__main__":
    app = qt.QApplication(sys.argv)

    main_window = LissajousWindow()

    main_window.show()
    sys.exit(app.exec_())
