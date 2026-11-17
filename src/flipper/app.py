# Date: 14/11/26 | Author: Jonathan Windle
# main executed file for FlipperAI project 

# We will initially use this project to learn Qt/Pyside6 for GUI. 
import sys
import json
from pathlib import Path
from platformdirs import user_config_dir
from flipper.consts import APP_NAME, APP_AUTHOR, CONFIG_DEFAULTS

from PySide6 import QtWidgets
from flipper.ui.main_window import MainWindow
def main():
    application = QtWidgets.QApplication([])

    # Setup AI configuration files
    print("Checking for flipper_config.json")
    config_dir = Path(user_config_dir(APP_NAME, APP_AUTHOR))
    print(f"Loading config from: {config_dir}")
    config_file = config_dir / "flipper_config.json"
    loaded_config = load_settings(config_dir, config_file)
    if loaded_config == -1:
        exit(1)
    print(f"Config accessible at: {config_file}")
    print(loaded_config)

    widget = MainWindow()
    widget.resize(900, 600)
    widget.show()

    sys.exit(application.exec())

def load_settings(config_dir, config_file) -> dict:
    try:
        if not config_file.exists() or config_file.stat().st_size == 0:
            print("config file not found or is empty.. creating default config")
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file.write_text(json.dumps(CONFIG_DEFAULTS, indent = 2))
        data = json.loads(config_file.read_text())
        if not isinstance(data, dict):
            raise ValueError("settings file is not an object")
        # start from defaults, overlay only known keys (or do a deeper merge)
        return {**CONFIG_DEFAULTS, **data}
    except (json.JSONDecodeError, OSError, ValueError) as e:
        # log the problem, fall back to defaults
        print(f"Failed to load settings: {e}")
        return -1
    
if __name__ == "__main__":
    main()

