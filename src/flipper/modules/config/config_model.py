from PySide6.QtCore import QObject, Signal, Property
from PySide6 import QtCore
from datetime import datetime

# holds data for config module. 

class ConfigModel(QObject):
    updated = Signal()
    api_key_changed = Signal()
    url_changed = Signal()
    model_changed = Signal()





    def __init__(self, data_service):
        super().__init__()
        self.data_service = data_service
        
        # define property value equiv variables (These hold the actual values of the named property)
        self._api_key = ''
        self._url     = ''
        self._model   = ''

        self.current_config = self.get_latest_config()

        # Set the config Properties to current configuration
        self.api_key = self.current_config["api_key"]
        self.url     = self.current_config['url']
        self.model   = self.current_config['model']


    def get_api_key(self):
         return self._api_key 

    def set_api_key(self, value):
         if self._api_key == value:
              return 
         self._api_key = value
         self.api_key_changed.emit()

    def get_url(self):
         return self._url

    def set_url(self, value):
         if self._url == value:
              return
         self._url = value
         self.url_changed.emit()

    def get_model(self):
         return self._model

    def set_model(self, value):
         if self._model == value:
              return
         self._model = value
         self.model_changed.emit()

    # set the properties
    api_key = Property(str, get_api_key, set_api_key, notify=api_key_changed)
    url     = Property(str, get_url, set_url, notify=url_changed)
    model   = Property(str, get_model, set_model, notify=model_changed)


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


    
    

