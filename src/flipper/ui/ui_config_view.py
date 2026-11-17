# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_view.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_ConfigView(object):
    def setupUi(self, ConfigView):
        if not ConfigView.objectName():
            ConfigView.setObjectName(u"ConfigView")
        ConfigView.resize(479, 334)
        self.verticalLayout = QVBoxLayout(ConfigView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lbl_apiKey = QLabel(ConfigView)
        self.lbl_apiKey.setObjectName(u"lbl_apiKey")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_apiKey)

        self.txt_apiKey = QLineEdit(ConfigView)
        self.txt_apiKey.setObjectName(u"txt_apiKey")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.txt_apiKey)

        self.txt_URL = QLineEdit(ConfigView)
        self.txt_URL.setObjectName(u"txt_URL")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.txt_URL)

        self.lbl_modelName = QLabel(ConfigView)
        self.lbl_modelName.setObjectName(u"lbl_modelName")
        self.lbl_modelName.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_modelName)

        self.txt_modelName = QLineEdit(ConfigView)
        self.txt_modelName.setObjectName(u"txt_modelName")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.txt_modelName)

        self.lbl_url = QLabel(ConfigView)
        self.lbl_url.setObjectName(u"lbl_url")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_url.sizePolicy().hasHeightForWidth())
        self.lbl_url.setSizePolicy(sizePolicy)
        self.lbl_url.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_url)


        self.verticalLayout.addLayout(self.formLayout)

        self.lbl_localInfo = QLabel(ConfigView)
        self.lbl_localInfo.setObjectName(u"lbl_localInfo")

        self.verticalLayout.addWidget(self.lbl_localInfo)

        self.btn_save = QPushButton(ConfigView)
        self.btn_save.setObjectName(u"btn_save")

        self.verticalLayout.addWidget(self.btn_save)


        self.retranslateUi(ConfigView)

        QMetaObject.connectSlotsByName(ConfigView)
    # setupUi

    def retranslateUi(self, ConfigView):
        ConfigView.setWindowTitle(QCoreApplication.translate("ConfigView", u"Form", None))
        self.lbl_apiKey.setText(QCoreApplication.translate("ConfigView", u"API_KEY", None))
        self.lbl_modelName.setText(QCoreApplication.translate("ConfigView", u"Model Name", None))
        self.lbl_url.setText(QCoreApplication.translate("ConfigView", u"URL", None))
        self.lbl_localInfo.setText(QCoreApplication.translate("ConfigView", u"Note: local AI URL form: http://localhost:PORT/v1 ", None))
        self.btn_save.setText(QCoreApplication.translate("ConfigView", u"Save Configuration", None))
    # retranslateUi

