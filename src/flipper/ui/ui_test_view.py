# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_view.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QRadioButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_testView(object):
    def setupUi(self, testView):
        if not testView.objectName():
            testView.setObjectName(u"testView")
        testView.resize(560, 300)
        self.verticalLayout = QVBoxLayout(testView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lbl_question = QLabel(testView)
        self.lbl_question.setObjectName(u"lbl_question")

        self.verticalLayout.addWidget(self.lbl_question)

        self.answer_1 = QRadioButton(testView)
        self.answer_1.setObjectName(u"answer_1")

        self.verticalLayout.addWidget(self.answer_1)

        self.answer_2 = QRadioButton(testView)
        self.answer_2.setObjectName(u"answer_2")

        self.verticalLayout.addWidget(self.answer_2)

        self.answer_3 = QRadioButton(testView)
        self.answer_3.setObjectName(u"answer_3")

        self.verticalLayout.addWidget(self.answer_3)

        self.answer_4 = QRadioButton(testView)
        self.answer_4.setObjectName(u"answer_4")

        self.verticalLayout.addWidget(self.answer_4)

        self.btn_submitAnswer = QPushButton(testView)
        self.btn_submitAnswer.setObjectName(u"btn_submitAnswer")

        self.verticalLayout.addWidget(self.btn_submitAnswer)


        self.retranslateUi(testView)

        QMetaObject.connectSlotsByName(testView)
    # setupUi

    def retranslateUi(self, testView):
        testView.setWindowTitle(QCoreApplication.translate("testView", u"Form", None))
        self.lbl_question.setText(QCoreApplication.translate("testView", u"TextLabel", None))
        self.answer_1.setText(QCoreApplication.translate("testView", u"RadioButton", None))
        self.answer_2.setText(QCoreApplication.translate("testView", u"RadioButton", None))
        self.answer_3.setText(QCoreApplication.translate("testView", u"RadioButton", None))
        self.answer_4.setText(QCoreApplication.translate("testView", u"RadioButton", None))
        self.btn_submitAnswer.setText(QCoreApplication.translate("testView", u"PushButton", None))
    # retranslateUi

