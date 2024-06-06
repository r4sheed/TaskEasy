import os
import json
from PyQt5.QtCore import QDateTime
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QMessageBox

class TaskManager:
    """Class to manage tasks including saving, loading, and checking tasks."""

    def __init__(self, parent, key_file="key.key", task_file="tasks.txt"):
        self.parent = parent
        self.key_file = key_file
        self.task_file = task_file
        self.tasks = []
        self.key = self.load_or_generate_key()
        self.load_tasks()

    def load_or_generate_key(self):
        """Loads or generates an encryption key."""
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
            return key

    def save_tasks(self):
        """Saves the tasks to a file with encryption."""
        fernet = Fernet(self.key)
        with open(self.task_file, "wb") as file:
            for task, datetime, repeat_until, priority, notified in self.tasks:
                repeat_until_str = repeat_until if repeat_until else ""
                encrypted_task = fernet.encrypt(f"{task} - {datetime} - {repeat_until_str} - {priority} - {notified}".encode())
                file.write(encrypted_task + b"\n")

    def load_tasks(self):
        """Loads tasks from the file and decrypts them."""
        try:
            fernet = Fernet(self.key)
            with open(self.task_file, "rb") as file:
                encrypted_tasks = [line.strip() for line in file.readlines()]
                for encrypted_task in encrypted_tasks:
                    decrypted_task = fernet.decrypt(encrypted_task).decode()
                    task_datetime_repeat_priority_notified = decrypted_task.split(" - ")
                    if len(task_datetime_repeat_priority_notified) == 5:
                        task, datetime, repeat_until, priority, notified = task_datetime_repeat_priority_notified
                        notified = notified == "True"
                        repeat_until = repeat_until if repeat_until else None
                        self.tasks.append((task, datetime, repeat_until, priority, notified))
                    else:
                        QMessageBox.warning(self.parent, "Warning", "Invalid file format!")
        except FileNotFoundError:
            pass

    def check_tasks(self):
        """Checks if any tasks are due and shows notifications."""
        current_datetime = QDateTime.currentDateTime()
        for idx, (task, datetime_str, repeat_until, priority, notified) in enumerate(self.tasks):
            task_datetime = QDateTime.fromString(datetime_str, "yyyy-MM-dd HH:mm")
            if current_datetime >= task_datetime and not notified:
                self.tasks[idx] = (task, datetime_str, repeat_until, priority, True)
                self.save_tasks()
                self.parent.show_notification(task, idx, priority)
