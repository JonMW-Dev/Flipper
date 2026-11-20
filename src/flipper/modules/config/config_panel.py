
from PySide6 import QtWidgets


from pathlib import Path
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtCore import QUrl

class ConfigPanel(QtWidgets.QWidget):

    def __init__(self, data_model):
        super().__init__()

        self.data_model = data_model

        #self.ui = Ui_ConfigView()
        #self.ui.setupUi(self)

        # Hook up QML GUI
        qml_view = QQuickWidget() # create widget to hold the QML vew
        qml_view.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView) # 
        qml_path = Path(__file__).resolve().parent / "ConfigPanel.qml" # resolve the path to the qml file
        
        qml_view.rootContext().setContextProperty("configModel", self.data_model) # give name configModel to QML file and bind it to ConfigModel
        qml_view.setSource(QUrl.fromLocalFile(str(qml_path))) # set the source of the view to the file

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(qml_view)
        #self.ui.verticalLayout.insertWidget(0, qml_view) # insert widget in the verticalLayout of the self.ui. 


        #self.current_config = self.data_model.get_current_config()



        
        # #load values into textboxes
        # self.ui.txt_apiKey.setText(self.current_config['api_key'])
        # self.ui.txt_URL.setText(self.current_config['url'])
        # self.ui.txt_modelName.setText(self.current_config['model'])

        # # configure the save button
        # self.ui.btn_save.clicked.connect(self.save_config)

    







        # self.data_model.save_config()

        # print("Saving new configuration")

    