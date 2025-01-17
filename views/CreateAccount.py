import tkinter as tk
from tkinter import messagebox

class CreateAccountView(tk.Frame):
    def __init__(self, parent, controller, user):
        super().__init__(parent)
        self.controller = controller
        self.user = user

        self.canvas = tk.Canvas(self, width=410, height=375, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_view()

    def create_view(self):
        self.label_account = tk.Label(self.canvas, text="Tạo Tài Khoản Mới", font=("Inter", 18, "bold"))
        self.canvas.create_window(202, 40, window=self.label_account)

        self.label_appname = tk.Label(self.canvas, text="Tên Ứng Dụng ", font=("Arial", 13))
        self.canvas.create_window(80, 100, window=self.label_appname)

        self.appname = tk.Entry(self.canvas, width=25, font=("Arial", 12))
        self.canvas.create_window(250, 100, width=190, height=30, window=self.appname)

        self.label_username = tk.Label(self.canvas, text="Tên Tài Khoản ", font=("Arial", 13))
        self.canvas.create_window(80, 150, window=self.label_username)

        self.username = tk.Entry(self.canvas, width=25, font=("Arial", 12))
        self.canvas.create_window(250, 150, width=190, height=30, window=self.username)

        self.label_password = tk.Label(self.canvas, text="Mật Khẩu ", font=("Arial", 13))
        self.canvas.create_window(63, 200, window=self.label_password)

        self.password = tk.Entry(self.canvas, width=25, font=("Arial", 12), show='*')
        self.canvas.create_window(250, 200, width=190, height=30, window=self.password)

        self.show_password_button = tk.Button(self.canvas, text="👁", relief="flat", borderwidth=0, font=("Inter", 8), 
                                             highlightthickness=0,  command=lambda e=self.password: self.toggle_password(e))
        self.canvas.create_window(352, 200, window=self.show_password_button)

        self.label_desciption = tk.Label(self.canvas, text="Ghi Chú ", font=("Arial", 13))
        self.canvas.create_window(60, 250, window=self.label_desciption)

        self.desciption = tk.Text(self.canvas, font=("Arial", 12), wrap=tk.WORD)
        self.canvas.create_window(250, 270, width=190, height=60, window=self.desciption)

        buttonSave = tk.Button(self.canvas, text="Thêm Mới", font=("Arial", 14), command=self.create_account, bg="#1492C3", fg="#ffffff")
        self.canvas.create_window(150, 335, window=buttonSave)

        buttonCancel = tk.Button(self.canvas, text="Huỷ", font=("Arial", 14), command=lambda:self.controller.show_account_view())
        self.canvas.create_window(270, 335, window=buttonCancel)

    def toggle_password(self, entry):
        if entry.cget('show') == '*':
            entry.config(show='')
        else:
            entry.config(show='*')

    def create_account(self):
        appname = self.appname.get()
        username = self.username.get()
        password = self.password.get()
        desciption = self.desciption.get("1.0", "end").strip()
        if self.valid_input(appname, username, password):
            self.controller.create_account(self.user.username ,appname, username, password, desciption)

    def refresh_data(self):
        self.canvas.delete("all")
        self.create_view() 

    def valid_input(self, appname, username, password):
        isValid = True
        if appname == "" or not appname.strip():
            messagebox.showinfo("Thông Báo!", "Vui lòng nhập 'Tên Ứng Dụng'.")
            isValid = False
        elif username == "" or not username.strip():
            messagebox.showinfo("Thông Báo!", "Vui lòng nhập 'Tên Tài Khoản'.")
            isValid = False
        elif password == "" or not password.strip():
            messagebox.showinfo("Thông Báo!", "Vui lòng nhập 'Mật Khẩu'.")
            isValid = False
        return isValid
