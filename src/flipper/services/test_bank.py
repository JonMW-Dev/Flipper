from flipper.data_access.question_repository import QuestionRepository


class TestBank:
    """Saves a question for a course. The window calls this, not the database."""

    def __init__(self, questions: QuestionRepository | None = None):
        self.questions = questions if questions is not None else QuestionRepository()

    def add_question(self, course: str, question: str, answer: str) -> int:
        course = course.strip()
        question = question.strip()
        answer = answer.strip()
        if not course or not question or not answer:
            raise ValueError("A course, question, and answer are required.")
        return self.questions.insert(course, question, answer)

    def add_data(self, row_id: int, column: str, value: int | str):
        if column not in ["f1", "f2", "f3", "correct", "attempts"]:
            raise ValueError("Invalid column name provided")

        if column in {"correct", "attempts"} and isinstance(value, str):
            raise ValueError(f"The column {column} cannot be a string: {value}")

        return self.questions.insert_cell(row_id, column, value)

    def get_data_byId(self, row_id: int) -> tuple:
        return self.questions.get(row_id)

    def add_false_answer(self, id: int, f_id: str, value: str | int):
        return self.questions.insert_cell(id, f_id, value)

    def get_invalid_count(self, course: str) -> int:
        course = course.strip()
        if not course:
            raise ValueError("A course is required")

        return self.questions.invalid_count(course)

    def get_total_count(self, course: str) -> int:
        course = course.strip()
        if not course:
            raise ValueError("A course is required")

        return self.questions.total_count(course)

    
    def get_invalid_list(self, course: str) -> int:
        course = course.strip()
        if not course: 
            raise ValueError("A course is required")

        return self.questions.invalid_list(course)

    def get_valid_list(self, course: str) -> list[int]:
        course = course.strip()
        if not course:
            raise ValueError("A course is required")

        return self.questions.valid_list(course)
    

    def check_col(self, id: int, column: str) -> bool:
        column = column.strip()
        if not column:
            raise ValueError("A column id must be provided")

        return self.questions.check_col(id, column)

    def get_QA_byId(self, id: int) -> tuple[str,str] | None:
        return self.questions.get_QA_byId(id)

    def get_overall_score(self, course: str):
        # accummulate attempts over each course question
        total_attempts = 0
        total_correct  = 0
        valid_list = self.get_valid_list(course)
        # for each id in valid list get attempts and correct answer counts
        for id in valid_list:
            data_tuple = self.get_data_byId(id)
            if data_tuple[8] != None and data_tuple[7] != None:
                total_attempts += data_tuple[8]
                total_correct  += data_tuple[7]
            else:
                return -1

        if total_attempts != 0:
            return (total_correct/total_attempts)*100
        else:
            return -1

        


    
    