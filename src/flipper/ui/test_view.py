from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QMessageBox, QButtonGroup
from flipper.ui.generated.ui_test_view import Ui_testView
from flipper.services.testbank_service import TestBankService
import random

class TestView(QtWidgets.QWidget):
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
        self.db_service = TestBankService()



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
        data_tuple = self.db_service.get_row(self.current_id)
        
        #display question data on window
        if data_tuple is None:
            raise RuntimeError(f"Error: no data found for id {self.current_id}")
        
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
        checked_button = self.grp_answers.checkedButton()
        if checked_button is None:
            QMessageBox.warning(self, "No answer selected", "Please select an answer before submitting.")
            return
        
        selected_answer = checked_button.text()

        data_tuple = ()
        if selected_answer and self.current_id:
            data_tuple = self.db_service.get_row(self.current_id)
            if data_tuple is None:
                raise RuntimeError(f"Error: no data found for id {self.current_id}")
            
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
    
