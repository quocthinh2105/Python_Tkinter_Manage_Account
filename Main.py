import tkinter as tk
from utils.Database_connection import Database
from controller.AuthController import AuthController

def on_close():
    print("Closing application...")
    Database.close_pool()
    root.quit()
    root.destroy()

if __name__ == "__main__":
    Database.init_pool()
    root = tk.Tk()
    app = AuthController(root)
    root.geometry("600x400")
    root.configure(bg="#ffffff")
    root.title("Manage Account")
    root.resizable(False, False)

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()