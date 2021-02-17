import os
import sys


# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False) and not __file__.endswith('.exe'):
    application_path = os.path.dirname(os.path.realpath(sys.executable))
else:
    application_path = os.path.dirname(os.path.realpath(__file__))


SETTINGS_MPL = \
    {
        "color_map": {
            "Красный": "crimson",
            "Зелёный": "green",
            "Жёлтый": "gold",
            "Синий": "midnightblue"
        },

        "paths": {
            "files": f"{os.path.join(application_path, 'files', 'presets')}",
            "icon": {
                "main": f"{os.path.join(application_path, 'files', 'icon.ico')}",
            },

            "ui": f"{os.path.join(application_path, 'main_window.ui')}"
        },

        "dirs": {
            "images": [None, "Сохранение изображения",
                       f"{os.path.join(application_path, 'files', 'pics')}",
                       "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) "],
            "settings": [None, "Сохранение настроек",
                         f"{os.path.join(application_path, 'files', 'presets')}",
                         "JSON(*.json);;All Files(*.*) "],
        },

        "message": "Генератор фигур Лиссажу. Версия {}. CC BY-SA 4.0 Lazarev",

        "version": "0.1"
    }
