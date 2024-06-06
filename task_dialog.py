from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDateTimeEdit, QComboBox, QDialogButtonBox
from PyQt5.QtCore import QDateTime, QLocale

class TaskDialog(QDialog):
    """Dialog window for adding or editing a task."""

    def __init__(self, parent=None, task=None, datetime=None, repeat_until=None, priority=None, translations=None):
        super().__init__(parent)
        self.translations = translations or {}
        self.setWindowTitle(self.translations.get_translation("add_edit_task"))
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()

        # Task description label and input
        task_label = QLabel(self.translations.get_translation("task_description"), self)
        layout.addWidget(task_label)
        self.task_entry = QLineEdit(self)
        if task:
            self.task_entry.setText(task)
        layout.addWidget(self.task_entry)

        # Deadline label and datetime picker
        datetime_label = QLabel(self.translations.get_translation("deadline"), self)
        layout.addWidget(datetime_label)
        self.datetime_picker = QDateTimeEdit(self)
        self.datetime_picker.setCalendarPopup(True)
        locale = QLocale("hu_HU")
        self.datetime_picker.setLocale(locale)
        if datetime:
            self.datetime_picker.setDateTime(QDateTime.fromString(datetime, "yyyy-MM-dd HH:mm"))
        else:
            self.datetime_picker.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(self.datetime_picker)

        # Repeat until text entry
        repeat_label = QLabel(self.translations.get_translation("repeat_until"), self)
        layout.addWidget(repeat_label)
        self.repeat_entry = QLineEdit(self)
        if repeat_until:
            self.repeat_entry.setText(repeat_until)
        layout.addWidget(self.repeat_entry)


        # Priority selection
        priority_label = QLabel(self.translations.get_translation("priority"), self)
        layout.addWidget(priority_label)
        self.priority_combo = QComboBox(self)
        self.priority_combo.addItems([self.translations.get_translation("normal"), 
                                      self.translations.get_translation("high"), 
                                      self.translations.get_translation("highest")])
        if priority:
            self.priority_combo.setCurrentText(priority)
        layout.addWidget(self.priority_combo)

        # Dialog buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_task_details(self):
        """Returns the entered task details."""
        task = self.task_entry.text()
        datetime = self.datetime_picker.dateTime().toString("yyyy-MM-dd HH:mm")
        repeat_until = self.repeat_entry.text().strip() if self.repeat_entry.text().strip() else None
        priority = self.priority_combo.currentText()
        return task, datetime, repeat_until, priority

