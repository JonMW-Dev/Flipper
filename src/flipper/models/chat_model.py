from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex
from PySide6 import QtCore
from PySide6.QtGui import QBrush, QColor

from flipper.services.chat_client import AIChatController
class MessageRoles:
        TextRole = Qt.UserRole + 1
        AiRole = Qt.UserRole + 2
class ChatModel(QAbstractListModel):
    ColorRole = Qt.UserRole + 10
    failed_message = QtCore.Signal(dict)
    def __init__(self):
        super().__init__()

        self.messages: list[dict[str,str]] = [
            {"role":"assistant",  "content":"Hello please enter a message"},    
        ]


    def rowCount(self, parent=None):
        return len(self.messages)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        msg = self.messages[index.row()]
        text = msg["content"]
        is_user = msg["role"] == "user"
        is_ai = msg["role"] == "assistant"

        if role == Qt.DisplayRole:
        # Show whatever is in the dict
            if is_user:
                return text
            if is_ai:
                return "Bot: " + text
            return str(msg)
        
        # if role == MessageRoles.TextRole:
        #     return msg["user"]

        # if role == MessageRoles.AiRole:
        #      return msg["AI"]

        # Alignment
        if role == Qt.TextAlignmentRole:
            if is_user:
                return Qt.AlignRight
            if is_ai:
                return Qt.AlignLeft

        # ChatDelegate reads this. Leave every other role as None.
        if role == self.ColorRole:
            if is_user:
                return QColor("#7ae582")
            return QColor("#25a18e")

        if role == Qt.ForegroundRole:
            return QColor("#000000")
        



        return None

    def add_message(self, message: dict):
        self.beginInsertRows(QModelIndex(), len(self.messages), len(self.messages))
        self.messages.append(message)
        self.endInsertRows()

    # Runs on a pool thread. Emit the reply; the window adds it on the GUI thread.
    def request_response(self, messages, reply_ready):
        AI_service = AIChatController()
        AI_service.failed.connect(self.remove_lastMessage)
        response = AI_service.send_message(messages)
        response_msg = response.choices[0].message.content
        if response_msg is None:
            raise RuntimeError("Error: no response received")
        reply_ready.emit({"role": "assistant", "content": response_msg}) # signal emmited, captured by view slot
        
    def remove_lastMessage(self):
        self.beginInsertRows(QModelIndex(), len(self.messages), len(self.messages))
        removed_msg = self.messages.pop()

        self.endInsertRows()
        self.failed_message.emit(removed_msg)


    def get_message(self):
        return self.messages
    
    
        
