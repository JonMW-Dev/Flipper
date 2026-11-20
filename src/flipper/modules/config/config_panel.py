from datetime import datetime
from PySide6 import QtWidgets, QtCore
from .ui_config_view import Ui_ConfigView

class ConfigPanel(QtWidgets.QWidget):
    updated = QtCore.Signal()
    def __init__(self, data_service):
        super().__init__()
        self.data_service = data_service

        self.ui = Ui_ConfigView()
        self.ui.setupUi(self)
        self.updated.connect(self.reload_page)

        #read config
        # self.config_svc = ConfigService()
        # self.configuration = self.config_svc.loaded_config
        self.current_config = self.get_latest_config()

        #load values into textboxes
        self.ui.txt_apiKey.setText(self.current_config['api_key'])
        self.ui.txt_URL.setText(self.current_config['url'])
        self.ui.txt_modelName.setText(self.current_config['model'])

        # configure the save button
        self.ui.btn_save.clicked.connect(self.save_config)

    def get_latest_config(self) -> dict:
        latest_config: datetime = datetime(2025,1,1,1,1,1)
        ts_index = None
        configurations: list = self.data_service.get_all()
        if not configurations:
            print(f"ConfigPanel: The table {self.data_service.table_name} in {self.data_service.database} is empty")
            return {
                'api_key': 'null',
                'url': 'Null',
                'model': 'Null'
            }
        
        col_names = configurations[0].keys()

        target_row = 0
        for row, index in enumerate(configurations):
            timestamp = index[1]
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            if dt > latest_config:
                latest_config = dt
                target_row = row
                ts_index = index

        result = {}
        index = 0

        if ts_index == None:
            raise ValueError("ConfigPanel:Error: The reported timestamp for the latest config is None")

        
        for column in col_names:
            result[column] = configurations[target_row][index]
            index += 1

        return result

    def save_config(self):
        api_key = self.ui.txt_apiKey.text()
        url     = self.ui.txt_URL.text()
        model   = self.ui.txt_modelName.text()

        if api_key == None or api_key == '':
            api_key = "local"
        data: dict = {
            "api_key": api_key,
            "url": url,
            "model": model
        }

        self.data_service.insert(data)

        print("Saving new configuration")
        self.updated.emit()

    def reload_page(self):
        self.current_config = self.get_latest_config()
        self.ui.txt_apiKey.setText(self.current_config['api_key'])
        self.ui.txt_URL.setText(self.current_config['url'])
        self.ui.txt_modelName.setText(self.current_config['model'])
    


