# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edu_view.ui'
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
from PySide6.QtWidgets import (QApplication, QLineEdit, QListView, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_eduView(object):
    def setupUi(self, eduView):
        if not eduView.objectName():
            eduView.setObjectName(u"eduView")
        eduView.resize(1017, 650)
        self.verticalLayout = QVBoxLayout(eduView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.w_list_courseList = QListView(eduView)
        self.w_list_courseList.setObjectName(u"w_list_courseList")

        self.verticalLayout.addWidget(self.w_list_courseList)

        self.txtBox_courseName = QLineEdit(eduView)
        self.txtBox_courseName.setObjectName(u"txtBox_courseName")

        self.verticalLayout.addWidget(self.txtBox_courseName)

        self.btn_addCourse = QPushButton(eduView)
        self.btn_addCourse.setObjectName(u"btn_addCourse")

        self.verticalLayout.addWidget(self.btn_addCourse)


        self.retranslateUi(eduView)

        QMetaObject.connectSlotsByName(eduView)
    # setupUi

    def retranslateUi(self, eduView):
        eduView.setWindowTitle(QCoreApplication.translate("eduView", u"Form", None))
        self.btn_addCourse.setText(QCoreApplication.translate("eduView", u"Add new course", None))
    # retranslateUi

