import tkinter as tk
from tkinter import messagebox
from customtkinter import CTkToplevel,CTkEntry,CTkButton
from task import Task
class TopLevelWindowEdit(CTkToplevel):
    def __init__(self, master, app, selected_item):
        super().__init__(master)
        
        self.title("Edit Tasks")
        self.geometry("600x200")

        self.app = app
        self.selected_item = selected_item

        # Get the selected task from Treeview
        selected_task = self.app.frame.task_tree.item(selected_item, "values")[1]

        # Entry widget to display and edit the task
        self.edit_entry = CTkEntry(self)
        self.edit_entry.grid(row=1, column=0, pady=10, padx=10, sticky=tk.W)
        self.edit_entry.insert(0, selected_task)

        # Button to save changes made during editing
        save_edit_button = CTkButton(
            self,
            text="Save Changes",
            command=self.save_edited_task,
        )
        save_edit_button.grid(row=2, column=0, pady=10, padx=10, sticky=tk.W)

    def save_edited_task(self):
        edited_task_text = self.edit_entry.get()

        if edited_task_text:
            # Update the selected task in the list of tasks
            task_id = self.app.frame.task_tree.item(self.selected_item, "values")[0]
            for i, current_task in enumerate(self.app.tasks):
                if current_task.task_id == task_id:
                    updated_task = Task(
                        current_task.task_id,
                        edited_task_text,
                        current_task.priority,
                        current_task.date,
                        current_task.status,
                    )
                    self.app.tasks[i] = updated_task
                    break
                # Mark changes as made
            self.changes_made = True

        if self.changes_made:
            # Prompt the user to save changes before closing
            response = messagebox.askyesnocancel(
                "Save Changes", "Are you sure you want to save changes?"
            )

            if response is None:
                return  # Cancelled
            elif response:

            # Update the Treeview
                self.app.frame.update_task_tree()

                # Close the top-level window after saving changes
                self.destroy()
