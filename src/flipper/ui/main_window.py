from PySide6 import QtWidgets, QtCore
from flipper.ui.ui_main_window import Ui_MainWindow
from flipper.ui.chat_view import ChatWidget
from flipper.ui.edu_view import eduView

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # add dynamic spacer to set the Exit button at the bottom of the navBar
        spacer = QtWidgets.QWidget()
        spacer.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        spacer.setSizePolicy ( #sets the spacer to dynamic spacing
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        self.ui.navBar.insertWidget(self.ui.actionQuit, spacer) #insert spacer before actionQuit

        self.ui.actionHome.triggered.connect(self.show_home) # go to home
        self.ui.actionChat.triggered.connect(self.show_chat) # go to AI chat 
        self.ui.actionEducation.triggered.connect(self.show_edu) # go to Edu page
        self.ui.actionQuit.triggered.connect(QtWidgets.QApplication.quit) # terminate the application


        # Add the chat view
        self.chat_view = ChatWidget()
        self.ui.chatLabel.hide()
        self.ui.verticalLayout.addWidget(self.chat_view)

        self.edu_view = eduView()
        self.ui.label.hide()
        self.ui.verticalLayout_2.addWidget(self.edu_view)

    def show_home(self):
        self.ui.viewStack.setCurrentWidget(self.ui.homePage)

    def show_chat(self):
        self.ui.viewStack.setCurrentWidget(self.ui.chatPage)

    def show_edu(self):
        self.ui.viewStack.setCurrentWidget(self.ui.eduPage)