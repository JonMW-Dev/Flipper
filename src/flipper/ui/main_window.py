# creation of my widgets to display
from PySide6 import QtCore, QtWidgets, QtGui
from flipper.ui.chat_delegate import ChatDelegate
from flipper.models.chat_model import chatModel
from flipper.services.chat_client import AIChatController

SYSTEM_INSTRUCTION = "You are a conversational chatbot"
class main_widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

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

        # Connect AI model 
        self.AIController = AIChatController()
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
        # check that the input box has a message to send
        if len(self.input_textbox.text()) == 0:
            print("Error: There was no message to send.")
            return

        # store the message to send and clear input box
        user_msg = self.input_textbox.text()
        self.input_textbox.clear()

        #add user message to the data model
        self.model.add_message({"role":"user", "content":user_msg})

        #Construct prompt to AI, include system prompt and chat history
        request = [
            {"role":"system", "content": SYSTEM_INSTRUCTION},
            *self.model.messages
        ]

        # send message to the AI
        response = self.AIController.send_message(request)
        response_msg = response.choices[0].message.content

        #Add the AI response to the data model
        print(response_msg)
        self.model.add_message({"role":"assistant", "content":response_msg})





    

