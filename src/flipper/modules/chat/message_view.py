from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMessageBox
from .chat_delegate import ChatDelegate


class MessageView(QtWidgets.QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        #setup the view
        self.list_view = QtWidgets.QListView()
        self.list_view.setModel(self.model) # Connect view to the model
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

        self.model.rowsInserted.connect(lambda: self.list_view.scrollToBottom()) # scroll to bottom when row data is inserted

        # render the list
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.list_view)


    def display_warning(self, message):
        QMessageBox.information(None, "AI Chat Failed", f"CHAT ERROR - REMOVING MESSAGE: \n\n\"{message['content']}\"")

    @Slot(dict)
    def update_chat(self, message):
        self.model.add_message(message)
        #get latest status from chat model


        pass
    pass