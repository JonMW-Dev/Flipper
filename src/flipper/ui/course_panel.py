from PySide6 import QtCore, QtWidgets
from flipper.services.testbank_service import TestBankService
from flipper.services.chat_service import ChatService
from PySide6.QtCore import QThreadPool
from flipper.ui.question_view import QuestionView
from flipper.ui.test_view import TestView


class CoursePanel(QtWidgets.QWidget):
    bank_changed = QtCore.Signal()
    validation_failed = QtCore.Signal()

    def __init__(self, course: str, parent=None):
        
        super().__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.addWidget(QtWidgets.QLabel(course))
        layout.addStretch()
        self.course_name = course
        
        #setup thread pool so GUI stays responsive during db validation
        self.threadpool = QThreadPool()
        self.db_service = TestBankService()
        
        # add reset score button
        btn_resetScore = QtWidgets.QPushButton("reset score")
        btn_resetScore.clicked.connect(self.reset_score)
        layout.addWidget(btn_resetScore)

        #add overall score label
        lbl_overallScore = QtWidgets.QLabel()
        overallScore = str(self.db_service.get_overall_score(self.course_name))
        
        if overallScore == "-1":
            overallScore = "no overall score"
        else:
            overallScore = overallScore + "%"
        
        lbl_overallScore.setText(f"{overallScore}  | ")
        layout.addWidget(lbl_overallScore)

        # determine percent of valid questions in bank

        invalid_count = self.db_service.get_invalid_count(self.course_name)
        valid_count = self.db_service.get_total_count(self.course_name)
        
        if valid_count > 0:
            percent_valid: str = str(((valid_count-invalid_count)/valid_count)*100)
        else: 
            percent_valid = "err"
        
        pcomplete = QtWidgets.QLabel(f"{percent_valid} % valid")
        layout.addWidget(pcomplete)
        


        
        #Add a validate DB button
        validate_btn = QtWidgets.QPushButton("validate bank")
        validate_btn.clicked.connect(self.validate_bank)
        layout.addWidget(validate_btn)

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
        self.q_view = QuestionView()
        self.q_view.ui.lbl_course.setText(
            f"{self.course_name}"
        )
        self.q_view.saved.connect(self.bank_changed)
        self.q_view.show()

    def reset_score(self):
        valid_list = self.db_service.get_valid_list(self.course_name)
        for row_id in valid_list:
            self.db_service.add_data(row_id, "correct", 0)
            self.db_service.add_data(row_id, "attempts", 0)
        self.bank_changed.emit() # update the course panels

    

    #sends each question and answer pair to the AI to generate f1-3
    def validate_bank(self):
        db_service = TestBankService()
        f_answer: dict[str, bool | None] = {
            "f1": None,
            "f2": None,
            "f3": None
        }
        # get list of invalid db entries
        invalid_list = db_service.get_invalid_list(self.course_name)

        pending_work: list[tuple[int , str]] = []
        # for each invalid entry id, find each missing f and add to work list
        for id in invalid_list:
            for f in f_answer:
                check = db_service.check_col(id, f)
                if not check:
                    pending_work.append((id, f))

        self.threadpool.start(
            lambda: self.fill_missing_answers(pending_work)
        )
            
    # to be called on a new thread - Sends messages to ai and receives responses
    def fill_missing_answers(self, pending_work: list[tuple[int, str]]):
        db_service = TestBankService()
        client = ChatService()

        # call the AI to fill in the missing f's
        for task in pending_work:
            #db_id, db_f = next(iter(task.items()))
            db_id = task[0]
            db_f  = task[1]
            #get the question and answer for the id
            qa_tuple = db_service.get_question_answer(db_id)
            if qa_tuple is None:
                self.validation_failed.emit(f"Error: no question/answer found for id {db_id}")
                break
            #build the prompt
            system_instruction = """
                You task is to provide the incorrect answer to the question.
                You have been provided the QUESTION and the CORRECT_ANSWER.
                You must respond by INCORRECTLY ANSWERING THE QUESTION. 
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

                #add the false answer to f
                print(f"AI response: {response_msg}")
                db_service.add_false_answer(db_id, db_f, response_msg) 
            except RuntimeError as error:
                self.validation_failed.emit(str(error))
                break

            
        self.bank_changed.emit()

    #opens a test window 
    def take_test(self):


        #collect id's of valid questions for course
        valid_questions: list[int] = self.db_service.get_valid_list(self.course_name)
        print(f"List of valid id's: {valid_questions}")

        #create test_view
        self.test_window = TestView(valid_questions)
        self.test_window.test_completed.connect(self.test_completed)
        # self.bank_changed.emit()
        self.test_window.show()

    def test_completed(self):
        self.test_window.close()
        self.bank_changed.emit()
