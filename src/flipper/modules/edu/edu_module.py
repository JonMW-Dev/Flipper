from .edu_panel import EduPanel
from .course_list_model import CourseListModel

class EduModule():
    def __init__(self, course_das, testbank_das, chat_service):
        self.course_das   = course_das
        self.testbank_das = testbank_das
        self.chat_service = chat_service
        
        self.course_list_model = CourseListModel()

        self.edu_panel = EduPanel(self.course_das, self.testbank_das, self.chat_service, self.course_list_model)

        pass

    def get_edu_panel(self):
        return self.edu_panel


    pass