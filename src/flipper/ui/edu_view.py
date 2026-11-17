import grp
import random
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QMessageBox
from flipper.ui.generated.ui_edu_view import Ui_eduView
from flipper.models.course_list_model import CourseListModel
from flipper.ui.course_panel import CoursePanel


class EduView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # setup GUI 
        self.ui = Ui_eduView()
        self.ui.setupUi(self)
        # setup List view to list added courses
        self.model = CourseListModel()
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
        if course != None:
            widget = CoursePanel(course)


        widget.bank_changed.connect(self.schedule_refresh)
        widget.validation_failed.connect(self.show_validation_error)
        self.ui.w_list_courseList.setIndexWidget(index, widget)

    def show_validation_error(self, message: str):
        QMessageBox.warning(self, "validation failed", message)
    def schedule_refresh(self):
        QtCore.QTimer.singleShot(0, self.model.refresh)

class CourseRowDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        return

    def sizeHint(self, option, index):
        return QtCore.QSize(200, 48)


