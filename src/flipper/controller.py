
# The Controller owns the modules and provides them to the main window
from flipper.modules.chat.chat_module import ChatModule
from flipper.services.chat_service import ChatService
from flipper.modules.config.config_module import ConfigModule
from flipper.data_access.data_access import DataAccessService
from flipper.modules.edu.edu_module import EduModule
class MainController():
    def __init__(self, data_services: dict[str,DataAccessService]):


        #report DAS names 
        if data_services != None:
            DAS_names = data_services.keys()
            print(f"MainController: Application reports the following DAS services: \n\t{DAS_names}")
        else:
            print(f"MainController: Application has no DAS services to report.")

        # Any module requiring a DAS is built here

        self.config_module  = ConfigModule(data_services["config"])
        self.current_config = self.config_module.get_current_config()

        # Creates shared chat service
        self.chat_service = ChatService(self.current_config)
        self.edu_module     = EduModule(data_services["courses"], data_services["testbank"], self.chat_service)
        






        # Creates Modules
        self.chat_module = ChatModule(self.chat_service)

        # connect config update signal
        self.config_module.config_panel.updated.connect(self.update_config)

    def get_chat_panel(self):
        return  self.chat_module.get_chat_panel()

    def get_edu_panel(self):
        return self.edu_module.get_edu_panel()

    def get_config_panel(self):
        return self.config_module.get_config_panel()
    
    def update_config(self):
        new_config = self.config_module.get_current_config()
        self.current_config.clear()
        self.current_config.update(new_config)
        self.chat_service.reload_configuration()
    
