# Provides the AI prompt and response services to the MainWindow

from openai import OpenAI, AuthenticationError, APIError
from openai.types.chat import ChatCompletionMessageParam
from PySide6 import QtCore
from PySide6.QtCore import QObject
from typing import cast


class ChatService(QObject):
    api_key = None
    url     = None
    model   = None
    failed  = QtCore.Signal()
    reply_ready = QtCore.Signal(dict)

    def __init__(self, configuration: dict):
        super().__init__()
        self.configuration = configuration
        self.reload_configuration()

    def send_message(self, messages: list[dict[str, str]]):
        try:
            typed_messages = cast(list[ChatCompletionMessageParam], messages)
            if not self.api_key or not self.url or not self.model:
                self.failed.emit()
                raise RuntimeError("Missing API key, base URL, or model configuration")
            
            return self.AI_client.chat.completions.create(
                model = self.model,
                messages=typed_messages,
            )

            self.reply_ready.emit()
        except AuthenticationError:
            self.failed.emit()
            raise RuntimeError("Invalid/missing API key, check your configuration")
        except APIError as e:
            self.failed.emit()
            raise RuntimeError(f"AI request failed: {e}")
            

    def reload_configuration(self):
        self.api_key = self.configuration['api_key']
        self.url     = self.configuration['url']
        self.model   = self.configuration['model']
        
        # reset ai client with new config.
        self.AI_client = OpenAI(
            base_url = self.url,
            api_key  = self.api_key
        )

