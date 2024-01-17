import random, string
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, filedialog, StringVar
import tkinter.simpledialog
from saveloadtask import SaveLoadManager
from task import Task
from editwindow import TopLevelWindowEdit
from calendarwindow import TopLevelCalendar



class App():
    def __init__(self, frame,username):


        self.save_load_manager = SaveLoadManager(username)
        self.username = username
        self.tasks = self.save_load_manager
        self.frame = frame
        self.tasks = []
        # Load tasks during initialization
        self.tasks = [Task(*task_info) for task_info in self.save_load_manager.load_tasks_for_user(username)]
        self.priority_order = {"High Priority": 1, "Normal": 2}
        self.priority_order_status = {"Done": 1, "Incomplete": 2}

    def add_task(self):
        task_text = self.frame.task_entry.get()

        if task_text != "":

            task_id = self.generate_task_id()

            # Create an instance of the Task class
            new_task = Task(task_id, task_text, "Normal", "", "Incomplete")

            # Append the task to the list of tasks
            self.tasks.append(new_task)

            # Update the Treeview
            self.frame.update_task_tree()

            # Clear the task entry and due date entry
            self.frame.task_entry.delete(0, tk.END)
            self.frame.due_date_variable.set("")  # Clear the due date

    def generate_task_id(self):
        # Generate a random alphanumeric ID in the format ABC-123
        task_id = ''.join(random.choices(string.ascii_uppercase, k=3)) + '-' + ''.join(random.choices(string.digits, k=3))
        return task_id
    
    def change_status(self):
        selected_item = self.frame.task_tree.selection()
        if selected_item:
            task_id = self.frame.task_tree.item(selected_item, "values")[0]
            # Find the task in the list and update the status
            for i, current_task in enumerate(self.tasks):
                if current_task.task_id == task_id:
                    # Toggle the status between "Incomplete" and "Done"
                    new_status = "Done" if current_task.status == "Incomplete" else "Incomplete"
                    updated_task = Task(
                        current_task.task_id,
                        current_task.task_text,
                        current_task.priority,
                        current_task.date,
                        new_status,
                    )
                    self.tasks[i] = updated_task
                    break

            # Update the Treeview
            self.frame.update_task_tree()

    def prioritize_task(self):
        selected_item = self.frame.task_tree.selection()
        if selected_item:
            task_id = self.frame.task_tree.item(selected_item, "values")[0]
            # Find the task in the list and update the priority
            for i, task in enumerate(self.tasks):
                if task.task_id == task_id:
                    # Toggle the priority between "Normal" and "High Priority"
                    new_priority = "High Priority" if task.priority == "Normal" else "Normal"
                    self.tasks[i].priority = new_priority
                    break
            # Update the Treeview
            self.frame.update_task_tree()

    def search_task(self):
        search_text = self.frame.search_entry.get().lower()

        for item in self.frame.task_tree.get_children():
            task_text = self.frame.task_tree.item(item, "values")[1].lower()
            if search_text in task_text:
                # Highlight or focus on the matching task in Treeview
                self.frame.task_tree.selection_set(item)
                self.frame.task_tree.focus(item)
                return

        # Display a message if the task is not found
        messagebox.showinfo("Search Result", f"No task found with '{search_text}'.")

    def delete_selected_task(self):
        selected_item = self.frame.task_tree.selection()
        if selected_item:
            task_id = self.frame.task_tree.item(selected_item, "values")[0]
            confirmation = messagebox.askyesno(
                "Delete Task", f"Do you want to delete the task: {task_id}?"
            )
            if confirmation:
                self.tasks = [task for task in self.tasks if task.task_id != task_id]
        self.frame.update_task_tree()

    def edit_tasks(self):
        # Get the selected item in the Treeview
        selected_item = self.frame.task_tree.selection()
        if not selected_item:
            messagebox.showinfo("Error", "Please select a task to edit.")
            return
    # Open a new top-level window for editing tasks
        TopLevelWindowEdit(self.frame, self, selected_item)

    def update_due_date(self, selected_item, date_str):
        if selected_item:
            task_id = self.frame.task_tree.item(selected_item, "values")[0]

            # Find the task in the list and update the date
            for i, current_task in enumerate(self.tasks):
                if current_task.task_id == task_id:
                    # Handle the case where date_str is None
                    formatted_date = date_str if date_str is not None else ""
                    updated_task = Task(
                        current_task.task_id,
                        current_task.task_text,
                        current_task.priority,
                        formatted_date,
                        current_task.status,
                    )
                    self.tasks[i] = updated_task
                    break
            self.frame.update_task_tree()
            

    def show_due_date_calendar(self, default_date=None):
        # Create an instance of TopLevelCalendar
        TopLevelCalendar(self, default_date)
    
    def on_date_select(self, cal, due_date_window):
        # Get the selected date
        date_str = cal.selection_get()

        # Format the selected date
        formatted_date = date_str.strftime("%Y-%m-%d")

        # Insert the formatted date into the due date variable
        self.frame.due_date_variable.set(formatted_date)

        # Update the Treeview
        self.update_due_date(self.frame.task_tree.selection(), formatted_date)

        # Close the calendar window
        due_date_window.destroy()
        return self.frame.due_date_variable.get()
    
    def sort_by_status(self):
    # Sort tasks by status

        self.tasks = sorted(
            self.tasks, key=lambda task: self.priority_order_status.get(task.status, float("inf"))
        )
        self.frame.update_task_tree()

    def sort_by_priority(self):
        # Define a custom sorting order where "High Priority" comes before "Normal"
        self.tasks = sorted(
            self.tasks, key=lambda task: self.priority_order.get(task.priority, float("inf"))
        )
        self.frame.update_task_tree()

    def sort_by_date(self):
    # Separate tasks with and without due dates
        tasks_with_dates = [task for task in self.tasks if task.date]
        tasks_without_dates = [task for task in self.tasks if not task.date]

        # Sort tasks with due dates by due date
        tasks_with_dates = sorted(
            tasks_with_dates, key=lambda task: datetime.strptime(task.date, "%Y-%m-%d")
        )

        # Combine tasks with and without due dates
        self.tasks = tasks_with_dates + tasks_without_dates

        # Update the Treeview
        self.frame.update_task_tree()    

    def save_tasks(self):

        task_data = [
            [task.task_id, task.task_text, task.priority, task.date, task.status]
            for task in self.tasks
        ]
        self.save_load_manager.save_tasks_for_user(self.username, task_data)
        messagebox.showinfo("Task List", "Tasks saved successfully.")

    def load_tasks(self):

        file_path = filedialog.askopenfilename(
            title="Select JSON File", filetypes=[("JSON Files", "*.json")]
        )

        if file_path:
            try:
                # Load tasks from the selected file
                task_data = self.save_load_manager.load_tasks_from_file(file_path)
                self.tasks = [Task(*task_info) for task_info in task_data]
        # Update the Treeview
                self.frame.update_task_tree()
                messagebox.showinfo("Task List", "Tasks loaded successfully.")
            except Exception as e:
                messagebox.showerror("Task List", f"Error loading tasks: {str(e)}")

    def clear_saved_tasks(self):
        # Clear the saved tasks using SaveLoadManager
        self.save_load_manager.clear_saved_tasks()
        messagebox.showinfo("Clear Successful", "Saved tasks cleared successfully.")

    def filter_by_status(self):
        # Ask the user whether to filter by "Complete" or "Incomplete"
        status_options = ["Done", "Incomplete"]
        selected_status = tkinter.simpledialog.askstring(
            "Filter by Status", "Enter 'Done' or 'Incomplete':", 
            initialvalue=status_options[0]
        )

        if selected_status:
            # Filter tasks based on the selected status
            filtered_tasks = [task for task in self.tasks if task.status.lower() == selected_status.lower()]

            # Update the tasks and Treeview
            self.tasks = filtered_tasks
            self.frame.update_task_tree()

    def reset_filter(self):
        # Reset the tasks to the original list
        self.tasks = [Task(*task_info) for task_info in self.save_load_manager.load_tasks_for_user(self.username)]

        # Update the Treeview
        self.frame.update_task_tree()