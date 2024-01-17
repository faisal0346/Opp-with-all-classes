from datetime import datetime
from tkinter import messagebox
from tkcalendar import Calendar
from customtkinter import CTkToplevel, CTkButton


class TopLevelCalendar(CTkToplevel):
    def __init__(self, app, default_date=None):
        super().__init__(app.frame)

        self.title("Select Due-Date")

        # Create a calendar dialog to select a date
        self.cal = Calendar(
            self, font="Arial 14", selectmode="day", cursor="hand1"
        )
        self.cal.pack()

        if default_date:
            try:
                # Set the calendar to the default date
                self.cal.selection_set(datetime.strptime(default_date, "%Y-%m-%d"))
            except ValueError:
                # Handle the case where the default_date is not a valid date
                messagebox.showerror(
                    "Error", "Invalid default date format. Defaulting to today."
                )
        else:
            default_date = datetime.now().strftime("%Y-%m-%d")

        # Button to confirm the selected date
        confirm_button = CTkButton(
            self,
            text="OK",
            command=lambda: app.on_date_select(self.cal, self),
        )
        confirm_button.pack(pady=10)

        self.wait_window()