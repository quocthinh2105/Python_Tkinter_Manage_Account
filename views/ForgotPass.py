import tkinter as tk
from tkinter import messagebox

class ForgotPassView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.canvas = tk.Canvas(self, bg="#F9F9FC", width=244, height=244, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()

    def create_widgets(self):
        self.label_register = tk.Label(self.canvas, text="KHÔI PHỤC MẬT KHẨU", font=("Inter", 16, "bold"), bg="#F9F9FC")
        self.canvas.create_window(122, 40, window=self.label_register)

        self.label_Username = tk.Label(self.canvas, text="Username: ", font=("Arial", 10, "bold"), bg="#F9F9FC")
        self.canvas.create_window(60, 75, window=self.label_Username)

        self.username = tk.Entry(self.canvas, width=30, bg="#F9F9FC")
        self.canvas.create_window(122, 105, height=30 , window=self.username)

        self.label_email = tk.Label(self.canvas, text="Email: ", font=("Arial", 10, "bold"), bg="#F9F9FC")
        self.canvas.create_window(50, 135, window=self.label_email)

        self.email = tk.Entry(self.canvas, width=30, bg="#F9F9FC")
        self.canvas.create_window(122, 165, height=30 , window=self.email)

        buttonRegister = tk.Button(self.canvas, text="Gửi", command=self.reset_password, bg="#1492C3", fg="#ffffff")
        self.canvas.create_window(75, 210, width=60, window=buttonRegister)

        buttonBack = tk.Button(self.canvas, text="Thoát", command=self.cancel)
        self.canvas.create_window(160, 210, width=60, window=buttonBack)

    def cancel(self):
        self.place_forget()

    def reset_password(self):
        username = self.username.get()
        email = self.email.get()
        if self.valid_input(username, email):
            print(email)
            self.controller.forgot(username, email)

    def valid_input(self, username, email):
        isValid = True
        if username == "" or not username.strip():
            messagebox.showinfo("Thông Báo!", "Vui lòng nhập 'username'.")
            isValid = False
        elif email == "" or not email.strip():
            messagebox.showinfo("Thông Báo!", "Vui lòng nhập 'email'.")
            isValid = False
        return isValid
    
    def refresh_data(self):
        self.canvas.delete("all")
        self.create_widgets() 