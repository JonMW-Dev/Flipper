from PySide6 import QtWidgets, QtCore
from flipper.ui.ui_edu_view import Ui_eduView
from flipper.models.edu_model import eduModel
from flipper.ui.ui_question_view import Ui_questionView
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

        #setup submit button
        self.ui.btn_submit.clicked.connect(self.add_question)

    def add_question(self):
        course   = self.ui.lbl_course.text()
        question = self.ui.text_question.toPlainText()
        answer   = self.ui.text_answer.toPlainText()

        # connect to test_bank service and query the db
        print("Sending query to db_service")
        db_service = TestBank()
        result = db_service.add_question(course, question, answer)
        print(result)
        self.saved.emit()



class PanelWidget(QtWidgets.QWidget):
    bank_changed = QtCore.Signal()

    def __init__(self, course: str, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.addWidget(QtWidgets.QLabel(course))
        layout.addStretch()
        self.course_name = course

        # determine percent of valid questions in bank
        db_service = TestBank()
        invalid_count = db_service.get_invalid_count(self.course_name)
        valid_count = db_service.get_total_count(self.course_name)
        
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

            #query the bot for a false answer
            client = AIChatController()
            response = client.send_message(prompt)
            response_msg = response.choices[0].message.content
            if response_msg is None:
                raise RuntimeError("Error: no response received")

            #add the false answer to f
            print(f"AI response: {response_msg}")
            db_service.add_false_answer(db_id, db_f, response_msg) 