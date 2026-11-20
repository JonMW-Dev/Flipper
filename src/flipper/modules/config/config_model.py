from PySide6.QtCore import QAbstractListModel
from PySide6 import QtCore
from datetime import datetime

# holds data for config module. 

class ConfigModel(QAbstractListModel):
    updated = QtCore.Signal()
    api_key = ''
    url     = ''
    model   = ''

    def __init__(self, data_service):
        super().__init__()
        self.data_service = data_service

        self.current_config = self.get_latest_config()
        self.api_key = self.current_config["api_key"]
        self.url     = self.current_config['url']
        self.model   = self.current_config['model']



    def get_current_config(self):
         self.current_config['api_key'] = self.api_key
         self.current_config['url']     = self.url
         self.current_config['model']   = self.model

         return self.current_config
    
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
         
        data: dict = {
            "api_key": self.api_key,
            "url": self.url,
            "model": self.model
        }
        self.data_service.insert(data)


        self.updated.emit()


    
    

