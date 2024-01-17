import re
import tkinter as tk
from tkinter import messagebox
from customtkinter import CTkToplevel, CTkButton, CTkEntry

class CreateUserWindow(CTkToplevel):
    def __init__(self, login_window, save_load_manager):
        super().__init__()

        self.login_window = login_window  # Reference to the login window

        self.title("Create User")
        self.geometry("400x300")

        # Entry widgets for user details
        self.first_name_entry = CTkEntry(self, placeholder_text="First Name")
        self.last_name_entry = CTkEntry(self, placeholder_text="Last Name")
        self.username_entry = CTkEntry(self, placeholder_text="Username")
        self.password_entry = CTkEntry(self, show="*", placeholder_text="Password")

        # SaveLoadManager instance for managing user data
        self.save_load_manager = save_load_manager

        # Button to create user
        create_user_button = CTkButton(
            self, text="Create User", command=self.click_create_user
        )

        # Grid placement
        self.first_name_entry.pack(pady=10, padx=20, fill=tk.X)
        self.last_name_entry.pack(pady=10, padx=20, fill=tk.X)
        self.username_entry.pack(pady=10, padx=20, fill=tk.X)
        self.password_entry.pack(pady=10, padx=20, fill=tk.X)
        create_user_button.pack(pady=20)

    def click_create_user(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Authentication logic (create user)
        if username and password and first_name and last_name:
            # Check if the username already exists
            if not self.save_load_manager.user_exists(username):
                # Check if the username meets the specified pattern
                if re.match(r".*\d+@gmail\.com", username):
                    # Check if the password is at least 8 characters long and contains at least 2 numbers
                    if len(password) >= 8 and sum(c.isdigit() for c in password) >= 2:
                    # Create a new user
                        self.save_load_manager.create_user(
                            username, password, first_name, last_name
                        )
                        messagebox.showinfo("User Created", "User created successfully!")
                        self.withdraw()
                        self.login_window.deiconify()


                    else:
                        messagebox.showerror(
                            "Invalid Password",
                            "Password must be at least 8 characters long and contain at least 2 numbers."
                            )
                else:
                    messagebox.showerror(
                        "Invalid Username",
                        "Username must contain some numbers and end with '@gmail.com'.",
                    )
            else:
                messagebox.showerror(
                    "Username Exists",
                    "Username already exists. Please choose another.",
                )
        else:
            messagebox.showerror(
                "Invalid Input", "Please enter all required information."
            )

    
