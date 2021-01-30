import os

os.makedirs(os.path.normpath(os.path.dirname(__file__) + '/files/pics'), exist_ok=True)
os.makedirs(os.path.normpath(os.path.dirname(__file__) + '/files/presets'), exist_ok=True)


settings_mpl = \
    {
        "color_map": {
            "Красный": "crimson",
            "Зелёный": "green",
            "Жёлтый": "gold",
            "Синий": "midnightblue"
        },

        "paths": {
            "files": "files/presets/",
        },

        "messages": {
            "images": [None, "Сохранение изображения",
                       f"{os.path.normpath(os.path.dirname(__file__) + '/files/pics')}",
                       "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) "],
            "settings": [None, "Сохранение настроек",
                         f"{os.path.normpath(os.path.dirname(__file__) + '/files/presets')}",
                         "JSON(*.json);;All Files(*.*) "],
        },

        "version": "0.1"
    }
