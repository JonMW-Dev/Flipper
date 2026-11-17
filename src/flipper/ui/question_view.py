from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QEvent, Qt
from flipper.ui.generated.ui_question_view import Ui_questionView
from flipper.services.testbank_service import TestBankService

class QuestionView(QtWidgets.QWidget):
    saved = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_questionView()
        self.ui.setupUi(self)

        #setup EventFilter to allow for easier QnA entry
        self.ui.text_question.installEventFilter(self)
        self.ui.text_answer.installEventFilter(self)

        #set Focus to questions textbox
        self.ui.text_question.setFocus()

        #setup submit button
        self.ui.btn_submit.clicked.connect(self.add_question)

        #setup done button
        self.ui.btn_done.clicked.connect(self.done)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if obj is self.ui.text_question:
                self.ui.text_answer.setFocus()
                return True
            if obj is self.ui.text_answer:
                self.add_question()
                return True
        return super().eventFilter(obj, event)

            


    def add_question(self):
        course   = self.ui.lbl_course.text()
        question = self.ui.text_question.toPlainText()
        answer   = self.ui.text_answer.toPlainText()

        # connect to test_bank service and query the db
        print("Sending query to db_service")
        db_service = TestBankService()
        result = db_service.add_question(course, question, answer)
        print(result)

        # clear textboxes
        self.ui.text_answer.clear()
        self.ui.text_question.clear()

        self.ui.text_question.setFocus()
    
    def done(self):
        self.saved.emit()