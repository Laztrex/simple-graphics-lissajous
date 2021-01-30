import sys
import PyQt5.QtWidgets as Qt

from form import LissajousWindow


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)

    main_window = LissajousWindow()

    main_window.show()

    app.exec_()
