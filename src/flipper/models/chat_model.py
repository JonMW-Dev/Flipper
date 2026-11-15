from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex
from PySide6.QtGui import QBrush, QColor
class MessageRoles:
        TextRole = Qt.UserRole + 1
        AiRole = Qt.UserRole + 2
class chatModel(QAbstractListModel):
    ColorRole = Qt.UserRole + 10
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
    
    
        
