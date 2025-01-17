import os
import tkinter as tk
from tkinter import messagebox
from utils.Bcrypt_utils import check_password
from utils.Send_mail import send_email
from model.UserModel import UserModels
from views.Login import LoginView
from views.Register import RegisterView
from views.ForgotPass import ForgotPassView
from controller.DashboardController import DashboardController

class AuthController:
    def __init__(self, root):
        self.root = root
        self.view = LoginView(root, self)
        self.dashboard_controller = None
        self.view.pack(fill=tk.BOTH, expand=True)
        self.frames = {}
        self.frames["REGISTER"] = RegisterView(parent=self.root, controller=self)
        self.frames["FORGOTPASS"] = ForgotPassView(parent=self.root, controller=self)

    user = None

    def load_asset(self, path):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assets = os.path.join(base, "images")
        return os.path.join(assets, path)
    
    def show_container(self, container_class):
        if container_class == "REGISTER":
            print("REGISTER")
            register_view = self.frames["REGISTER"]
            register_view.place(x=61, y=78, width=244, height=244)
        else:
            print("FORGOTPASS")
            register_view = self.frames["FORGOTPASS"]
            register_view.place(x=61, y=78, width=244, height=244)

    def login(self, username, password):
        user = UserModels.validate_user(username)        
        if user != None and check_password(user.password, password):
            messagebox.showinfo("Thông Báo!", "Đăng nhập thành công!")
            self.view.destroy()
            DashboardController(self.root, user)
        else:
            messagebox.showerror("Thông Báo!", "Username hoặc mật khẩu không đúng.")

    def register(self, username, password, email, phone):
        if UserModels.validate_user(username) != None:
            messagebox.showinfo("Thông Báo!", "Đăng ký thất bại! \n'{}' đã tồn tại trong hệ thống.".format(username))
            return
        if UserModels.create_user(username, password, email, phone):
            messagebox.showinfo("Thông Báo!", "Đăng ký thành công!")
            self.frames["REGISTER"].place_forget()
        else:
            messagebox.showinfo("Thông Báo!", "Đăng ký thất bại!")

    def forgot(self, username, email):
        user = UserModels.find_user(username, email)
        if user == None:
            messagebox.showinfo("Thông Báo!", "Username: {} hoặc Email: {} không đúng.".format(username, email))
            return
        
        subject = "Password Recovery"
        body = f"Dear {user.username},\n\nYour password is: 123456a@\n\nPlease keep it secure.\n\nThanks & Best regards !"
        if send_email(user.email, subject, body) and UserModels.reset_pass(user.username, user.email):
            messagebox.showinfo("Thông Báo!", "Thông tin mật khẩu đã được gửi đến email của bạn.")
        else:
            messagebox.showinfo("Thông Báo!", "Có lỗi trong quá trình gửi mail.")

    def updateUser(self, username, password, email, phone):
        if UserModels.validate_user(username) == None:
            messagebox.showinfo("Thông Báo!", "'{}' không tồn tại trong hệ thống.".format(username))
            return False

        if UserModels.update_user(username, password, email, phone):
            messagebox.showinfo("Thông Báo!", "Cập nhật thành công!")
            return True
        else:
            messagebox.showinfo("Thông Báo!", "Cập nhật thất bại!")
            return False
        
    def findUser(self, username):
        return UserModels.validate_user(username)