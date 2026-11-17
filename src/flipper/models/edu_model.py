from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex
import PySide6.QtCore
class EduModel(QAbstractListModel):
    def __init__(self):
        super().__init__()

        # Read courses from courselist.txt
        self.courses = self.read_courselist()

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

        #save list to txt file
        try:
            with open("courselist.txt", "w") as fw:
                for course in self.courses:
                    fw.write(f"{course}\n")

            fw.close()
        except:
            raise Exception("Error: Could not save course list to file")

    def refresh(self):
        self.beginResetModel()
        self.courses = self.read_courselist()
        self.endResetModel()

    def read_courselist(self) -> list[str]:
        new_courses: list[str] = []
        try:
            with open("data/courselist.txt", "r") as fr:
                for line in fr:
                    line = line.strip()
                    if not line:
                        continue
                    new_courses.append(line)
            fr.close()
            return new_courses
        except:
            raise OSError("Error opening course_list.txt")
        
        


    