import os

settings_mpl = \
    {
        "color_map": {
            "Красный": "crimson",
            "Зелёный": "green",
            "Жёлтый": "gold",
            "Синий": "midnightblue"
        },

        "default": {
            "freq_x": 1,
            "freq_y": 3,
            "color": "midnightblue",
            "width": 2
        },
        "paths": {
            "files": "files/presets/",
        },

        "messages": {
            "images": [None, "Сохранение изображения", "C:\\",
                       "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) "],
            "settings": [None, "Сохранение настроек", f"{os.path.normpath(os.path.dirname(__file__) + '/presets')}",
                         "JSON(*.json);;All Files(*.*) "],
        },

        "version": "0.1"
    }
