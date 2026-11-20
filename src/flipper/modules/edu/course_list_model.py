from os import path

from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex
from flipper.data_access.data_access import DataAccessService


class CourseListModel(QAbstractListModel):
    def __init__(self):
        super().__init__()

        self.course_db_service = DataAccessService("education.db", "courses")       
        print("Course Model: Reading course data from courses table")
        self.courses = self.read_courselist()
        if len(self.courses) == 0:
            print(f"Course Model: the courses table has no courses")
        

    def rowCount(self, parent=None):
        return len(self.courses)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            raise IndexError(f"Invalid index provided {index}")
        

        course = self.courses[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            return course

    def add_course(self, course_name: str):
        print(f"Adding Course: {course_name}")
        row = len(self.courses)
        self.beginInsertRows(QModelIndex(), row, row) # notify model is changing
        self.courses.append(course_name)
        self.endInsertRows() # signal that edits are complete
        print(f"Updated Course List: {self.courses}")
        print(f"Updating course list")

        self.course_db_service.insert({"course": course_name})

    def refresh(self):
        self.beginResetModel()
        self.courses = self.read_courselist()
        self.endResetModel()


    def read_courselist(self) -> list[str]:
        new_courses: list[str] = []
        courses_data = self.course_db_service.get_all()
        for row in courses_data:
            if row["course"] not in new_courses:
                new_courses.append(row["course"])

        return new_courses
        
        


    