import os
from tkinter import messagebox
from datetime import datetime
from utils.EncDecryption import decrypt_password
from model.AccountModel import AccountModels
from model.ContactModel import ContactModels
from model.MessageModel import MessageModels

class ContactController:
    def __init__(self, root, dashboard_controller):
        self.app = root
        self.dashboard_controller = dashboard_controller
        self.last_check_time = datetime.now()

    def load_asset(self, path):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assets = os.path.join(base, "images")
        return os.path.join(assets, path)

    def get_list_contacts(selt, username):
        return ContactModels.get_list_contact(username)
    
    def find_contacts(selt, username, contact_name):
        return ContactModels.find_contact(username, contact_name)
    
    def delete_contact(selt, contacId):
        if ContactModels.delete_contac(contacId):
            messagebox.showinfo("Thông Báo!", "Xoá bạn thành công.")
            contact_view = selt.dashboard_controller.frames.get("CONTACT")
            if contact_view:
                contact_view.refresh_data()
        else:
            messagebox.showinfo("Thông Báo!", "Có lỗi trong quá trình xử lý.\nVui lòng thử lại sau!")
    
    def add_contact(selt, username, contact_name, email, phone):
        if ContactModels.add_contact(username, contact_name, email, phone):
            messagebox.showinfo("Thông Báo!", "Thêm bạn thành công.")
            contact_view = selt.dashboard_controller.frames.get("FIND_CONTACT")
            if contact_view:
                contact_view.refresh_data()
        else:
            messagebox.showinfo("Thông Báo!", "Có lỗi trong quá trình xử lý.\nVui lòng thử lại sau!")

    def send_message(selt, sender_id , receiver_id , message):
        if MessageModels.create_message(sender_id , receiver_id , message):
            contact_view = selt.dashboard_controller.frames.get("MESSAGE")
            if contact_view:
                contact_view.refresh_data()
            return True
        else:
            messagebox.showinfo("Thông Báo!", "Có lỗi trong quá trình xử lý.\nVui lòng thử lại sau!")
            return False
    
    def call_find_contact_view(self):
        self.dashboard_controller.show_screen("FIND_CONTACT")

    def show_contact_view(self):
        self.dashboard_controller.show_screen("CONTACT")

    def show_message(self, contactId):
        self.dashboard_controller.show_message(contactId)

    def get_messages(self, user_name, contact_name):
        return MessageModels.load_messages(user_name, contact_name)

    def decrypt_pass(self, acc_pass_enc, key_enc):
        return decrypt_password(acc_pass_enc, key_enc)
    
    def get_list_acc(self, username):
        return AccountModels.get_list_account(username)

    def checking_new_messages(self, user_name, contact_name):
        new_messages = MessageModels.check_new_messages(user_name, contact_name, self.last_check_time)
        if new_messages:
            self.last_check_time = datetime.now()
            return True
        else: return False
