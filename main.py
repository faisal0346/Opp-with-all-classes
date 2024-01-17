from login import LoginWindow
import customtkinter
from saveloadtask import SaveLoadManager
if __name__ == "__main__":
    customtkinter.set_appearance_mode("light")
    save_load_manager = SaveLoadManager()
    login_window= LoginWindow()
    login_window.mainloop()
