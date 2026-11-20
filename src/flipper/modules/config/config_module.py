from .config_panel import ConfigPanel
from .config_model import ConfigModel
class ConfigModule():
    def __init__(self, data_service):
        self.data_service = data_service

        self.config_model = ConfigModel(self.data_service)
        self.config_panel = ConfigPanel(self.config_model)

    def get_config_panel(self):
        return self.config_panel

    def get_current_config(self):
        return self.config_model.get_current_config()

    