import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QComboBox, QDialog, QDialogButtonBox, QLabel, QLineEdit
from PyQt5.QtCore import Qt, QDateTime, QTimer
from language import LanguageManager
from task_manager import TaskManager
from task_table import TaskTable
from task_dialog import TaskDialog

class ToDoListGUI(QWidget):
    """Main GUI for the To-Do List application."""

    def __init__(self):
        super().__init__()
        self.language_manager = LanguageManager(self)
        self.task_manager = TaskManager(self)
        self.setWindowTitle(self.language_manager.get_translation("title"))
        self.current_language = self.language_manager.default_language

        main_layout = QVBoxLayout()
        self.setup_header(main_layout)
        self.setup_description(main_layout)
        self.setup_buttons(main_layout)
        self.setup_search(main_layout)
        self.setup_task_table(main_layout)

        self.setLayout(main_layout)
        self.update_task_list()
        self.setup_timer()

    def setup_header(self, layout):
        """Sets up the header section."""
        header_layout = QHBoxLayout()
        header_label = QLabel(self.language_manager.get_translation("title"), self)
        header_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(header_label)

        # Language selection
        self.language_combo = QComboBox(self)
        self.language_combo.addItems(self.language_manager.get_available_languages())
        self.language_combo.setCurrentText(self.current_language)
        self.language_combo.currentTextChanged.connect(self.change_language)
        header_layout.addWidget(QLabel(self.language_manager.get_translation("language"), self))
        header_layout.addWidget(self.language_combo)

        layout.addLayout(header_layout)

    def change_language(self, language):
        """Changes the application language."""
        self.current_language = language
        self.language_manager.translations = self.language_manager.load_language(language)
        self.update_ui_texts()

    def update_ui_texts(self):
        """Updates all UI texts based on the current language."""
        self.setWindowTitle(self.language_manager.get_translation("title"))
        self.description_label.setText(self.language_manager.get_translation("description"))
        self.add_button.setText(self.language_manager.get_translation("add"))
        self.remove_button.setText(self.language_manager.get_translation("delete"))
        self.search_button.setText(self.language_manager.get_translation("search"))

    def setup_description(self, layout):
        """Sets up the description section."""
        self.description_label = QLabel(self.language_manager.get_translation("description"), self)
        self.description_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.description_label)

    def setup_buttons(self, layout):
        """Sets up the add and remove buttons."""
        add_remove_layout = QHBoxLayout()
        self.add_button = QPushButton(self.language_manager.get_translation("add"))
        self.add_button.clicked.connect(self.open_add_task_dialog)
        add_remove_layout.addWidget(self.add_button)

        self.remove_button = QPushButton(self.language_manager.get_translation("delete"))
        self.remove_button.clicked.connect(self.remove_task)
        add_remove_layout.addWidget(self.remove_button)

        layout.addLayout(add_remove_layout)

    def setup_search(self, layout):
        """Sets up the search bar."""
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText(self.language_manager.get_translation("enter_search_term"))
        search_layout.addWidget(self.search_input)
        
        self.search_button = QPushButton(self.language_manager.get_translation("search"))
        self.search_button.clicked.connect(self.search_task)
        search_layout.addWidget(self.search_button)
        
        layout.addLayout(search_layout)

    def setup_task_table(self, layout):
        """Sets up the task table widget."""
        self.task_table = TaskTable(self.language_manager)
        self.task_table.task_changed.connect(self.on_task_changed)
        layout.addWidget(self.task_table)

    def update_task_list(self):
        """Updates the task table based on the current tasks."""
        self.task_table.update_task_list(self.task_manager.tasks)

    def setup_timer(self):
        """Sets up a timer to check tasks periodically."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.task_manager.check_tasks)
        self.timer.start(10000)

    def open_add_task_dialog(self):
        """Opens the dialog for adding a new task."""
        dialog = TaskDialog(self, translations=self.language_manager)
        if dialog.exec_() == QDialog.Accepted:
            task, datetime, repeat_until, priority = dialog.get_task_details()
            if task:
                self.task_manager.tasks.append((task, datetime, repeat_until, priority, False))
                self.update_task_list()
                self.task_manager.save_tasks()
            else:
                QMessageBox.warning(self, self.language_manager.get_translation("warning"), self.language_manager.get_translation("enter_task"))

    def on_task_changed(self, row, column, value):
        """Handles changes in the task table and saves them."""
        task, datetime, repeat_until, priority, notified = self.task_manager.tasks[row]
        if column == 0:
            task = value
        elif column == 1:
            datetime = value
        elif column == 2:
            priority = value
        elif column == 3:
            repeat_until = value if value else None
        self.task_manager.tasks[row] = (task, datetime, repeat_until, priority, notified)
        self.task_manager.save_tasks()

    def remove_task(self):
        """Removes the selected task."""
        selected_items = self.task_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            del self.task_manager.tasks[row]
            self.update_task_list()
            self.task_manager.save_tasks()
        else:
            QMessageBox.warning(self, self.language_manager.get_translation("warning"), self.language_manager.get_translation("no_task_selected"))

    def search_task(self):
        """Searches for tasks based on user input."""
        search_term = self.search_input.text().strip().lower()
        filtered_tasks = [task for task in self.task_manager.tasks if search_term in task[0].lower()]
        self.task_table.update_task_list(filtered_tasks)

    def show_notification(self, task, index, priority):
        """Shows a notification dialog for a due task."""
        dialog = QDialog(self)
        dialog.setWindowTitle(self.language_manager.get_translation("notification"))
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.language_manager.get_translation("task_due").format(task=task), self))
        button_box = QDialogButtonBox()
        
        done_button = QPushButton(self.language_manager.get_translation("done"))
        cancel_button = QPushButton(self.language_manager.get_translation("cancel"))
        postpone_button = QPushButton(self.language_manager.get_translation("postpone"))

        button_box.addButton(done_button, QDialogButtonBox.AcceptRole)
        button_box.addButton(cancel_button, QDialogButtonBox.RejectRole)
        button_box.addButton(postpone_button, QDialogButtonBox.HelpRole)

        done_button.clicked.connect(lambda: self.handle_done_button(dialog, index))
        cancel_button.clicked.connect(dialog.reject)
        postpone_button.clicked.connect(lambda: self.handle_postpone_button(dialog, index))

        layout.addWidget(button_box)
        dialog.setLayout(layout)
        
        dialog.exec_()

    def handle_done_button(self, dialog, index):
        """Handles the done button click event."""
        del self.task_manager.tasks[index]
        self.update_task_list()
        self.task_manager.save_tasks()
        dialog.accept()

    def handle_postpone_button(self, dialog, index):
        """Handles the postpone button click event."""
        self.extend_task(index, 60)
        dialog.accept()

    def extend_task(self, index, minutes):
        """Extends the due time of a task by the specified number of minutes."""
        task, datetime_str, repeat_until, priority, _ = self.task_manager.tasks[index]
        task_datetime = QDateTime.fromString(datetime_str, "yyyy-MM-dd HH:mm")
        task_datetime = task_datetime.addSecs(minutes * 60)
        self.task_manager.tasks[index] = (task, task_datetime.toString("yyyy-MM-dd HH:mm"), repeat_until, priority, False)
        self.update_task_list()
        self.task_manager.save_tasks()
        QMessageBox.information(self, self.language_manager.get_translation("notification"), self.language_manager.get_translation("task_extended").format(task=task, minutes=minutes))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo_app = ToDoListGUI()
    todo_app.show()
    sys.exit(app.exec_())
