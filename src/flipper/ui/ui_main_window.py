# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QSizePolicy,
    QStackedWidget, QStatusBar, QToolBar, QVBoxLayout,
    QWidget)
from . import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(999, 600)
        self.actionHome = QAction(MainWindow)
        self.actionHome.setObjectName(u"actionHome")
        icon = QIcon()
        icon.addFile(u":/icons/Home_dm.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionHome.setIcon(icon)
        self.actionHome.setMenuRole(QAction.MenuRole.NoRole)
        self.actionChat = QAction(MainWindow)
        self.actionChat.setObjectName(u"actionChat")
        icon1 = QIcon()
        icon1.addFile(u":/icons/Chat_dm.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionChat.setIcon(icon1)
        self.actionChat.setMenuRole(QAction.MenuRole.NoRole)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionQuit.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.viewStack = QStackedWidget(self.centralwidget)
        self.viewStack.setObjectName(u"viewStack")
        self.homePage = QWidget()
        self.homePage.setObjectName(u"homePage")
        self.verticalLayout_3 = QVBoxLayout(self.homePage)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.homeLabel = QLabel(self.homePage)
        self.homeLabel.setObjectName(u"homeLabel")

        self.verticalLayout_3.addWidget(self.homeLabel)

        self.viewStack.addWidget(self.homePage)
        self.chatPage = QWidget()
        self.chatPage.setObjectName(u"chatPage")
        self.verticalLayout = QVBoxLayout(self.chatPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.chatLabel = QLabel(self.chatPage)
        self.chatLabel.setObjectName(u"chatLabel")

        self.verticalLayout.addWidget(self.chatLabel)

        self.viewStack.addWidget(self.chatPage)

        self.verticalLayout_2.addWidget(self.viewStack)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.navBar = QToolBar(MainWindow)
        self.navBar.setObjectName(u"navBar")
        self.navBar.setMovable(False)
        self.navBar.setFloatable(False)
        MainWindow.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.navBar)

        self.navBar.addAction(self.actionHome)
        self.navBar.addAction(self.actionChat)
        self.navBar.addAction(self.actionQuit)

        self.retranslateUi(MainWindow)

        self.viewStack.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionHome.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.actionChat.setText(QCoreApplication.translate("MainWindow", u"Chat", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.homeLabel.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.chatLabel.setText(QCoreApplication.translate("MainWindow", u"Chat", None))
        self.navBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

