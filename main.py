# Date: 14/11/26 | Author: Jonathan Windle
# main executed file for FlipperAI project 

# We will initially use this project to learn Qt/Pyside6 for GUI. 
import sys
from PySide6 import QtWidgets
from MainWindow import main_widget
def main():
    application = QtWidgets.QApplication([])

    widget = main_widget()
    widget.resize(900, 600)
    widget.show()

    sys.exit(application.exec())

if __name__ == "__main__":
    main()

