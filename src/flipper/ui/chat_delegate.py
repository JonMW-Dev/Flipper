# Controls the appearance of data within the View
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtGui import QPainter, QColor
from flipper.models.chat_model import ChatModel

class ChatDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()
        color = index.data(ChatModel.ColorRole)
        if color:
            painter.fillRect(option.rect, color)
        super().paint(painter, option, index)
        painter.restore()


