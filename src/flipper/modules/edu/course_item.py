from PySide6 import QtWidgets
from PySide6.QtCore import QThreadPool
from .question_view import QuestionView
from .test_view import TestView


class CourseItem(QtWidgets.QWidget):
    def __init__(self, course: str, testbank_service, chat_service, notifier, parent=None):
        super().__init__(parent)
        self.chat_service = chat_service
        self.notifier = notifier
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.addWidget(QtWidgets.QLabel(course))
        layout.addStretch()
        self.course_name = course
        
        #setup thread pool so GUI stays responsive during db validation
        self.threadpool = QThreadPool()
        self.testbank_service = testbank_service
        
        # add reset score button
        btn_resetScore = QtWidgets.QPushButton("reset score")
        btn_resetScore.clicked.connect(self.reset_score)
        layout.addWidget(btn_resetScore)

        self.lbl_overall_score = QtWidgets.QLabel()
        layout.addWidget(self.lbl_overall_score)
        self.lbl_percent = QtWidgets.QLabel()
        layout.addWidget(self.lbl_percent)

        #Add a validate DB button
        self.validate_btn = QtWidgets.QPushButton("validate bank")
        self.validate_btn.clicked.connect(self.validate_bank)
        layout.addWidget(self.validate_btn)
        self.refresh_stats()

        #Add a "take test" button
        btn_takeTest = QtWidgets.QPushButton("Take Test")
        btn_takeTest.clicked.connect(self.take_test)
        layout.addWidget(btn_takeTest)

        #Add add questions button
        btn = QtWidgets.QPushButton("Add Questions")
        btn.clicked.connect(self.add_questions)
        layout.addWidget(btn)

    def add_questions(self):
        #Open new window
        self.q_view = QuestionView(self.testbank_service)
        self.q_view.ui.lbl_course.setText(
            f"{self.course_name}"
        )
        self.q_view.saved.connect(lambda: self.notifier.bank_changed.emit(self.course_name))
        self.q_view.show()

    def refresh_stats(self):
        self.validate_btn.setEnabled(True)
        overall_score = self.testbank_service.get_overall_score(self.course_name)
        if overall_score == -1:
            overall_score = "no overall score"
        else:
            overall_score = str(overall_score) + "%"
        self.lbl_overall_score.setText(f"{overall_score}  | ")

        invalid_count = self.testbank_service.get_invalid_count(self.course_name)
        total_count = self.testbank_service.get_total_count(self.course_name)
        if total_count > 0:
            percent_valid = str(((total_count - invalid_count) / total_count) * 100)
        else:
            percent_valid = "err"
        self.lbl_percent.setText(f"{percent_valid} % valid")

    def reset_score(self):
        valid_list = self.testbank_service.get_valid_list(self.course_name)
        for row_id in valid_list:
            self.testbank_service.update_data(row_id, "correct", 0)
            self.testbank_service.update_data(row_id, "attempts", 0)
        self.notifier.bank_changed.emit(self.course_name)

    

    # Fill any missing f1-f3 answers, then mark the row valid.
    def validate_bank(self):
        service = self.testbank_service
        pending_work: list[tuple[int, str]] = []
        for row_id in service.get_invalid_list(self.course_name):
            missing = [
                column for column in ("f1", "f2", "f3")
                if not service.check_col(row_id, column)
            ]
            if missing:
                pending_work.extend((row_id, column) for column in missing)
            else:
                service.update_data(row_id, "is_valid", 1)

        if pending_work:
            self.validate_btn.setEnabled(False) # don't allow user to click validate btn again while validating
            self.threadpool.start(lambda: self.fill_missing_answers(pending_work))
            return
        self.notifier.bank_changed.emit(self.course_name)
            
    # to be called on a new thread - Sends messages to ai and receives responses
    def fill_missing_answers(self, pending_work: list[tuple[int, str]]):
        db_service = self.testbank_service
        client = self.chat_service

        try:
            self._fill_missing_answers(pending_work, db_service, client)
        finally:
            self.notifier.bank_changed.emit(self.course_name)

    def _fill_missing_answers(self, pending_work, db_service, client):
        # call the AI to fill in the missing f's
        for task in pending_work:
            #db_id, db_f = next(iter(task.items()))
            db_id = task[0]
            db_f  = task[1]
            #get the question and answer for the id
            qa_tuple = db_service.get_question_answer(db_id)
            if qa_tuple is None:
                self.notifier.validation_failed.emit(f"Error: no question/answer found for id {db_id}")
                break
            #build the prompt
            system_instruction = """
                You task is to provide the incorrect answer to the question.
                You have been provided the QUESTION and the CORRECT_ANSWER.
                You must respond by INCORRECTLY ANSWERING THE QUESTION.
                Reply with only the incorrect answer, with no label or explanation.
            """
            qa_message = f"""
                QUESTION: {qa_tuple[0]}
                ANSWER: {qa_tuple[1]}
            """
            prompt: list[dict[str,str]] = [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": qa_message}
            ]
            try: 
                response = client.send_message(prompt)

                response_msg = response.choices[0].message.content
                if response_msg is None:
                    raise RuntimeError("Error: no response received")

                #add the false answer to f columns
                print(f"AI response: {response_msg}")
                db_service.add_false_answer(db_id, db_f, response_msg)
                if all(db_service.check_col(db_id, column) for column in ("f1", "f2", "f3")):
                    db_service.update_data(db_id, "is_valid", 1) 
            except Exception as error:
                self.notifier.validation_failed.emit(str(error))
                break

    #opens a test window 
    def take_test(self):


        #collect id's of valid questions for course
        valid_questions: list[int] = self.testbank_service.get_valid_list(self.course_name)
        print(f"List of valid id's: {valid_questions}")

        if not valid_questions:
            QtWidgets.QMessageBox.information(
                self,
                "No valid questions",
                "Validate the bank before taking a test.",
            )
            return

        #create test_view
        self.test_window = TestView(valid_questions, self.testbank_service)
        self.test_window.test_completed.connect(self.test_completed)
        # self.bank_changed.emit()
        self.test_window.show()

    def test_completed(self):
        self.test_window.close()
        self.notifier.bank_changed.emit(self.course_name)
