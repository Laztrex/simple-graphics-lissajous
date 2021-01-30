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
            "files": f"{os.path.join(os.path.dirname(__file__) + '/files/presets/')}",
            "icon": {
                "main": f"{os.path.join(os.path.dirname(__file__) + '/files/icon.bmp')}",
                "error": f"{os.path.join(os.path.dirname(__file__) + '/files/error.bmp')}"
            },

            "ui": f"{os.path.join(os.path.dirname(__file__) + '/main_window.ui')}"
        },

        "dirs": {
            "images": [None, "Сохранение изображения",
                       f"{os.path.join(os.path.dirname(__file__) + '/files/pics')}",
                       "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) "],
            "settings": [None, "Сохранение настроек",
                         f"{os.path.join(os.path.dirname(__file__) + '/files/presets')}",
                         "JSON(*.json);;All Files(*.*) "],
        },


        "message": "Генератор фигур Лиссажу. Версия {}. CC BY-SA 4.0 Lazarev",


        "version": "0.1"
    }
