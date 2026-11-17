# Provides the AI prompt and response services to the MainWindow

from openai import OpenAI, AuthenticationError, APIError
from src.flipper.services.config_service import ConfigService
from PySide6 import QtCore
from PySide6.QtCore import QObject


class ChatClient(QObject):
    api_key = None
    url     = None
    model   = None
    failed  = QtCore.Signal()
    def __init__(self):
        super().__init__()
        #connect to config service
        self.config_service = ConfigService()
        self.config_service.saved.connect(self.reload_configuration)

        self.reload_configuration()
        # Create OpenAI API client
        self.AI_client = OpenAI(
            base_url= self.url,
            api_key =self.api_key,
        )

    def send_message(self, messages: list[dict[str,str]]):
        try: 
            return self.AI_client.chat.completions.create(
                model = self.model,
                messages=messages,
            )
        except AuthenticationError:
            self.failed.emit()
            raise RuntimeError("Invalid/missing API key, check your configuration")
        except APIError as e:
            self.failed.emit()
            raise RuntimeError(f"AI request failed: {e}")
            

    def reload_configuration(self):
        config = self.config_service.get_config()
        self.api_key = config['API_KEY']
        self.url     = config['base_url']
        self.model   = config['model']
        
        # reset ai client with new config.
        self.AI_client = OpenAI(
            base_url = self.url,
            api_key  = self.api_key
        )

