import os
import tkinter as tk
from datetime import datetime
from controller.AccountController import AccountController
from controller.ContactController import ContactController
from views.Dashboard import DashboardView
from views.User import UserView
from views.Account import AccountView
from views.Contact import ContactView
from views.Messages import MessageView
from views.FindContact import FindContactView
from views.CreateAccount import CreateAccountView
from views.AccountInfo import AccountInfoView
from views.AppInfor import AppView

class DashboardController:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.view = DashboardView(self.root, self)
        self.view.pack(fill=tk.BOTH, expand=True)
        self.last_check_time = datetime.now()
        self.running = False
        self.timer = None
        self.frames = {}
    
    def load_asset(self, path):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assets = os.path.join(base, "images")
        return os.path.join(assets, path)

    def get_username(self):
        return self.user.username

    def show_screen(self, screen_name):
        # self.stop_checking_for_new_messages()
        if "MESSAGE" in self.frames:
            self.frames["MESSAGE"].stop_run_checking()
        if self.frames:
            for frame in self.frames.values():
                frame.pack_forget()
        else:
            for widget in self.view.container.winfo_children():
                    widget.destroy()

        from controller.AuthController import AuthController
        screens = {
            "USER": (UserView, AuthController),
            "ACCOUNT": (AccountView, AccountController),
            "CONTACT": (ContactView, ContactController),
            "FIND_CONTACT": (FindContactView, ContactController),
            "CREATE_ACCOUNT": (CreateAccountView, AccountController),
            "INFO": (AppView, None)
        }

        if screen_name in screens:
            view_class, controller_class = screens[screen_name]
            if screen_name not in self.frames:
                self.frames[screen_name] = self.create_frame(screen_name, view_class, controller_class)
            frame = self.frames[screen_name]
            if hasattr(frame, 'refresh_data'):
                frame.refresh_data()
            frame.pack(fill=tk.BOTH, expand=True)
        else:
            raise ValueError(f"Unknown screen name: {screen_name}")

    def create_frame(self, screen_name, view_class, controller_class=None):
        # self.stop_checking_for_new_messages()
        if "MESSAGE" in self.frames:
            self.frames["MESSAGE"].stop_run_checking()
        controller_args = [self.root]
        if screen_name in ["ACCOUNT", "CREATE_ACCOUNT", "CONTACT", "FIND_CONTACT"]:
            controller_args.append(self)
        controller = controller_class(*controller_args) if controller_class else self
        return view_class(self.view.container, controller, self.user)
    
    def logout(self):
        from controller.AuthController import AuthController
        if "MESSAGE" in self.frames:
            self.frames["MESSAGE"].stop_run_checking()
        self.view.destroy()
        AuthController(self.root)
        

    def show_accountInfo(self, accountId):
        # self.stop_checking_for_new_messages()
        if "MESSAGE" in self.frames:
            self.frames["MESSAGE"].stop_run_checking()
        for frame in self.frames.values():
                frame.pack_forget()
        if "ACCOUNT_INFO" not in self.frames:
            self.frames["ACCOUNT_INFO"] = AccountInfoView(self.view.container, AccountController(self.root, self), self.user, accountId)
        frame = self.frames["ACCOUNT_INFO"]
        frame.accountId = accountId
        if hasattr(frame, 'refresh_data'):
            frame.refresh_data()
        frame.pack(fill=tk.BOTH, expand=True)

    def show_message(self, contactId):
        for frame in self.frames.values():
                frame.pack_forget()
        if "MESSAGE" not in self.frames:
            self.frames["MESSAGE"] = MessageView(self.view.container, ContactController(self.root, self), self.user, contactId)            
        frame = self.frames["MESSAGE"]
        frame.contactId = contactId
        if "MESSAGE" in self.frames:
            frame.start_run_checking()
        if hasattr(frame, 'refresh_data'):
            frame.refresh_data()
        frame.pack(fill=tk.BOTH, expand=True)

    # def start_checking_for_new_messages(self, user_name, contact_name, callback):
    #     self.stop_checking_for_new_messages()
    #     self.running = True
    #     def check_for_new_messages():
    #         if not self.running:
    #             return
    #         print("----- check new messages RUN! -----")

    #         print("user_name", user_name)
    #         print("contact_name", contact_name)
    #         print("last_check_time", self.last_check_time)
    #         new_messages = MessageModels.check_new_messages(user_name, contact_name, self.last_check_time)
    #         if new_messages:
    #             print("Gọi vào tới đây rồi")
    #             self.last_check_time = datetime.now()
    #             callback(True)
    #         # Khởi động Timer
    #         if self.running:
    #             self.timer = threading.Timer(10, check_for_new_messages)
    #             self.timer.start()
    #     check_for_new_messages()

    # def stop_checking_for_new_messages(self):
    #     print("----- check new messages STOP! -----")
    #     # Đóng các luồng đang chạy
    #     self.running = False
    #     if self.timer is not None:
    #         self.timer.cancel()
    #         self.timer = None