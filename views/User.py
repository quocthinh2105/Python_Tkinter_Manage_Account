import tkinter as tk
from tkinter import messagebox

class UserView(tk.Frame):
    def __init__(self, parent, controller, user):
        super().__init__(parent)
        self.controller = controller
        self.user = user

        self.canvas = tk.Canvas(self, width=410, height=375, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_userview()

    def create_userview(self):
        self.label_title = tk.Label(self.canvas, text="THÔNG TIN NGƯỜI DÙNG", font=("Inter", 18, "bold"))
        self.canvas.create_window(202, 40, window=self.label_title)

        self.label_username = tk.Label(self.canvas, text="Tên tài khoản ", font=("Arial", 13))
        self.canvas.create_window(80, 100, window=self.label_username)

        self.username = tk.Label(self.canvas, text=self.user.username, font=("Arial", 13))
        self.canvas.create_window(220, 100, window=self.username)

        self.label_password = tk.Label(self.canvas, text="Mật khẩu ", font=("Arial", 13))
        self.canvas.create_window(63, 150, window=self.label_password)

        self.password = tk.Entry(self.canvas, width=25, font=("Arial", 12), show='*')
        self.password_placeholder = self.user.password
        self.password.insert(0, self.password_placeholder)
        self.password.bind("<FocusIn>", self.on_focus_in)
        self.password.bind("<FocusOut>", self.on_focus_out)
        self.canvas.create_window(250, 150, width=190, height=30, window=self.password)

        # self.show_password_button = tk.Button(self.canvas, text="👁", relief="flat", borderwidth=0, font=("Inter", 8), 
        #                                      highlightthickness=0,  command=lambda e=self.password: self.toggle_password(e))
        # self.canvas.create_window(352, 150, window=self.show_password_button)

        self.label_email = tk.Label(self.canvas, text="Email ", font=("Arial", 13))
        self.canvas.create_window(51, 200, window=self.label_email)

        self.email = tk.Entry(self.canvas, width=25, font=("Arial", 12))
        self.email.insert(0, self.user.email)
        self.canvas.create_window(250, 200, width=190, height=30, window=self.email)

        self.label_phone = tk.Label(self.canvas, text="Số điện thoại ", font=("Arial", 13))
        self.canvas.create_window(78, 250, window=self.label_phone)

        self.phone = tk.Entry(self.canvas, width=25, font=("Arial", 12))
        self.phone.insert(0, self.user.phone)
        self.canvas.create_window(250, 250, width=190, height=30, window=self.phone)

        buttonSave = tk.Button(self.canvas, text="Lưu", font=("Arial", 14), command=self.update_user_infor, bg="#1492C3", fg="#ffffff")
        self.canvas.create_window(205, 320, width=60, window=buttonSave)

    def on_focus_in(self, event):
        if self.password.get() == self.password_placeholder:
            self.password.delete(0, tk.END)

    def on_focus_out(self, event):
        if self.password.get() == "":
            self.password.insert(0, self.password_placeholder)

    # def toggle_password(self, entry):
    #     if entry.cget('show') == '*':
    #         entry.config(show='')
    #     else:
    #         entry.config(show='*')

    def update_user_infor(self):
        password = self.password.get()
        email = self.email.get()
        phone = self.phone.get()
        if self.valid_input(password, email, phone):
            if self.controller.updateUser(self.user.username, password, email, phone):
                self.user = self.controller.findUser(self.user.username)
                self.refresh_user_info()

    def valid_input(self, password, email, phone):
        isValid = True
        if password == "" or not password.strip():
            messagebox.showinfo("Thông Báo!", "Vui lòng nhập 'password'.")
            isValid = False
        elif email == "" or not email.strip():
            messagebox.showinfo("Thông Báo!", "Vui lòng nhập 'email'.")
            isValid = False
        elif phone == "" or not phone.strip():
            messagebox.showinfo("Thông Báo!", "Vui lòng nhập 'phone'.")
            isValid = False
        return isValid
    
    def refresh_user_info(self):
        self.email.delete(0, tk.END)
        self.email.insert(0, self.user.email)
        self.phone.delete(0, tk.END)
        self.phone.insert(0, self.user.phone)

    def refresh_data(self):
        self.canvas.delete("all")
        self.create_userview() 