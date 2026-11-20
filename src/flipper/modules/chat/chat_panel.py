from .message_view import MessageView
from PySide6 import QtWidgets
from PySide6.QtCore import QThreadPool, Signal
# holds all the visually rendered elements for the chat module

SYSTEM_INSTRUCTION = "You are a conversational chatbot"

class ChatPanel(QtWidgets.QWidget):
    message_signal = Signal(dict)
    def __init__(self, chat_model):
        super().__init__()
        # set up connections (model, thread pool)
        self.chat_model = chat_model
        self.threadpool = QThreadPool()


        # add the MessageView 
        self.message_view = MessageView(self.chat_model)

        # Add message input box and send button
        self.input_textbox = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton("send")

        #define layout of the panel
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.message_view)
        layout.addWidget(self.input_textbox)
        layout.addWidget(self.button)

        self.input_textbox.returnPressed.connect(self.send_message)
        self.button.clicked.connect(self.send_message)

        self.chat_model.failed_message.connect(self.display_error)

    def send_message(self):

        # check that the input box has a message to send
        if len(self.input_textbox.text()) == 0:
            print("Error: There was no message to send.")
            return

        # store the message to send and clear input box
        user_msg = self.input_textbox.text()
        self.input_textbox.clear()

        #add user message to the data model
        self.chat_model.add_message({"role":"user", "content":user_msg})

        # System instruction stays out of the visible list. The pool thread
        # receives this snapshot and must not touch the model.
        request = [
            {"role":"system", "content": SYSTEM_INSTRUCTION},
            *self.chat_model.messages
        ]
        self.threadpool.start(
            lambda: self.chat_model.request_response(request)
        )

    def display_error(self, message: dict):
        error_message = f"""
            Chat Service Failed - No Response Received
            Deleting Message: \n\t {message['content']}
            \n\n
            Please ensure your configuration is correct
        """
        QtWidgets.QMessageBox.warning(self, "Chat Error", error_message)