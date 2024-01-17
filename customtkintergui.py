import tkinter as tk
from tkinter import messagebox
from customtkinter import CTk, CTkButton
from frame import Frame
from saveloadtask import SaveLoadManager
from task import Task

class CustomTkinterGUI(CTk):
    def __init__(self,username):
        super().__init__()

        self.title("To-Do List")
        self.geometry("800x600")
        #self.iconbitmap(r"icons.ico")   
        
        # Create a custom scrollable frame within the main window
        self.scrollable_frame = Frame(self, username)
        self.scrollable_frame.pack(expand=True, fill="both")
        self.save_load_manager = SaveLoadManager(username)
        # Load tasks for the logged-in user
        self.scrollable_frame.app.tasks = [Task(*task_info) for task_info in self.save_load_manager.load_tasks_for_user(username)]
        # Update the Treeview in the Frame to display the tasks
        self.scrollable_frame.update_task_tree()
        # Close the entire application when the close button is clicked
        self.protocol("WM_DELETE_WINDOW", self.close_app)
        # Button to close the to-do list window
        close_app_button = CTkButton(
            self, text="Close To-Do List", command=self.close_app
        )
        close_app_button.pack(pady=20, padx=150, side=tk.RIGHT)
        # Button to logout
        logout_button = CTkButton(
            self, text="Logout", command=self.logout
        )
        logout_button.pack(pady=20, padx=20, side=tk.RIGHT)

    def logout(self):
        from login import LoginWindow
        confirmation = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirmation:
            self.withdraw()
            print("Successfully Logout")
            self.login_window = LoginWindow()
            self.login_window.deiconify()


    def close_app(self):
    # Destroy the main window
        self.withdraw()
        print("Application Closed")