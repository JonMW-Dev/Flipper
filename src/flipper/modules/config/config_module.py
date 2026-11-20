from .config_panel import ConfigPanel

class ConfigModule():
    def __init__(self, DAS):
        self.data_service = DAS

        self.config_panel = ConfigPanel(self.data_service)

    def get_config_panel(self):
        return self.config_panel

    def get_current_config(self):
        return self.config_panel.current_config

    