# main.py

import sys
from gui import ShoppingCartApp
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    window = ShoppingCartApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
