
import json
from pathlib import Path
from PySide6.QtCore import QObject, Signal
from PySide6 import QtCore
from platformdirs import user_config_dir
from flipper.consts import APP_NAME, APP_AUTHOR, CONFIG_DEFAULTS
class ConfigService(QObject):
    saved = QtCore.Signal()
    def __init__(self):
        super().__init__()

        # load config
        # Setup AI configuration files
        self.saved.connect(self.refresh_config)
        print("Config Service: Checking for flipper_config.json")
        self.config_dir = Path(user_config_dir(APP_NAME, APP_AUTHOR))
        print(f"Config Service: Loading config from: {self.config_dir}")
        self.config_file = self.config_dir / "flipper_config.json"
        self.loaded_config = self.load_settings(self.config_dir, self.config_file)
        if self.loaded_config == -1:
            exit(1)
        print(f"Config Service: Config accessible at: {self.config_file}")
        

    def load_settings(self, config_dir, config_file) -> dict:
        try:
            if not config_file.exists() or config_file.stat().st_size == 0:
                print("Config Service: config file not found or is empty.. creating default config")
                config_dir.mkdir(parents=True, exist_ok=True)
                config_file.write_text(json.dumps(CONFIG_DEFAULTS, indent = 2))
            data = json.loads(config_file.read_text())
            if not isinstance(data, dict):
                raise ValueError("Config Service: settings file is not an object")
            # start from defaults, overlay only known keys (or do a deeper merge)
            return {**CONFIG_DEFAULTS, **data}
        except (json.JSONDecodeError, OSError, ValueError) as e:
            # log the problem, fall back to defaults
            print(f"Config Service: Failed to load settings: {e}")
            return -1

    def save_settings(self, configuration: dict)->int:
        try:
            if not self.config_file.exists():
                raise FileNotFoundError("Config Service: Could not save, file not found.. restart application")
            self.config_file.write_text(json.dumps(configuration, indent = 2))

        except (json.JSONDecodeError, OSError, ValueError) as e:
            # log the problem, fall back to defaults
            print(f"Config Service: Failed to save settings: {e}")
            return -1

        self.saved.emit()
        return 0

    def refresh_config(self):
        print("Config Service: refreshing loaded configuration")
        self.loaded_config = self.load_settings(self.config_dir, self.config_file)
        print(f"Config Service: configuration updated at {self.config_file}")

    def get_config(self) -> dict:
        return self.loaded_config

    
