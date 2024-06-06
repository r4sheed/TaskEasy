import json
import os
from PyQt5.QtWidgets import QMessageBox

class LanguageManager:
    def __init__(self, parent, language_folder="languages", default_language="en_US"):
        self.parent = parent
        self.language_folder = language_folder
        self.default_language = default_language
        self.default_translations = self.create_default_translations()
        self.ensure_default_language_file()
        self.translations = self.load_language(default_language)

    def ensure_default_language_file(self):
        """Ensures that the default language file exists."""
        if not os.path.exists(self.language_folder):
            os.makedirs(self.language_folder)
        language_file = os.path.join(self.language_folder, f"{self.default_language}.json")
        if not os.path.exists(language_file):
            self.create_default_language_file(language_file)

    def load_language(self, language):
        """Loads the specified language file."""
        language_file = os.path.join(self.language_folder, f"{language}.json")
        if not os.path.exists(language_file):
            QMessageBox.warning(self.parent, "Error", f"Translation file for {language} not found!")
            return self.default_translations
        try:
            with open(language_file, 'r', encoding='utf-8') as file:
                translations = json.load(file)
                translations = self.ensure_all_keys(translations)
                self.save_language_file(language_file, translations)  # Save the updated translations back to the file
                return translations
        except FileNotFoundError:
            QMessageBox.warning(self.parent, "Error", "Translation file not found!")
            return self.default_translations

    def ensure_all_keys(self, translations):
        """Ensures all keys from the default translations are present in the loaded translations."""
        updated = False
        for key, value in self.default_translations.items():
            if key not in translations:
                translations[key] = value
                updated = True
        return translations

    def create_default_language_file(self, language_file):
        """Creates the default language file with predefined translations."""
        with open(language_file, 'w', encoding='utf-8') as file:
            json.dump(self.default_translations, file, ensure_ascii=False, indent=4)

    def create_default_translations(self):
        """Creates the default translations."""
        return {
            "title": "ToDo List",
            "description": "Enter the new task, select the date and time, then click the 'Add' button.\nTo delete a selected task, click the 'Delete' button.\nYou can select multiple items for deletion at once.",
            "add": "Add",
            "edit": "Edit",
            "delete": "Delete",
            "task_description": "Task Description:",
            "deadline": "Deadline:",
            "notification": "Notification",
            "task_due": "{task} is due!",
            "done": "Done",
            "cancel": "Cancel",
            "postpone": "Postpone by 1 hour",
            "warning": "Warning",
            "enter_task": "Please enter a task!",
            "select_task": "Please select a task to edit!",
            "task_not_found": "Task not found!",
            "task_extended": "{task} extended by {minutes} minutes!",
            "file_error": "Invalid file format!",
            "no_task_selected": "No task selected!",
            "language": "Language",
            "show_notifications": "Show notifications",
            "repeat_until": "Repeat until:",
            "priority": "Priority:",
            "normal": "Normal",
            "high": "High",
            "highest": "Highest",
            "sort": "Sort",
            "search": "Search",
            "sort_by": "Sort by:",
            "date": "Date",
            "enter_search_term": "Enter search term:",
            "priority_sort": "Priority"
        }

    def save_language_file(self, language_file, translations):
        """Saves the language file with the provided translations."""
        with open(language_file, 'w', encoding='utf-8') as file:
            json.dump(translations, file, ensure_ascii=False, indent=4)

    def get_available_languages(self):
        """Returns a list of available languages based on the files in the language folder."""
        predefined_languages = ["en_US", "hu_HU", "de_DE"]
        available_languages = [f.split('.')[0] for f in os.listdir(self.language_folder) if f.endswith('.json')]
        return [lang for lang in predefined_languages if lang in available_languages]

    def get_translation(self, key):
        """Gets the translation for the specified key."""
        return self.translations.get(key, self.default_translations.get(key, key))
