import tkinter as tk
from tkinter import ttk, StringVar
from customtkinter import  CTkScrollableFrame, CTkEntry, CTkButton, CTkLabel, CTkComboBox
from app import App
class Frame(CTkScrollableFrame):
    def __init__(self, master,username, **kwargs):
        super().__init__(master, **kwargs)

        self.app = App(self, username)
        # Entry widget for Due Date of tasks
        self.due_date_variable = StringVar()

        # Entry widget to input new tasks
        self.task_entry = CTkEntry(
            self, corner_radius=10, placeholder_text="Add New Task"
        )
        self.task_entry.grid(row=0, column=0, pady=10, padx=10, sticky=tk.W + tk.E)

        # Button to add a new task
        add_button = CTkButton(
            self, corner_radius=5, text="Add Task", command=self.app.add_task
        )
        add_button.grid(row=0, column=1, pady=10, padx=10, sticky=tk.W)

        # Entry widget to search for tasks
        self.search_entry = CTkEntry(
            self, corner_radius=10, placeholder_text="Search Task"
        )
        self.search_entry.grid(row=1, column=0, pady=10, padx=10, sticky=tk.W + tk.E)

        # Button to search for tasks
        search_button = CTkButton(
            self, text="Search", command=self.app.search_task
        )
        search_button.grid(row=1, column=1, pady=10, padx=10, sticky=tk.W)

        # Button for Due Date of tasks
        due_date_button = CTkButton(
            self, text="Due-Date", command=self.app.show_due_date_calendar
        )
        due_date_button.grid(row=2, column=1, pady=10, padx=10, sticky=tk.W)

        # Button to save tasks to a file
        save_button = CTkButton(
            self, text="Save Tasks", command=self.app.save_tasks
        )
        save_button.grid(row=3, column=0, pady=10, padx=10, sticky=tk.W)

        # Entry widget for Due Date of tasks
        self.due_date_entry = CTkEntry(
            self, textvariable=self.due_date_variable
        )

        # Button to load tasks from a file
        load_button = CTkButton(
            self, text="Load Tasks", command=self.app.load_tasks
        )
        load_button.grid(row=3, column=1, pady=10, padx=10, sticky=tk.W)

        # Button to set Task as priority
        priority_status_button = CTkButton(
            self, text="Change Task Priority", command=self.app.prioritize_task
        )
        priority_status_button.grid(row=3, column=0, pady=10, padx=200, sticky=tk.W)

        # Button to change status
        change_status_button = CTkButton(
            self, text="Change Status", command=self.app.change_status
        )
        change_status_button.grid(row=4, column=1, pady=10, padx=10, sticky=tk.W)

        # Button to sort tasks
        sort_button = CTkButton(
            self, text="Sort by Status", command=self.app.sort_by_status
        )
        sort_button.grid(row=4, column=0, pady=10, padx=10, sticky=tk.W)

        # Button to sort tasks by date
        sort_date_button = CTkButton(
            self, text="Sort by Due-Date", command=self.app.sort_by_date
        )
        sort_date_button.grid(row=4, column=0, pady=10, padx=200, sticky=tk.W)

        # Button to sort tasks by date
        sort_priority_button = CTkButton(
            self, text="Sort by Priority", command=self.app.sort_by_priority
        )
        sort_priority_button.grid(row=4, column=0, pady=10, padx=400, sticky=tk.W)

        # Button to delete tasks
        delete_button = CTkButton(
            self, text="Delete Task", command=self.app.delete_selected_task
        )
        delete_button.grid(row=5, column=1, pady=5, padx=10, sticky=tk.W)

        # Button to edit tasks
        edit_button = CTkButton(
            self, text="Edit Task", command=self.app.edit_tasks
        )
        edit_button.grid(row=5, column=1, pady=5, padx=175, sticky=tk.W)
        # Button to filter by status
        filter_Status_button = CTkButton(
            self, text="Filter-by-Status", command=self.app.filter_by_status
        )
        filter_Status_button.grid(row=6, column=1, pady=5, padx=10, sticky=tk.W)
        reset_filter_button = CTkButton(
            self, text="Reset-Filter", command=self.app.reset_filter
        )
        reset_filter_button.grid(row=6, column=1, pady=5, padx=175, sticky=tk.W

        )

        # Create a Treeview to display tasks
        self.task_tree = ttk.Treeview(
            self,
            columns=("Task ID", "Task", "Priority", "Due-Date", "Status"),
            show="headings",
        )
        self.task_tree.heading("Task ID", text="Task ID")
        self.task_tree.heading("Task", text="Task")
        self.task_tree.heading("Priority", text="Priority")
        self.task_tree.heading("Due-Date", text="Due-Date")
        self.task_tree.heading("Status", text="Status")
        self.task_tree.grid(row=5, column=0, pady=10, padx=10, sticky=tk.W)


    def update_task_tree(self):
        self.task_tree.delete(*self.task_tree.get_children())
        for task in self.app.tasks:  # Use self.app.tasks instead of self.tasks
            self.task_tree.insert(
                "", tk.END, values=(task.task_id, task.task_text, task.priority, task.date, task.status)
            )

    #def create_menu(self):
        # Create a menu bar
     #   menu_bar = tk.Menu(self)
      #  self.config(menu=menu_bar)

        # Create a "Filter" menu with "By Status" and "Reset" options
       # filter_menu = tk.Menu(menu_bar, tearoff=0)
        #menu_bar.add_cascade(label="Filter", menu=filter_menu)

        #filter_menu.add_command(label="By Status", command=self.app.filter_by_status)
        #filter_menu.add_command(label="Reset", command=self.app.reset_filter)
    