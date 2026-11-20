from multiprocessing import Value

from flipper.data_access.data_access import TABLE_DEFINITIONS, DataAccessService

TABLE_COLS = ("id", "is_valid", "course", "question", "answer", "f1", "f2", "f3", "correct", "attempts")

class TestBankService:
    def __init__(self, data_service: DataAccessService):
        self.data_service = data_service
        # get list of courses:
        self.course_list = self.get_course_list()
        print(f"TestBank Service: found courses: \n {self.course_list}")

    def get_course_list(self):
        course_service = DataAccessService("education.db", "courses") 
        table_data = course_service.get_all()
        course_list = []
        for row in table_data:
            if row["course"] not in course_list:
                course_list.append(row["course"])
                
        
        return course_list
    def get_all_rows(self, course: str):
        if course not in self.course_list:
            print(f"TestBank Service:Error: [{course}] was not found in course list:\n {self.course_list}")
            return 

        identifier = ("course",course)
        conditions = {"is_valid": False, "is_valid": True}
        return self.data_service.get_list(identifier, conditions)

    def add_question(self, course: str, question: str, answer: str):
        if course not in self.course_list:
            print(f"TestBank Service:Error: [{course}] was not found in course list:\n {self.course_list}")
            return 
            
        data: dict = {
            "course"  :  course,
            "question":  question,
            "answer"  :  answer,
        }
        
        self.data_service.insert(data)

    def update_data(self, row_id: int, column: str, value: int | str):
        if column not in TABLE_COLS:
            raise ValueError("TestBank Service:Error: invalid column provided to update_data")

        if column in {"correct", "attempts"} and isinstance(value, str):
            raise ValueError(f"The column {column} cannot be a string: {value}")

        identifier: tuple = ("id", row_id)
        data: dict = {column:value}


        self.data_service.update_row(identifier, data)


    def get_row(self, row_id: int) -> tuple | None:
        identifier = ("id", row_id)
        return self.data_service.get_row(identifier)

    def get_record(self, row_id: int) -> dict | None:
        row_data = self.get_row(row_id)
        if row_data is None:
            return None
        if len(row_data) != len(TABLE_COLS):
            raise ValueError(f"TestBank Service:Error: The testbank service definition of the table does not match the definition in the database")
        return dict(zip(TABLE_COLS, row_data))

    def add_false_answer(self, id: int, f_id: str, value: str | int):
        if f_id not in TABLE_COLS:
            raise ValueError(f"TestBank Service:Error: [{f_id}] is not a valid column")
        identifier = ("id", id)
        data = {f_id:value}

        self.data_service.update_row(identifier, data)

    def get_invalid_count(self, course: str) -> int:
        identifier = ("course", course)
        condition: dict[str, bool] = {"is_valid":False}

        return self.data_service.count_rows(identifier, condition)

    def get_total_count(self, course: str) -> int:
        if course not in self.course_list:
            return 0
        
        identifier: tuple = ("course",course)
        return self.data_service.count_rows(identifier)

    
    def get_invalid_list(self, course: str) -> list[int]:


        identifier: tuple = ("course", course)
        condition: dict = {"is_valid":False}

        return self.data_service.get_list(identifier, condition)

    def get_valid_list(self, course: str) -> list[int]:


        identifier: tuple = ("course", course)
        condition: dict = {"is_valid":True}

        return self.data_service.get_list(identifier, condition)
    

    def check_col(self, id: int, column: str) -> bool:
        if column not in TABLE_COLS:
            raise ValueError(f"TestBank Service:Error: [{column}] is not a valid column")

        # True when the column holds a value. None and "" both count as empty.
        return self.data_service.check_col(id, column)

    def get_question_answer(self, id: int) -> tuple[str,str] | None:
        identifier = ("id", id)
        row_data = self.data_service.get_row(identifier)
        if row_data == None:
            raise ValueError(f"TestBank Service:Error: DAS returned a None value")

        # TODO - This only confirms that DAS returned the correct number of values, does not check that the column names are the same.
        # Therefor, we should check the column names in the table match TABLE_COLS and raise a warning about the mismatch.

        if len(row_data) != len(TABLE_COLS):
            raise ValueError(f"TestBank Service:Error: The testbank service definition of the table does not match the definition in the database")

        data: dict = {}
        i: int = 0
        for column in TABLE_COLS:
            data[column] = row_data[i]
            i += 1

        return (data["question"], data["answer"])
    

    def get_overall_score(self, course: str):
        if course not in self.course_list:
            return -1
        total_attempts = 0
        total_correct  = 0
        for row_id in self.get_valid_list(course):
            record = self.get_record(row_id)
            if record is None:
                return -1
            total_attempts += record["attempts"] or 0
            total_correct  += record["correct"] or 0

        if total_attempts != 0:
            return (total_correct/total_attempts)*100
        else:
            return -1

        


    
    