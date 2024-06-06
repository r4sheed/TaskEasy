from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox, QHeaderView
from PyQt5.QtCore import Qt, pyqtSignal

class TaskTable(QTableWidget):
    """Custom QTableWidget to display and manage tasks."""
    
    task_changed = pyqtSignal(int, int, str)  # Signal to notify when a task has been changed

    def __init__(self, translations, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.translations = translations
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels([
            self.translations.get_translation("task_description"),
            self.translations.get_translation("deadline"),
            self.translations.get_translation("priority"),
            self.translations.get_translation("repeat_until")
        ])
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

        self.cellChanged.connect(self.on_cell_changed)

    def update_task_list(self, tasks):
        """Updates the task table based on the current tasks."""
        self.setRowCount(0)
        for task, datetime_str, repeat_until, priority, notified in tasks:
            row_position = self.rowCount()
            self.insertRow(row_position)

            # Task description
            task_item = QTableWidgetItem(task)
            task_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
            self.setItem(row_position, 0, task_item)

            # Deadline
            datetime_item = QTableWidgetItem(datetime_str)
            datetime_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
            self.setItem(row_position, 1, datetime_item)

            # Priority
            priority_combo = QComboBox()
            priority_combo.addItems([self.translations.get_translation("normal"), 
                                      self.translations.get_translation("high"), 
                                      self.translations.get_translation("highest")])
            priority_combo.setCurrentText(priority)
            priority_combo.currentTextChanged.connect(lambda text, row=row_position: self.on_priority_changed(row, text))
            self.setCellWidget(row_position, 2, priority_combo)

            # Repeat until
            repeat_item = QTableWidgetItem(repeat_until if repeat_until else "")
            repeat_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
            self.setItem(row_position, 3, repeat_item)

            # Set notified color
            if notified:
                task_item.setForeground(Qt.gray)
                datetime_item.setForeground(Qt.gray)
                priority_combo.setStyleSheet("color: gray;")
                repeat_item.setForeground(Qt.gray)

    def on_cell_changed(self, row, column):
        """Handles changes in the cell and emits a signal."""
        item = self.item(row, column)
        if item:
            self.task_changed.emit(row, column, item.text())

    def on_priority_changed(self, row, text):
        """Handles changes in the priority and emits a signal."""
        self.task_changed.emit(row, 2, text)
