from PySide6 import QtWidgets, QtCore
from flipper.ui.ui_config_view import Ui_ConfigView
from flipper.ui.chat_view import ChatView
from flipper.ui.edu_view import EduView
from flipper.services.config_service import ConfigService

class ConfigView(QtWidgets.QWidget):
    updated = QtCore.Signal()
    def __init__(self):
        super().__init__()
        self.ui = Ui_ConfigView()
        self.ui.setupUi(self)
        self.updated.connect(self.reload_page)

        #read config
        self.config_svc = ConfigService()
        self.configuration = self.config_svc.loaded_config

        #load values into textboxes
        self.ui.txt_apiKey.setText(self.configuration['API_KEY'])
        self.ui.txt_URL.setText(self.configuration['base_url'])
        self.ui.txt_modelName.setText(self.configuration['model'])

        # configure the save button
        self.ui.btn_save.clicked.connect(self.save_config)

    def save_config(self):
        api_key = self.ui.txt_apiKey.text()
        url     = self.ui.txt_URL.text()
        model   = self.ui.txt_modelName.text()

        if api_key == None or api_key == '':
            api_key = "local"

        new_config = self.configuration
        new_config["API_KEY"] = api_key
        new_config["base_url"]= url
        new_config["model"]   = model

        print("Saving new configuration")
        self.config_svc.save_settings(new_config)
        self.updated.emit()

    def reload_page(self):
        self.ui.txt_apiKey.setText(self.configuration['API_KEY'])
        self.ui.txt_URL.setText(self.configuration['base_url'])
        self.ui.txt_modelName.setText(self.configuration['model'])
    




