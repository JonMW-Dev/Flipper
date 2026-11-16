import random
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QThreadPool, Qt, QEvent
from PySide6.QtWidgets import QMessageBox, QButtonGroup
from flipper.ui.ui_edu_view import Ui_eduView
from flipper.models.edu_model import eduModel
from flipper.ui.ui_question_view import Ui_questionView
from flipper.ui.ui_test_view import Ui_testView
from flipper.services.test_bank import TestBank
from flipper.services.chat_client import AIChatController


class eduView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # setup GUI 
        self.ui = Ui_eduView()
        self.ui.setupUi(self)
        # setup List view to list added courses
        self.model = eduModel()
        # setup course delegate
        self.ui.w_list_courseList.setItemDelegate(CourseRowDelegate(self.ui.w_list_courseList))
        self.ui.w_list_courseList.setModel(self.model)
        # A saved question asks the model to reload. The reload emits modelReset,
        # which discards the row widgets, so they are built again afterwards.
        self.model.modelReset.connect(self.show_all_rows)
        for row in range(self.model.rowCount()):
            self.attach_row(row)

        #Listen for when new rows are inserted and refresh list
        self.model.rowsInserted.connect(self.show_new_rows)

        # setup add course button
        self.ui.btn_addCourse.clicked.connect(self.add_course)

    # opens a new window where the user can add a new course
    def add_course(self):
        self.model.add_course(self.ui.txtBox_courseName.text())

    def show_new_rows(self, parent, first, last):
        for row in range(first, last + 1):
            self.attach_row(row)

    def show_all_rows(self):
        for row in range(self.model.rowCount()):
            self.attach_row(row)

    def attach_row(self, row: int):
        index = self.model.index(row, 0)
        course = self.model.data(index)
        widget = PanelWidget(course)
        # singleShot returns first, so the model resets after the row signal finishes.
        widget.bank_changed.connect(self.schedule_refresh)
        self.ui.w_list_courseList.setIndexWidget(index, widget)

    def schedule_refresh(self):
        QtCore.QTimer.singleShot(0, self.model.refresh)

class CourseRowDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        return

    def sizeHint(self, option, index):
        return QtCore.QSize(200, 48)

class questionView(QtWidgets.QWidget):
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
        if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter):
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
        db_service = TestBank()
        result = db_service.add_question(course, question, answer)
        print(result)

        # clear textboxes
        self.ui.text_answer.clear()
        self.ui.text_question.clear()

        self.ui.text_question.setFocus()
    
    def done(self):
        self.saved.emit()

class testView(QtWidgets.QWidget):
    test_completed = QtCore.Signal()
    def __init__(self, questions: list[int]):
        super().__init__()
        #setup gui window
        self.ui = Ui_testView()
        self.ui.setupUi(self)
        completed = QtCore.Signal()

        # group radio buttons
        self.grp_answers = QButtonGroup()
        self.grp_answers.addButton(self.ui.answer_1)
        self.grp_answers.addButton(self.ui.answer_2)
        self.grp_answers.addButton(self.ui.answer_3)
        self.grp_answers.addButton(self.ui.answer_4)

        #self.completed.connect(self.display_score)
        self.question_list = questions
        self.total_q_count = len(self.question_list)
        print("init total_correct_answers")
        self.total_correct_answers = 0
        self.current_id = None

        #connect to db service
        self.db_service = TestBank()



        #Display question
        print(f"Question list from testView: {self.question_list}")
        if len(self.question_list) > 0:
            self.display_question(self.question_list.pop())
        else:
            #self.completed.emit()
            print("Test completed")    

        #setup submit button
        self.ui.btn_submitAnswer.clicked.connect(self.submit_answer)

    # TODO - Display question relies on the format of the DB structure remaining
    # constant. This function should not have to know the structure of the DB.
    # This function should request answers for the id, and the testbank service
    # scrambles them, after asking for the answers from the DAS. 

    def display_question(self, id: int):
        #set current_id variable to id
        self.current_id = id
        #get question data
        data_tuple = self.db_service.get_data_byId(self.current_id)
        
        #display question data on window
        self.ui.lbl_question.setText(data_tuple[2])
        answer_choices: list[str] = []
        answer_choices.append(data_tuple[3])
        answer_choices.append(data_tuple[4])
        answer_choices.append(data_tuple[5])
        answer_choices.append(data_tuple[6])

        # scramble the questions
        answer_scrambled: list[str] = []
        while len(answer_choices) != 0:
            # select a random number between 0 and length of list-1
            index = random.randint(0, len(answer_choices)-1)
            answer_scrambled.append(answer_choices.pop(index))

        # display answers into radio buttons
        self.ui.answer_1.setText(answer_scrambled[0])
        self.ui.answer_2.setText(answer_scrambled[1])
        self.ui.answer_3.setText(answer_scrambled[2])
        self.ui.answer_4.setText(answer_scrambled[3])            

    def submit_answer(self):
        #get string held by answer selected
        selected_answer = self.grp_answers.checkedButton().text()
        data_tuple = ()
        if selected_answer:
            data_tuple = self.db_service.get_data_byId(self.current_id)
            correct_answer = data_tuple[3]

            if data_tuple[7] == None:
                data_correct = 0
            else:
                data_correct = data_tuple[7]

            if data_tuple[8] == None:
                data_attempt = 0
            else:
                data_attempt = data_tuple[8]
            
            
            print(f"Selected Answer: {selected_answer} | Correct Answer: {correct_answer}")
            if selected_answer == correct_answer:
                self.total_correct_answers += 1
                
                data_correct += 1
                print(f"Updating {self.current_id} correct col with: {data_correct}")
                self.db_service.add_data(self.current_id, "correct", data_correct)

            # update attempt count
            data_attempt += 1
            print(f"Updating {self.current_id} attempts col with: {data_attempt}")
            self.db_service.add_data(self.current_id, "attempts", data_attempt)


        #deselect radio buttons
        self.grp_answers.setExclusive(False)
        for button in self.grp_answers.buttons():
            button.setChecked(False)
        self.grp_answers.setExclusive(True)

        #check if answer matches that held by current_id
            #if yes increment correct col by 1
        #increment attempt by 1

        #update the display and end test if no more questions exist
        if len(self.question_list) > 0:
            self.display_question(self.question_list.pop())
        else:
            self.test_completed.emit()
            print(f"Correct: {self.total_correct_answers} | Total Questions: {self.total_q_count}")
            score = (self.total_correct_answers/self.total_q_count) * 100
            QMessageBox.information(self, "SCORE_PLACEHOLDER", f"Test completed, score: {score}%")
    

    


class PanelWidget(QtWidgets.QWidget):
    bank_changed = QtCore.Signal()

    def __init__(self, course: str, parent=None):
        
        super().__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.addWidget(QtWidgets.QLabel(course))
        layout.addStretch()
        self.course_name = course
        
        #setup thread pool so GUI stays responsive during db validation
        self.threadpool = QThreadPool()
        self.db_service = TestBank()
        
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
        self.q_view = questionView()
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
        db_service = TestBank()
        f_answer: dict[str, bool | None] = {
            "f1": None,
            "f2": None,
            "f3": None
        }
        # get list of invalid db entries
        invalid_list = db_service.get_invalid_list(self.course_name)

        pending_work: list[list[int,str]] = []
        # for each invalid entry id, find each missing f and add to work list
        for id in invalid_list:
            for f in f_answer:
                check = db_service.check_col(id, f)
                if not check:
                    pending_work.append([id, f])

        self.threadpool.start(
            lambda: self.fill_missing_answers(pending_work)
        )
            
    # to be called on a new thread - Sends messages to ai and receives responses
    def fill_missing_answers(self, pending_work):
        db_service = TestBank()
        client = AIChatController()

        # call the AI to fill in the missing f's
        for task in pending_work:
            #db_id, db_f = next(iter(task.items()))
            db_id = task[0]
            db_f  = task[1]
            #get the question and answer for the id
            qa_tuple = db_service.get_QA_byId(db_id)
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
            response = client.send_message(prompt)

            response_msg = response.choices[0].message.content
            if response_msg is None:
                raise RuntimeError("Error: no response received")

            #add the false answer to f
            print(f"AI response: {response_msg}")
            db_service.add_false_answer(db_id, db_f, response_msg) 
        
        self.bank_changed.emit()

    #opens a test window 
    def take_test(self):


        #collect id's of valid questions for course
        valid_questions: list[int] = self.db_service.get_valid_list(self.course_name)
        print(f"List of valid id's: {valid_questions}")

        #create test_view
        self.test_window = testView(valid_questions)
        self.test_window.test_completed.connect(self.test_completed)
        # self.bank_changed.emit()
        self.test_window.show()

    def test_completed(self):
        self.test_window.close()
        self.bank_changed.emit()
