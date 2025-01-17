import tkinter as tk
from tkinter import messagebox

class RegisterView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.canvas = tk.Canvas(self, bg="#F9F9FC", width=244, height=244, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_register()

    def create_register(self):
        self.label_register = tk.Label(self.canvas, text="ĐĂNG KÝ", font=("Inter", 18, "bold"), bg="#F9F9FC")
        self.canvas.create_window(122, 30, window=self.label_register)

        self.label_username = tk.Label(self.canvas, text="Username: ", font=("Arial", 9), bg="#F9F9FC")
        self.canvas.create_window(40, 70, window=self.label_username)

        self.username = tk.Entry(self.canvas, width=25, bg="#F9F9FC")
        self.username_placeholder = "username"
        self.username.insert(0, self.username_placeholder)
        self.username.bind("<FocusIn>", lambda event: self.on_focus_in(event, "username"))
        self.username.bind("<FocusOut>", lambda event: self.on_focus_out(event,"username"))
        self.canvas.create_window(155, 70, window=self.username)

        self.label_password = tk.Label(self.canvas, text="Password: ", font=("Arial", 9), bg="#F9F9FC")
        self.canvas.create_window(40, 105, window=self.label_password)

        self.password = tk.Entry(self.canvas, width=25, bg="#F9F9FC", show='*')
        self.password_placeholder = "password"
        self.password.insert(0, self.password_placeholder)
        self.password.bind("<FocusIn>", lambda event: self.on_focus_in(event, "password"))
        self.password.bind("<FocusOut>", lambda event: self.on_focus_out(event,"password"))
        self.canvas.create_window(155, 105, window=self.password)

        self.show_password_button = tk.Button(self.canvas, text="👁", relief="flat", borderwidth=0, font=("Inter", 8), bg='#F9F9FC',
                                             highlightthickness=0,  command=lambda e=self.password: self.toggle_password(e))
        self.canvas.create_window(239, 105, window=self.show_password_button)

        self.label_email = tk.Label(self.canvas, text="Email: ", font=("Arial", 9), bg="#F9F9FC")
        self.canvas.create_window(28, 140, window=self.label_email)

        self.email = tk.Entry(self.canvas, width=25, bg="#F9F9FC")
        self.email_placeholder = "abc@gmail.com"
        self.email.insert(0, self.email_placeholder)
        self.email.bind("<FocusIn>", lambda event: self.on_focus_in(event, "email"))
        self.email.bind("<FocusOut>", lambda event: self.on_focus_out(event,"email"))
        self.canvas.create_window(155, 140, window=self.email)

        self.label_phone = tk.Label(self.canvas, text="Phone: ", font=("Arial", 9), bg="#F9F9FC")
        self.canvas.create_window(30, 175, window=self.label_phone)

        self.phone = tk.Entry(self.canvas, width=25, bg="#F9F9FC")
        self.phone_placeholder = "0123456789"
        self.phone.insert(0, self.phone_placeholder)
        self.phone.bind("<FocusIn>", lambda event: self.on_focus_in(event, "phone"))
        self.phone.bind("<FocusOut>", lambda event: self.on_focus_out(event,"phone"))
        self.canvas.create_window(155, 175, window=self.phone)

        buttonRegister = tk.Button(self.canvas, text="Đăng ký", command=self.register, bg="#1492C3", fg="#ffffff")
        self.canvas.create_window(75, 220, width=60, window=buttonRegister)

        buttonBack = tk.Button(self.canvas, text="Thoát", command=self.cancel)
        self.canvas.create_window(160, 220, width=60, window=buttonBack)

    def on_focus_in(self, event, inputName):
        if inputName == "username":
            if self.username.get() == self.username_placeholder:
                self.username.delete(0, tk.END)
        elif inputName == "password":
            if self.password.get() == self.password_placeholder:
                self.password.delete(0, tk.END)
        elif inputName == "email":
            if self.email.get() == self.email_placeholder:
                self.email.delete(0, tk.END)
        else:
            if self.phone.get() == self.phone_placeholder:
                self.phone.delete(0, tk.END)

    def on_focus_out(self, event, inputName):
        if inputName == "username":
            if self.username.get() == "":
                self.username.insert(0, self.username_placeholder)        
        elif inputName == "password":
            if self.password.get() == "":
                self.password.insert(0, self.password_placeholder)
        elif inputName == "email":
            if self.email.get() == "":
                self.email.insert(0, self.email_placeholder)
        else:
            if self.phone.get() == "":
                self.phone.insert(0, self.phone_placeholder)
    
    def cancel(self):
        self.place_forget()

    def register(self):
        username = self.username.get()
        password = self.password.get()
        email = self.email.get()
        phone = self.phone.get()
        if self.valid_input(username, password, email, phone):
            self.controller.register(username, password, email, phone)

    def valid_input(self, username, password, email, phone):
        isValid = True
        if username == "" or not username.strip():
            messagebox.showinfo("Thông Báo!", "Vui lòng nhập 'username'.")
            isValid = False
        elif password == "" or not password.strip():
            messagebox.showinfo("Thông Báo!", "Vui lòng nhập 'password'.")
            isValid = False
        elif email == "" or not email.strip():
            messagebox.showinfo("Thông Báo!", "Vui lòng nhập 'email'.")
            isValid = False
        elif phone == "" or not phone.strip():
            messagebox.showinfo("Thông Báo!", "Vui lòng nhập 'phone'.")
            isValid = False
        return isValid
    
    def toggle_password(self, entry):
        if entry.cget('show') == '*':
            entry.config(show='')
        else:
            entry.config(show='*')

    def refresh_data(self):
        self.canvas.delete("all")
        self.create_register() 