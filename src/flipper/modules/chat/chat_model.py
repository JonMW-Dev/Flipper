from threading import Lock

from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, Signal
from PySide6.QtGui import QColor

from flipper.services.chat_service import ChatService
class MessageRoles:
        TextRole = Qt.ItemDataRole.UserRole + 1
        AiRole = Qt.ItemDataRole.UserRole + 2
class ChatModel(QAbstractListModel):
    ColorRole = Qt.ItemDataRole.UserRole + 10
    failed_message = Signal(dict)
    def __init__(self, chat_service):
        super().__init__()
        self.chat_service = chat_service

        # One subscription. Connecting inside request_response stacked a removal per send.
        self._pending_replies = 0
        self._pending_lock = Lock()
        self.chat_service.reply_ready.connect(self.add_message)
        self.chat_service.failed.connect(self.remove_last_Message)

        self.messages: list[dict[str,str]] = [
            {"role":"assistant",  "content":"Hello please enter a message"},    
        ]


    def rowCount(self, parent=None):
        return len(self.messages)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        
        msg = self.messages[index.row()]
        text = msg["content"]
        is_user = msg["role"] == "user"
        is_ai = msg["role"] == "assistant"

        if role == Qt.ItemDataRole.DisplayRole:
        # Show whatever is in the dict
            if is_user:
                return text
            if is_ai:
                return "Bot: " + text
            return str(msg)
        
        # Alignment
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if is_user:
                return Qt.AlignmentFlag.AlignRight
            if is_ai:
                return Qt.AlignmentFlag.AlignLeft

        # ChatDelegate reads this. Leave every other role as None.
        if role == self.ColorRole:
            if is_user:
                return QColor("#7ae582")
            return QColor("#25a18e")

        if role == Qt.ItemDataRole.ForegroundRole:
            return QColor("#000000")
        



        return None

    def add_message(self, message: dict):
        self.beginInsertRows(QModelIndex(), len(self.messages), len(self.messages))
        self.messages.append(message)
        self.endInsertRows()

    def _add_pending(self):
        with self._pending_lock:
            self._pending_replies += 1

    def _take_pending(self) -> bool:
        with self._pending_lock:
            if self._pending_replies <= 0:
                return False
            self._pending_replies -= 1
            return True

    # Runs on a pool thread. Emit the reply; the window adds it on the GUI thread.
    def request_response(self, messages):
        self._add_pending()
        try:
            response = self.chat_service.send_message(messages)
        except RuntimeError:
            return
        response_msg = response.choices[0].message.content
        if response_msg is None:
            self.chat_service.failed.emit()
            return
        # This request succeeded, so a later failure must not remove its row.
        self._take_pending()
        self.chat_service.reply_ready.emit({"role": "assistant", "content": response_msg})
        
    def remove_last_Message(self):
        if not self._take_pending() or not self.messages:
            return
        row = len(self.messages) - 1
        self.beginRemoveRows(QModelIndex(), row, row)
        removed_msg = self.messages.pop()
        self.endRemoveRows()
        self.failed_message.emit(removed_msg)


    def get_message(self):
        return self.messages
    
    
        
