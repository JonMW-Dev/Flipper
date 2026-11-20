
# Displays the edu panel
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QMessageBox
from openai import chat
from .testbank_service import TestBankService
from .ui_edu_view import Ui_eduView
from .course_item import CourseItem

class EduNotifier(QtCore.QObject):
    bank_changed = QtCore.Signal(str)
    validation_failed = QtCore.Signal(str)

class EduPanel(QtWidgets.QWidget):
    def __init__(self, course_das, testbank_das, chat_service, course_list_model):
        super().__init__()
        self.ui = Ui_eduView()
        self.ui.setupUi(self)

        self.course_model = course_list_model
        self.course_das   = course_das
        self.testbank_das = testbank_das
        self.chat_service = chat_service
        self.testbank_service = TestBankService(self.testbank_das)
        self.notifier = EduNotifier(self)
        self.notifier.bank_changed.connect(self.refresh_course)
        self.notifier.validation_failed.connect(self.show_validation_error)

        # Course List View
        self.ui.w_list_courseList.setItemDelegate(CourseRowDelegate(self.ui.w_list_courseList))
        self.ui.w_list_courseList.setModel(self.course_model)

        self.course_model.modelReset.connect(self.show_all_rows)

        for row in range(self.course_model.rowCount()):
            self.attach_row(row)

        self.course_model.rowsInserted.connect(self.show_new_rows)
        self.ui.btn_addCourse.clicked.connect(self.add_course)

    # opens a new window where the user can add a new course
    def add_course(self):
        self.course_model.add_course(self.ui.txtBox_courseName.text())

    def show_new_rows(self, parent, first, last):
        for row in range(first, last + 1):
            self.attach_row(row)

    def show_all_rows(self):
        for row in range(self.course_model.rowCount()):
            self.attach_row(row)

    def attach_row(self, row: int):
        index = self.course_model.index(row, 0)
        course = self.course_model.data(index)
        if course != None:
            widget = CourseItem(course, self.testbank_service, self.chat_service, self.notifier)

        self.ui.w_list_courseList.setIndexWidget(index, widget)

    def show_validation_error(self, message: str):
        QMessageBox.warning(self, "validation failed", message)

    def refresh_course(self, course_name: str):
        for row in range(self.course_model.rowCount()):
            index = self.course_model.index(row, 0)
            widget = self.ui.w_list_courseList.indexWidget(index)
            if isinstance(widget, CourseItem) and widget.course_name == course_name:
                widget.refresh_stats()


class CourseRowDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        return

    def sizeHint(self, option, index):
        return QtCore.QSize(200, 48)
