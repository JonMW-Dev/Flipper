# creation of my widgets to display
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QThreadPool, Slot, Signal
from flipper.ui.chat_delegate import ChatDelegate
from flipper.models.chat_model import chatModel

SYSTEM_INSTRUCTION = "You are a conversational chatbot"
class ChatWidget(QtWidgets.QWidget):
    message_signal = Signal(dict)
    
    def __init__(self):
        super().__init__()
        # setup GUI thread slot for message received signal
        self.message_signal.connect(self.update_chat)

        # setup QThreadPool for responsive GUI during message send/receive
        self.threadpool = QThreadPool()

        # Setup Model/View for chat
        self.model = chatModel()
        self.list_view = QtWidgets.QListView()
        self.list_view.setModel(self.model)
        self.list_view.setItemDelegate(ChatDelegate())
        self.list_view.setAlternatingRowColors(False)
        self.list_view.setWordWrap(True)
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


    @Slot(dict)
    def update_chat(self, message):
        self.model.add_message(message)

    def send_message(self):

        # check that the input box has a message to send
        if len(self.input_textbox.text()) == 0:
            print("Error: There was no message to send.")
            return

        # store the message to send and clear input box
        user_msg = self.input_textbox.text()
        self.input_textbox.clear()

        #add user message to the data model
        self.model.add_message({"role":"user", "content":user_msg})

        # System instruction stays out of the visible list. The pool thread
        # receives this snapshot and must not touch the model.
        request = [
            {"role":"system", "content": SYSTEM_INSTRUCTION},
            *self.model.messages
        ]
        self.threadpool.start(
            lambda: self.model.request_response(request, self.message_signal)
        )





    

