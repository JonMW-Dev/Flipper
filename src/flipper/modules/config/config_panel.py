from datetime import datetime
from PySide6 import QtWidgets, QtCore
from .ui_config_view import Ui_ConfigView

class ConfigPanel(QtWidgets.QWidget):

    def __init__(self, data_model):
        super().__init__()

        self.data_model = data_model

        self.ui = Ui_ConfigView()
        self.ui.setupUi(self)
        self.data_model.updated.connect(self.reload_page)

        self.current_config = self.data_model.get_current_config()



        
        #load values into textboxes
        self.ui.txt_apiKey.setText(self.current_config['api_key'])
        self.ui.txt_URL.setText(self.current_config['url'])
        self.ui.txt_modelName.setText(self.current_config['model'])

        # configure the save button
        self.ui.btn_save.clicked.connect(self.save_config)

    

    def reload_page(self):
        self.current_config = self.data_model.get_latest_config()
        self.ui.txt_apiKey.setText(self.current_config['api_key'])
        self.ui.txt_URL.setText(self.current_config['url'])
        self.ui.txt_modelName.setText(self.current_config['model'])
    


    def save_config(self):
        self.data_model.api_key = self.ui.txt_apiKey.text()
        self.data_model.url     = self.ui.txt_URL.text()
        self.data_model.model   = self.ui.txt_modelName.text()

        if self.data_model.api_key == None or self.data_model.api_key == '':
            self.data_model.api_key = "local"



        self.data_model.save_config()
        
        print("Saving new configuration")

    