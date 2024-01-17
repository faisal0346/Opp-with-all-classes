import json
import os


class SaveLoadManager:
    def __init__(self, base_path=None, filename="users.json"):
        self.base_path = base_path or ""
        self.filename = filename
        self.file_path = os.path.join(self.base_path, filename)

    def save_tasks_for_user(self, username, tasks):
        # set user_task filename
        user_filename = f"{username}_tasks.json"
        #set user_task file_path
        user_file_path = os.path.join(self.base_path, user_filename)
        # Ensure that the directory structure exists
        os.makedirs(os.path.dirname(user_file_path), exist_ok=True)

        with open(user_file_path, "w", encoding="utf-8") as file:
            json.dump(tasks, file)

        print(f"Tasks for user '{username}' saved to file: {user_file_path}")

    def user_exists(self, username):
        # Check if a user with the given username exists
        users = self.load_users()
        return username in users

    def create_user(self, username, password, first_name, last_name):
        # Create a new user with the given username and password
        users = self.load_users()
        users[username] = {
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        }
        self.save_users(users)

    def load_users(self):
        try:
            with open(self.filename, "r") as file:
                users = json.load(file)
                return users
        except FileNotFoundError:
            return {}

    def load_tasks_for_user(self, username):
        user_filename = f"{username}_tasks.json"
        user_file_path = os.path.join(self.base_path, user_filename)

        try:
            with open(user_file_path, "r") as file:
                tasks = json.load(file)
                print(f"Tasks for user1 '{username}' loaded from file: {user_file_path}")
                return tasks
        except FileNotFoundError:
            print(f"No tasks found for user '{username}' at file: {user_file_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for user '{username}': {str(e)}")
            return []
        except Exception as e:
            print(f"Error loading tasks for user '{username}': {str(e)}")
            return []

    def save_users(self, users):

        # Ensure that the directory structure exists
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.filename, "w") as file:
            json.dump(users, file)

        print(f"User data saved to file: {self.file_path}")

    def load_tasks_from_file(self, file_path, encoding="utf-8"):
        try:
            with open(file_path, "r", encoding=encoding) as file:
                tasks = json.load(file)

                # Check if each task has at least four values
                for task in tasks:
                    if len(task) < 4:
                        raise ValueError("Invalid task format in the loaded file.")

                    # If the task has only four values, add an empty string for the date
                    if len(task) == 4:
                        task.append("")

                print("Tasks loaded from file:", file_path)
                return tasks
        except FileNotFoundError:
            print(f"No tasks found in the selected file: {file_path}")
            return []
        except ValueError as ve:
            print(f"Error loading tasks from file: {ve}")
            return []
        except Exception as e:
            print(f"Error loading tasks from file: {str(e)}")
            return []

