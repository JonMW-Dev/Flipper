from PySide6 import QtWidgets, QtCore
from flipper.controller import MainController
from flipper.ui.generated.ui_main_window import Ui_MainWindow
from flipper.data_access.data_access import DataAccessService


# Defines the main window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set up the NavBar
        spacer = QtWidgets.QWidget()
        spacer.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        spacer.setSizePolicy ( #sets the spacer to dynamic spacing
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.ui.navBar.insertWidget(self.ui.actionConfig, spacer)
        self.ui.actionHome.triggered.connect(self.show_home) # go to home
        self.ui.actionChat.triggered.connect(self.show_chat) # go to AI chat 
        self.ui.actionEducation.triggered.connect(self.show_edu) # go to Edu page
        self.ui.actionConfig.triggered.connect(self.show_config)
        self.ui.actionQuit.triggered.connect(QtWidgets.QApplication.quit) # terminate the application
        
        data_services: dict[str, DataAccessService] = {
            "config": DataAccessService("configurations.db", "ai_chat_config"),
            "courses"   : DataAccessService("education.db", "courses"),
            "testbank"  : DataAccessService("education.db", "testbank"),
        }
        # The window must keep the controller. A local variable is collected, and the
        # config updated slot is disconnected with it.
        self.controller = MainController(data_services)

        # get module panels from the controller and add to the stack widget
        self.chat_panel = self.controller.get_chat_panel()
        self.edu_panel  = self.controller.get_edu_panel()
        self.config_panel  = self.controller.get_config_panel()

        # connect panels to the stack widget layouts
        self.ui.verticalLayout.addWidget(self.chat_panel)
        self.ui.verticalLayout_2.addWidget(self.edu_panel)
        self.ui.verticalLayout_4.addWidget(self.config_panel)


        pass

    # TODO - The self.ui.___Page calls need to be changed to the panels created in the modules
    # Show the home panel NOTE The panels are known by the stack as pages,
    # so this change occurs in Designer


    def show_home(self):
        self.ui.viewStack.setCurrentWidget(self.ui.homePage)

    # Show the chat panel
    def show_chat(self):
        self.ui.viewStack.setCurrentWidget(self.ui.chatPage)

    # Show the edu panel
    def show_edu(self):
        self.ui.viewStack.setCurrentWidget(self.ui.eduPage)

    # Show the config panel
    def show_config(self):
        self.ui.viewStack.setCurrentWidget(self.ui.configPage)
    pass