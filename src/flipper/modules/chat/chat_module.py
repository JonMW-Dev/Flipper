from .chat_model import ChatModel
from .chat_panel  import ChatPanel
# Contains all objects required for the chat module. 

class ChatModule():
    def __init__(self, chat_service):
        self.chat_service = chat_service
        
        # Add the panel and model components to the module
        self.chat_model= ChatModel(self.chat_service)
        self.chat_panel = ChatPanel(self.chat_model)
        

    def get_chat_panel(self):
        return self.chat_panel
