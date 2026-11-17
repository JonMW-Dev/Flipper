# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'question_view.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_questionView(object):
    def setupUi(self, questionView):
        if not questionView.objectName():
            questionView.setObjectName(u"questionView")
        questionView.resize(400, 300)
        self.verticalLayout = QVBoxLayout(questionView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lbl_course = QLabel(questionView)
        self.lbl_course.setObjectName(u"lbl_course")

        self.verticalLayout.addWidget(self.lbl_course)

        self.label_q = QLabel(questionView)
        self.label_q.setObjectName(u"label_q")

        self.verticalLayout.addWidget(self.label_q)

        self.text_question = QTextEdit(questionView)
        self.text_question.setObjectName(u"text_question")

        self.verticalLayout.addWidget(self.text_question)

        self.label_a = QLabel(questionView)
        self.label_a.setObjectName(u"label_a")

        self.verticalLayout.addWidget(self.label_a)

        self.text_answer = QTextEdit(questionView)
        self.text_answer.setObjectName(u"text_answer")

        self.verticalLayout.addWidget(self.text_answer)

        self.btn_submit = QPushButton(questionView)
        self.btn_submit.setObjectName(u"btn_submit")

        self.verticalLayout.addWidget(self.btn_submit)

        self.btn_done = QPushButton(questionView)
        self.btn_done.setObjectName(u"btn_done")

        self.verticalLayout.addWidget(self.btn_done)


        self.retranslateUi(questionView)

        QMetaObject.connectSlotsByName(questionView)
    # setupUi

    def retranslateUi(self, questionView):
        questionView.setWindowTitle(QCoreApplication.translate("questionView", u"Form", None))
        self.lbl_course.setText(QCoreApplication.translate("questionView", u"Course Lable (lbl_course)", None))
        self.label_q.setText(QCoreApplication.translate("questionView", u"Question:", None))
        self.label_a.setText(QCoreApplication.translate("questionView", u"Answer:", None))
        self.btn_submit.setText(QCoreApplication.translate("questionView", u"Add to test bank", None))
        self.btn_done.setText(QCoreApplication.translate("questionView", u"Done", None))
    # retranslateUi

