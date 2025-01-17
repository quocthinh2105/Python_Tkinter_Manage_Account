from tkinter import messagebox
from utils.EncDecryption import encoded_key, encrypt_password, decrypt_password
from model.AccountModel import AccountModels

class AccountController:
    def __init__(self, root, dashboard_controller):
        self.app = root
        self.dashboard_controller = dashboard_controller

    def get_list_acc(selt, username):
        return AccountModels.get_list_account(username)
    
    def get_acc(selt, accountId):
        return AccountModels.find_account(accountId)
    
    def call_create_account_view(self):
        self.dashboard_controller.show_screen("CREATE_ACCOUNT")

    def call_account_view(self, accountId):
        self.dashboard_controller.show_accountInfo(accountId)

    def show_account_view(self):
        self.dashboard_controller.show_screen("ACCOUNT")

    def decrypt_pass(self, acc_pass_enc, key_enc):
        return decrypt_password(acc_pass_enc, key_enc)

    def create_account(self, username, app_name, acc_name, acc_pass, description):
        key_enc = encoded_key()
        acc_pass_enc = encrypt_password(acc_pass, key_enc)
        if AccountModels.create_account(username, app_name, acc_name, acc_pass, acc_pass_enc, key_enc, description):
            messagebox.showinfo("Thông Báo!", "Tạo tài khoản thành công.")
        else:
            messagebox.showinfo("Thông Báo!", "Có lỗi trong quá trình xử lý.\nVui lòng thử lại sau!")

    def update_account(self, accountId, app_name, acc_name, acc_pass, description):
        key_enc = encoded_key()
        acc_pass_enc = encrypt_password(acc_pass, key_enc)
        if AccountModels.update_account(accountId, app_name, acc_name, acc_pass, acc_pass_enc, key_enc, description):
            messagebox.showinfo("Thông Báo!", "Cập nhật tài khoản thành công.")
            account_view = self.dashboard_controller.frames.get("ACCOUNT_INFO")
            if account_view:
                account_view.refresh_data()
        else:
            messagebox.showinfo("Thông Báo!", "Có lỗi trong quá trình xử lý.\nVui lòng thử lại sau!")