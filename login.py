import tkinter as tk
from customtkinter import CTk, CTkButton, CTkEntry
from customtkintergui import CustomTkinterGUI
from createuser import CreateUserWindow
from task import Task
from saveloadtask import SaveLoadManager

class LoginWindow(CTk):
    def __init__(self):
        super().__init__()

        # Reference to CreateUserWindow instance
        self.create_user_window = None
        self.custom_tkinter_gui = None
        self.save_load_manager = SaveLoadManager()

        self.title("Login")
        self.geometry("400x200")

        # Entry widgets for login details
        self.username_entry = CTkEntry(self, placeholder_text="username")
        self.password_entry = CTkEntry(self, show="*", placeholder_text="password")

        # Button to login
        login_button = CTkButton(
            self, text="Login", command=self.login
        )

        # Button to create a new user
        new_user_button = CTkButton(
            self, text="Create New User", command=self.open_create_user_window
        )

        # Grid placement
        self.username_entry.pack(pady=10, padx=20, fill=tk.X)
        self.password_entry.pack(pady=10, padx=20, fill=tk.X)
        login_button.pack(pady=10)
        new_user_button.pack(pady=10)

    def login(self):
        # Get login details from entry widgets
        username = self.username_entry.get()
        password = self.password_entry.get()

        users = self.save_load_manager.load_users()

           # Check if the entered username and password match the stored data
        if username in users and users[username]["password"] == password:

            # hide login window
            self.withdraw()
            # Create and show the CustomTkinterGUI window
            self.custom_tkinter_gui = CustomTkinterGUI(username)
            self.custom_tkinter_gui.deiconify()
            print("Successfully Login")
        else:
            self.show_error("Incorrect password.")

    def open_create_user_window(self):
        
        # Hide the login window
        self.withdraw()

        # Open the CreateUserWindow when the "New User" button is clicked
        if self.create_user_window is None or not self.create_user_window.winfo_exists():
            self.create_user_window = CreateUserWindow(self, self.save_load_manager)

    def show_error(self, message):
        tk.messagebox.showerror("Error", message)

    def show_info(self, message):
        tk.messagebox.showinfo("Information", message)
