# creation of my widgets to display
from PySide6 import QtCore, QtWidgets, QtGui
from ChatModel import chatModel
from ChatDelegate import ChatDelegate


class main_widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Setup Model/View for chat
        self.model = chatModel()
        self.list_view = QtWidgets.QListView()
        self.list_view.setModel(self.model)
        self.list_view.setItemDelegate(ChatDelegate())
        self.list_view.setAlternatingRowColors(False)
        self.list_view.setStyleSheet("""
            QListView {
                border: none;
                outline: none;
            }
            QListView::item {
                width: auto;
                padding: 8px;
                border-radius: 8px;
                margin: 2px;
                background-color: transparent
                color: black;
            }
            QListView::item:selected {
            }
        """)
        self.model.rowsInserted.connect(lambda: self.list_view.scrollToBottom())

        #set up text input box
        self.input_textbox = QtWidgets.QLineEdit()
        #set up send button
        self.button = QtWidgets.QPushButton("send")

        # Define the layout of the main widget
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.list_view)
        self.layout.addWidget(self.input_textbox)
        self.layout.addWidget(self.button)

        # Set up event listener for the button or quick send (enter)
        self.input_textbox.returnPressed.connect(self.send_message)
        self.button.clicked.connect(self.send_message)

    def send_message(self):
        if len(self.input_textbox.text()) == 0:
            print("Error: There was no message to send.")
            return

        self.model.add_message({"role":"user", "content":self.input_textbox.text()})

        self.input_textbox.clear()




    

