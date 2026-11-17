# Date: 16/11/26 | Author: Jonathan Windle
# main executed file for FlipperAI project 

import sys
from PySide6 import QtWidgets
from flipper.ui.main_window import MainWindow
def main():
    application = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(900, 600)
    widget.show()

    sys.exit(application.exec())
    
if __name__ == "__main__":
    main()

