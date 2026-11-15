# creation of my widgets to display
from PySide6 import QtCore, QtWidgets, QtGui
class main_widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("click me")
        self.label  = QtWidgets.QLabel(
            "",
            alignment = QtCore.Qt.AlignCenter
        )

        # Define the layout of the main widget
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)

        # Set up event listener for the button

        self.button.clicked.connect(self.triggered)

    def triggered(self):
        self.label.setText("Hello World")

    

