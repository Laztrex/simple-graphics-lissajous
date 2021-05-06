# Генератор фигур Лисажу

Генератор фигур Лиссажу с графическим интерфейсом на PyQt5.

Возможности:
* Генерация фигур Лиссажу с заданными частотами по X, Y, Z.
* Есть возможность задавать сдвиг фаз
* Установка цвета фигуры.
* Установка толщины линии.
* Экспорт фигур в виде изображений.
* Загрузка/экспорт готовых пресетов настроек


>Замечание
>Иногда частоты по X и Y обозначают буквами $a$, $b$, $c$.


## Работа с исходным кодом
Запуск:

~~~
python main_lissajous.py

# Clone from github
git clone https://github.com/Laztrex/simple-graphics-lissajous.git

# Installing all dependencies 
pip install -r requirements.txt
~~~

Для удобства работы имеет смысл использовать виртуальные окружения.

Настройки цветовых схем, директорий, служебных сообщений и версии находятся в *settings.py*

Для упаковки в исполняемый файл выполните:
~~~
pyinstaller --onefile --icon=files/lissajous.ico --noconsole main_lissajous.py
~~~

Для этого для системы Windows может понадобиться библиотека _pywin32-ctypes_
~~~
pip install pywin32-ctypes
~~~

Все необходимые пакеты указаны в *requirements_win.txt (Windows 10 x64) и requirements_linux.txt (Ubuntu 20.4)*

## Работа с интерфейсом
Запуск:
~~~
main_lissajous.exe
~~~
**Вид стартового интерфейса** 
![Image alt](https://github.com/Laztrex/simple-graphics-lissajous/raw/master/media/main.jpg)

На текущий момент доступны функции:
* Установка частот [1; 99]  
(но желательно, конечно, устанавливать в рамках 
[правильных пропорций](https://cutt.ly/pkysYfO))
* Установка сдвига фаз
* Изменение цвета линий
* Регулирование толщины линии
* Вернуть окно к заданному соотношению (Выровнять)
* Отображение сетки
* Обновить фигуру (после измененных параметров нужно применить)
* Сохранить картинку полученной фигуру
* Сохранить/загрузить пресет нужной фигуры

Далее функционал будет расширяться.

Поменяем настройки, получим новую фигуру.

**Окно интерфейса после изменения настроек**
![Image alt](https://github.com/Laztrex/simple-graphics-lissajous/raw/master/media/main_2.jpg)

**Менять цвет фигуры можно с помощью меню _Цвет линии_**
![Image alt](https://github.com/Laztrex/simple-graphics-lissajous/raw/master/media/main_2_color.jpg)

Для удобства есть свитч для отображения сетки и числовых осей

**Вид сетки**

![Image alt](https://github.com/Laztrex/simple-graphics-lissajous/raw/master/media/main_2_grid.jpg)

Также рядом есть меню выбора толщины линии

**Регулирование толщины линии**
![Image alt](https://github.com/Laztrex/simple-graphics-lissajous/raw/master/media/main_2_grid_line.jpg)

Окно интерфейса можно регулировать по всем направлениям.
Однако предусмотрена кнопка _Выровнять_ для возврата к 
стандартному соотношению 4/3
![Image alt](https://github.com/Laztrex/simple-graphics-lissajous/raw/master/media/main_2_strached-norm.jpg)

Сохранить фигуру можно при нажатии кнопки _Сохранить фигуру в файл_,
 а сохранить текущие настройки можно по кнопке _Сохранить настройки_.
Откроется диалоговое окно, где необходимо написать имя файла и место сохранения. 
По умолчанию директория для картинок - _\files\pics_, для настроек - _\files\presets_

**Пример сохранения настроек**
![Image alt](https://github.com/Laztrex/simple-graphics-lissajous/raw/master/media/save_preset.jpg)

Загрузка настроек осуществляется при нажатии кнопки _Загрузить настройки_.
Данные будут считаны с файла и вставлена в соответствующие поля интерфейса. 
Фигура пересоберётся.

**Пример загрузки настроек**
![Image alt](https://github.com/Laztrex/simple-graphics-lissajous/raw/master/media/load_preset.jpg)


**Результат загрузки настроек**
![Image alt](https://github.com/Laztrex/simple-graphics-lissajous/raw/master/media/preset_to_load.jpg)

Поля параметров изменились, была выведена соответствующая фигура.


## Перспектива
В дальнейшем планируется:
* Расширять функционал вглубь и вширь
* Дорабатывать элементы управления
* Улучшать взаимодействие с настройками (плавное регулирование)
* Добавить возможность анимирования
* Добавить возможность отрисовки 3D-фигур

## Вариант запуска docker на Ubuntu20.04
- Собрать образ. Например:
~~~
user_mac simple-graphics-lissajous % docker build -t qt_test . 
~~~
~~~
docker run --rm -it -v $(pwd)/files:/tmp/files -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -u qtapp qt_test
~~~

## Вариант запуска docker на MacOS
- Собрать образ. Например:
~~~
user_mac simple-graphics-lissajous % docker build -t qt_test . 
~~~
- Установить XQuartz
- В настойках XQuartz дать разрешение подключения из клиентских сетей
- команды:
~~~
IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
~~~
~~~
xhost +
~~~
~~~
docker run --rm -it -v $(pwd)/files:/tmp/files -v /tmp/.X11-unix:/tmp.X11-unix -e DISPLAY=$IP:0 qt_test
~~~
