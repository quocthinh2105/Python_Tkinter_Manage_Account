import tkinter as tk
from tkinter import font
import functools

class AccountView(tk.Frame):
    def __init__(self, parent, controller, user):
        super().__init__(parent)
        self.controller = controller
        self.user = user

        self.canvas = tk.Canvas(self, width=410, height=375, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_accountview()

    def create_accountview(self):
        self.label_account = tk.Label(self.canvas, text="Danh Sách Tài Khoản", font=("Inter", 18, "bold"))
        self.canvas.create_window(205, 30, window=self.label_account)

        # Tìm kiếm
        self.label_search = tk.Label(self.canvas, text="Tìm kiếm", font=("Inter", 10))
        self.canvas.create_window(45, 70, window=self.label_search)

        self.search = tk.Entry(self.canvas, width=25, font=("Arial", 10))
        self.canvas.create_window(150, 70, width=140, height=25, window=self.search)
        self.search.bind("<KeyRelease>", self.filter_accounts)
        self.accounts = self.controller.get_list_acc(self.user.username)
        self.filtered_accounts = []

        self.sort_option = tk.StringVar()
        self.sort_option.set("Mới Nhất")
        sort_button = tk.Button(self.canvas, text="Sắp xếp", command=self.sort_accounts)
        self.canvas.create_window(250, 70, window=sort_button)

        buttonAdd = tk.Button(self.canvas, text="Thêm Mới", font=("Arial", 10), command=lambda:self.controller.call_create_account_view(), bg="#1492C3", fg="#ffffff")
        self.canvas.create_window(360, 70, window=buttonAdd)

        self.list_canvas = tk.Canvas(self.canvas, width=380, height=280, bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.list_canvas.yview)
        self.list_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Place canvas and scrollbar correctly
        self.canvas.create_window(205, 90, window=self.list_canvas, anchor="n")
        self.canvas.create_window(406, 90, height=280, window=self.scrollbar, anchor="ne")

        # Create frame inside the canvas
        self.list_frame = tk.Frame(self.list_canvas, bg="#F9F9FC")
        self.list_canvas.create_window((0, 0), window=self.list_frame, anchor="nw") 

        self.list_account(self.accounts)

        # Update the canvas scroll region after adding all account frames
        self.list_frame.update_idletasks()
        self.list_canvas.config(scrollregion=self.list_canvas.bbox("all"))

        # Bind the mouse wheel for scrolling
        self.list_canvas.bind("<Enter>", lambda e: self.list_canvas.bind_all("<MouseWheel>", self._on_mouse_wheel))
        self.list_canvas.bind("<Leave>", lambda e: self.list_canvas.unbind_all("<MouseWheel>"))

    def toggle_password(self, entry):
        if entry.cget('show') == '*':
            entry.config(show='')
        else:
            entry.config(show='*')

    def _on_mouse_wheel(self, event):
        self.list_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def refresh_data(self):
        self.canvas.delete("all")
        self.create_accountview() 

    def list_account(self, accounts):
        self.filtered_accounts = accounts

        if self.filtered_accounts is None:
            self.filtered_accounts = []

        self.filtered_accounts = sorted(self.filtered_accounts, key=lambda x: x.id, reverse=(self.sort_option.get() == "Cũ nhất"))

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for account in self.filtered_accounts:
            accountid = account.id
            app_name = account.app_name
            acc_name = account.acc_name
            acc_pass_enc = account.acc_pass_enc

            account_frame = tk.Frame(self.list_frame, bg="#FFFFFF", pady=5, padx=5, relief="solid", bd=0, width=360, height=100)
            account_frame.pack_propagate(False)
            account_frame.pack(fill=tk.X, pady=5)

            app_name_label = tk.Label(account_frame, text=f"Ứng Dụng: {app_name}", font=("Inter", 12), bg="#FFFFFF")
            app_name_label.place(x=10, y=5)

            username_label = tk.Label(account_frame, text=f"Username: {acc_name}", font=("Inter", 12), bg="#FFFFFF")
            username_label.place(x=10, y=30)

            password_label = tk.Label(account_frame, text="Password:", font=("Inter", 12), bg="#FFFFFF")
            password_label.place(x=10, y=55)

            password_var = tk.StringVar(value=acc_pass_enc)
            password_entry = tk.Entry(account_frame, textvariable=password_var, font=("Inter", 12), bd=0, bg="#FFFFFF", show="*", state="readonly")
            password_entry.place(x=92, y=55, width=150)

            underlined_font = font.Font(family="Inter", size=10, underline=True)
            account_info = tk.Button(account_frame, text="Chi tiết", relief="flat", borderwidth=1, fg="#000000", font=("Inter", 11) , bg="#89EB89", 
                                             highlightthickness=0,  command=functools.partial(self.controller.call_account_view, accountid))
            account_info.place(x=280, y=10)

            delete_account_info = tk.Button(account_frame, text="Xoá", relief="flat", borderwidth=1, fg="#AC1D1F", font=underlined_font , bg="#FFFFFF", 
                                             highlightthickness=0,  command=functools.partial(self.controller.delete_account, accountid))
            delete_account_info.place(x=290, y=50)

            # show_password_button = tk.Button(account_frame, text="👁", relief="flat", borderwidth=0, font=("Inter", 8), bg="#FFFFFF", 
            #                                  highlightthickness=0,  command=lambda e=password_entry: self.toggle_password(e))
            # show_password_button.place(x=300, y=55)

    def filter_accounts(self, event=None):
        search_text = self.search.get().lower()
        filtered_accounts = []
        for account in self.accounts:
            if search_text in account.app_name.lower() or search_text in account.acc_name.lower():
                filtered_accounts.append(account)
        self.filtered_accounts = filtered_accounts
        self.list_account(self.filtered_accounts)

    def sort_accounts(self):
        if self.sort_option.get() == "Mới nhất":
            self.sort_option.set("Cũ nhất")
        else:
            self.sort_option.set("Mới nhất")
        self.list_account(self.filtered_accounts)
